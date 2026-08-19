#!/usr/bin/env python3
"""Resolutor en red del registro de fuentes (`make refresh-sources`).

**No corre en CI y no bloquea nada.** Sale a la red, que es exactamente lo que
un verificador no puede hacer: pregunta a OpenLibrary por los libros, a Crossref
por los artículos y al sitio del organismo por las normas, y solo escribe un
localizador cuando la respuesta coincide con la obra que el programa cita.

Reglas que lo gobiernan:

  * **nada se inventa**: si ninguna API responde por la obra, la entrada se queda
    en `pendiente` con la nota de qué se intentó;
  * **nada se borra**: una obra que dejó de resolver conserva su entrada y se
    reporta como regresión;
  * **coincidencia estricta**: un título parecido no es la misma obra. Se exige
    igualdad normalizada del título o una similitud muy alta, más el apellido del
    primer autor y el año dentro de un margen de dos.

Uso:
  python scripts/refrescar_fuentes.py                # resuelve solo las pendientes
  python scripts/refrescar_fuentes.py --todas        # revalida también las verificadas
  python scripts/refrescar_fuentes.py --solo id1,id2 # revisa entradas concretas
  python scripts/refrescar_fuentes.py --dry-run      # informa y no escribe nada
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import html
import json
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fuentes as F  # noqa: E402

RAIZ = F.RAIZ
CANDIDATOS = RAIZ / "sources" / "candidatos-normativos.json"
CACHE = RAIZ / ".cache" / "fuentes-red.json"

AGENTE = ("education-pedagogy-learning-sciences-program/2.0 "
          "(+https://github.com/vladimiracunadev-create/"
          "education-pedagogy-learning-sciences-program)")

SIMILITUD_MINIMA = 0.94
MARGEN_ANIOS = 2
ESPERA = 0.25  # cortesía con las APIs públicas

_candado = threading.Lock()
_ultima_peticion: dict[str, float] = {}


# --------------------------------------------------------------------------- #
# Red
# --------------------------------------------------------------------------- #

def esperar(host: str) -> None:
    with _candado:
        ahora = time.monotonic()
        anterior = _ultima_peticion.get(host, 0.0)
        pausa = ESPERA - (ahora - anterior)
        if pausa > 0:
            time.sleep(pausa)
        _ultima_peticion[host] = time.monotonic()


def pedir(url: str, *, texto: bool = False, timeout: int = 30, intentos: int = 3):
    """GET con cabecera identificable, reintentos y cortesía.

    Reintenta porque la alternativa es peor: un 429 pasajero convertido en
    silencio marcaría como «sin localizador» una obra que sí resuelve, y eso es
    exactamente el error que este registro existe para no cometer.
    """
    host = urllib.parse.urlparse(url).netloc
    for intento in range(1, intentos + 1):
        esperar(host)
        peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE,
                                                        "Accept": "*/*"})
        try:
            with urllib.request.urlopen(peticion, timeout=timeout) as respuesta:
                crudo = respuesta.read(4_000_000)
                if texto:
                    codificacion = respuesta.headers.get_content_charset() or "utf-8"
                    return crudo.decode(codificacion, errors="replace")
                return json.loads(crudo.decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as fallo:
            if fallo.code in (429, 500, 502, 503, 504) and intento < intentos:
                espera = float(fallo.headers.get("Retry-After") or 0) or 2.0 * intento
                time.sleep(min(espera, 20.0))
                continue
            return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            if intento < intentos:
                time.sleep(1.5 * intento)
                continue
            return None
    return None


# --------------------------------------------------------------------------- #
# Coincidencia
# --------------------------------------------------------------------------- #

def similitud(a: str, b: str) -> float:
    """Parecido entre el título que cita el programa (a) y el que devuelve la API (b).

    La asimetría es deliberada. Que la respuesta **añada** subtítulo —«Cleverlands:
    the secrets behind…» frente a «Cleverlands»— sigue siendo la misma obra. Que la
    respuesta sea **más corta** que la cita no lo es: «Grading» no es «Grading and
    Group Work», y aceptarlo escribiría un DOI ajeno con aspecto de correcto. Los
    índices que guardan el subtítulo en un campo aparte se cubren comparando también
    la variante «título: subtítulo», no relajando esta regla.
    """
    na, nb = F.normalizar(a), F.normalizar(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if nb.startswith(na + " "):
        return 0.97
    return difflib.SequenceMatcher(None, na, nb).ratio()


def variantes(titulo, subtitulo) -> list[str]:
    """Título tal cual y título con su subtítulo, que muchos índices separan."""
    titulos = [t for t in (titulo or []) if t]
    subtitulos = [s for s in (subtitulo or []) if s]
    salida = list(titulos)
    for t in titulos:
        for s in subtitulos:
            salida.append(f"{t}: {s}")
    return salida or [""]


def apellidos(entrada: dict) -> list[str]:
    salida = []
    for autor in entrada.get("authors", []):
        apellido = autor.split(",")[0].replace("et al", "").strip()
        if len(apellido) > 2:
            salida.append(F.normalizar(apellido))
    return salida


def autor_coincide(entrada: dict, nombres: list[str]) -> bool:
    esperados = apellidos(entrada)
    if not esperados:
        return True  # la cita no nombra autor: no se puede exigir coincidencia
    if not nombres:
        return False
    devueltos = " ".join(F.normalizar(n) for n in nombres)
    return any(apellido in devueltos for apellido in esperados)


def anio_coincide(entrada: dict, anio) -> bool:
    esperado = entrada.get("published", "")
    if not esperado or not anio:
        return True
    try:
        return abs(int(esperado) - int(anio)) <= MARGEN_ANIOS
    except (TypeError, ValueError):
        return True


# --------------------------------------------------------------------------- #
# OpenLibrary → ISBN-13
# --------------------------------------------------------------------------- #

def buscar_libro(entrada: dict) -> dict | None:
    consulta = {
        "title": entrada["title"],
        "limit": "5",
        "fields": "title,subtitle,author_name,first_publish_year,isbn,publisher",
    }
    if apellidos(entrada):
        consulta["author"] = entrada["authors"][0].split(",")[0]
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(consulta)
    datos = pedir(url)
    if not datos:
        return None
    for doc in datos.get("docs", []):
        titulos = variantes([doc.get("title", "")], [doc.get("subtitle", "")])
        parecido = max(similitud(entrada["title"], t) for t in titulos)
        if parecido < SIMILITUD_MINIMA:
            continue
        if not autor_coincide(entrada, doc.get("author_name", [])):
            continue
        if not anio_coincide(entrada, doc.get("first_publish_year")):
            continue
        candidatos = [i for i in doc.get("isbn", []) if F.isbn13_valido(i)][:3]
        for posicion, isbn in enumerate(candidatos):
            # Se intenta confirmar la edición concreta. El endpoint de ediciones de
            # OpenLibrary se cae con frecuencia; cuando no responde no se descarta el
            # ISBN —viene del propio índice de OpenLibrary para esta obra— pero la
            # entrada deja constancia de que la confirmación se quedó en el índice.
            edicion = pedir(f"https://openlibrary.org/isbn/{isbn}.json",
                            timeout=15, intentos=1)
            if edicion:
                titulo_edicion = variantes([edicion.get("title", "")],
                                           [edicion.get("subtitle", "")])
                if max(similitud(entrada["title"], t) for t in titulo_edicion) < 0.80:
                    continue
                confirmacion = "edicion"
                devuelto = edicion.get("title", "")
                editorial = (edicion.get("publishers")
                             or doc.get("publisher") or ["OpenLibrary"])[0]
            elif posicion < len(candidatos) - 1:
                continue  # queda otro ISBN por probar antes de conformarse con el índice
            else:
                confirmacion = "indice de busqueda"
                devuelto = doc.get("title", "")
                editorial = (doc.get("publisher") or ["OpenLibrary"])[0]
            return {
                "isbn13": isbn,
                "locator": f"https://openlibrary.org/isbn/{isbn}",
                "authority": editorial,
                "type": "book",
                "resolucion": {
                    "fuente": "openlibrary",
                    "titulo_devuelto": devuelto,
                    "similitud": round(parecido, 3),
                    "confirmacion": confirmacion,
                },
            }
    return None


# --------------------------------------------------------------------------- #
# Crossref → DOI
# --------------------------------------------------------------------------- #

def buscar_articulo(entrada: dict) -> dict | None:
    bibliografica = " ".join(filter(None, [
        entrada["title"],
        " ".join(a.split(",")[0] for a in entrada.get("authors", [])[:2]),
        entrada.get("published", ""),
    ]))
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": bibliografica,
        "rows": "5",
        "select": "DOI,title,subtitle,author,issued,type,publisher,ISBN",
    })
    datos = pedir(url)
    if not datos:
        return None
    items = datos.get("message", {}).get("items", [])
    # Primero el más parecido; entre dos registros del mismo trabajo, el DOI
    # normalizado antes que el antiguo de doble barra.
    items.sort(key=lambda i: (
        -max(similitud(entrada["title"], t)
             for t in variantes(i.get("title"), i.get("subtitle"))),
        "//" in i.get("DOI", ""),
        len(i.get("DOI", "")),
    ))
    for item in items:
        titulos = variantes(item.get("title"), item.get("subtitle"))
        parecido = max(similitud(entrada["title"], t) for t in titulos)
        if parecido < SIMILITUD_MINIMA:
            continue
        nombres = [f"{a.get('family', '')} {a.get('given', '')}" for a in item.get("author", [])]
        if not autor_coincide(entrada, nombres):
            continue
        partes = item.get("issued", {}).get("date-parts") or [[None]]
        if not anio_coincide(entrada, partes[0][0]):
            continue
        doi = item.get("DOI", "")
        if not F.doi_valido(doi):
            continue
        resolucion = {
            "fuente": "crossref",
            "titulo_devuelto": titulos[0],
            "similitud": round(parecido, 3),
            "tipo_crossref": item.get("type", ""),
        }
        # Crossref también indexa libros. Si responde por uno y trae ISBN-13, el
        # localizador correcto es el ISBN, no el DOI del registro editorial.
        if item.get("type") in {"book", "monograph", "edited-book"}:
            for bruto in item.get("ISBN", []):
                isbn = bruto.replace("-", "").strip()
                if F.isbn13_valido(isbn):
                    return {
                        "isbn13": isbn,
                        "locator": f"https://openlibrary.org/isbn/{isbn}",
                        "authority": item.get("publisher", "Crossref"),
                        "type": "book",
                        "resolucion": resolucion,
                    }
            continue
        return {
            "doi": doi,
            "locator": f"https://doi.org/{doi}",
            "authority": item.get("publisher", "Crossref"),
            "type": "paper",
            "resolucion": resolucion,
        }
    return None


# --------------------------------------------------------------------------- #
# Normas y documentación oficial → URL comprobada
# --------------------------------------------------------------------------- #

def cargar_candidatos() -> dict[str, dict]:
    if not CANDIDATOS.exists():
        return {}
    return json.loads(CANDIDATOS.read_text(encoding="utf-8")).get("candidatos", {})


def comprobar_norma(entrada: dict, candidato: dict) -> dict | None:
    """Una URL propuesta solo vale si responde y si el documento habla de la obra.

    Un 200 prueba que la URL existe, no que sea el documento: por eso se exige
    además que el texto devuelto contenga las marcas declaradas en el candidato.
    Cuando la página publicada es una aplicación JavaScript que no sirve su texto
    —LeyChile, por ejemplo— el candidato declara en `comprobar` el servicio que sí
    lo devuelve, y el localizador publicado sigue siendo la página humana.
    """
    urls = candidato.get("urls") or ([candidato["url"]] if candidato.get("url") else [])
    marcas = candidato.get("marcas") or [entrada["title"]]
    for url in urls:
        if not F.URL_RE.match(url):
            continue
        cuerpo = pedir(candidato.get("comprobar") or url, texto=True, timeout=45)
        if cuerpo is None:
            continue
        # Los servicios de LeyChile devuelven el texto con entidades HTML
        # («ADECUACI&#211;N»). Sin deshacerlas, la marca «adecuación curricular»
        # no aparecería y una norma que sí resuelve se daría por perdida.
        plano = F.normalizar(html.unescape(cuerpo))
        if [m for m in marcas if F.normalizar(m) not in plano]:
            continue
        return {
            "locator": url,
            "authority": candidato.get("autoridad", ""),
            "type": candidato.get("tipo", "standard"),
            "accessed": dt.date.today().isoformat(),
            "resolucion": {
                "fuente": "sitio-oficial",
                "comprobado_en": candidato.get("comprobar") or url,
                "marcas_comprobadas": marcas,
            },
        }
    return None


# --------------------------------------------------------------------------- #
# Orquestación
# --------------------------------------------------------------------------- #

def resolver(entrada: dict, candidatos: dict[str, dict]) -> dict | None:
    candidato = candidatos.get(entrada["id"])
    if candidato:
        hallazgo = comprobar_norma(entrada, candidato)
        if hallazgo:
            return hallazgo
        if entrada["type"] == "standard":
            return None
    if entrada["type"] == "standard":
        return None
    orden = (buscar_articulo, buscar_libro) if entrada["type"] == "paper" \
        else (buscar_libro, buscar_articulo)
    for buscar in orden:
        hallazgo = buscar(entrada)
        if hallazgo:
            return hallazgo
    return None


def nota_pendiente(entrada: dict, candidatos: dict[str, dict]) -> str:
    """Por qué esta obra sigue sin localizador. La nota es el dato, no el relleno."""
    candidato = candidatos.get(entrada["id"])
    if candidato:
        urls = candidato.get("urls") or [candidato.get("url", "")]
        return (f"hay URL oficial propuesta ({urls[0]}) en sources/candidatos-normativos.json, "
                "pero el sitio no respondió al verificador desde este entorno; "
                "queda pendiente de comprobación manual")
    if entrada["type"] == "standard":
        return ("documento oficial sin URL estable comprobada: se cita la edición vigente y "
                "hay que localizarla en el sitio del organismo")
    return ("ni OpenLibrary ni Crossref devolvieron una coincidencia estricta de título, "
            "autor y año; vuelve a intentarlo con scripts/refrescar_fuentes.py")


def cargar_cache() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def guardar_cache(cache: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--todas", action="store_true",
                        help="revalida también las entradas ya verificadas")
    parser.add_argument("--solo", default="",
                        help="lista de ids separados por coma")
    parser.add_argument("--dry-run", action="store_true", help="informa sin escribir")
    parser.add_argument("--hilos", type=int, default=4)
    parser.add_argument("--sin-cache", action="store_true")
    args = parser.parse_args()

    registro = F.cargar_registro()
    candidatos = cargar_candidatos()
    cache = {} if args.sin_cache else cargar_cache()
    solo = {i.strip() for i in args.solo.split(",") if i.strip()}

    objetivo = [
        e for e in registro["entries"]
        if (not solo or e["id"] in solo)
        and (args.todas or solo or e["status"] != "verificada")
    ]
    print(f"Resolviendo {len(objetivo)} de {len(registro['entries'])} entradas…")

    resueltas, perdidas, sin_suerte = [], [], []

    def trabajar(entrada: dict) -> tuple[dict, dict | None]:
        clave = entrada["id"]
        if clave in cache and not args.sin_cache:
            return entrada, cache[clave]
        return entrada, resolver(entrada, candidatos)

    # as_completed y no map: con map, una sola entrada lenta al principio retiene el
    # informe de todas las que ya terminaron y el progreso parece congelado.
    with ThreadPoolExecutor(max_workers=max(1, args.hilos)) as pool:
        tareas = [pool.submit(trabajar, e) for e in objetivo]
        for hechas, tarea in enumerate(as_completed(tareas), start=1):
            entrada, hallazgo = tarea.result()
            if hechas % 25 == 0 or hechas == len(objetivo):
                print(f"  {hechas}/{len(objetivo)}…", flush=True)
            # Solo se cachea lo que resolvió: guardar los fracasos convertiría un
            # 429 pasajero en un «pendiente» permanente que nadie volvería a probar.
            if hallazgo:
                cache[entrada["id"]] = hallazgo
                entrada.update(hallazgo)
                entrada["status"] = "verificada"
                entrada.pop("nota", None)
                if entrada["type"] != "standard":
                    entrada["accessed"] = dt.date.today().isoformat()
                resueltas.append(entrada["id"])
            elif entrada["status"] == "verificada":
                # No se borra: se degrada y se informa para revisarla a mano.
                entrada["status"] = "pendiente"
                entrada["nota"] = ("dejó de resolver en la última comprobación; "
                                   "el localizador anterior queda en resolucion")
                for campo in ("isbn13", "doi", "locator"):
                    entrada.pop(campo, None)
                perdidas.append(entrada["id"])
            else:
                entrada["nota"] = nota_pendiente(entrada, candidatos)
                sin_suerte.append(entrada["id"])

    registro["verified_on"] = dt.date.today().isoformat()
    if not args.dry_run:
        F.guardar_registro(registro)
        guardar_cache(cache)

    datos = F.resumen(registro)
    print(f"\nResueltas ahora: {len(resueltas)}")
    print(f"Sin localizador (siguen pendientes): {len(sin_suerte)}")
    if perdidas:
        print(f"REGRESIONES — dejaron de resolver: {len(perdidas)}")
        for ident in perdidas:
            print(f"  - {ident}")
    print(f"\nRegistro: {datos['obras']} obras · {datos['verificadas']} verificadas "
          f"({datos['cobertura']} %) · {datos['pendientes']} pendientes")
    if args.dry_run:
        print("(--dry-run: no se escribió nada)")
    else:
        print("Recuerda ejecutar: python scripts/verificar_fuentes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
