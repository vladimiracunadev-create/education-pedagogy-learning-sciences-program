#!/usr/bin/env python3
"""Verificador offline del registro de fuentes (`make verify-sources`).

Corre en CI y bloquea. No toca la red **a propósito**: si el CI dependiera de que
OpenLibrary, Crossref o el sitio de un ministerio respondan, se pondría rojo por
razones ajenas al repositorio y en dos semanas nadie lo miraría. La resolución en
red vive aparte, en `refrescar_fuentes.py`, y no bloquea nada.

Lo que comprueba:

  1. `sources/bibliography.json` parsea y cumple el esquema declarado;
  2. toda entrada `verificada` de tipo `book` lleva ISBN-13 con dígito de control
     válido, y toda `paper`, un DOI bien formado;
  3. el `locator` coincide con la forma canónica que corresponde a su tipo;
  4. toda obra citada por una clase o por una portada de parte existe en el registro;
  5. ninguna entrada del registro queda sin usar, y `used_in` refleja exactamente
     lo que dicen los manifiestos;
  6. ningún bloque de fuentes se repite entre clases;
  7. `docs/REGISTRO_DE_FUENTES.md` está al día y las cifras que el README da sobre
     las fuentes coinciden con el recuento —las escribe este script, no una persona.

Uso:
  python scripts/verificar_fuentes.py            # escribe el documento y las cifras
  python scripts/verificar_fuentes.py --check    # falla si algo no está al día
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fuentes as F  # noqa: E402

RAIZ = F.RAIZ
CURRICULO = RAIZ / "curriculum"
README = RAIZ / "README.md"

MARCA_INICIO = "<!-- registro-de-fuentes:inicio -->"
MARCA_FIN = "<!-- registro-de-fuentes:fin -->"
NAV_BIBLIOGRAFIA = re.compile(r"\[📚 Bibliografía \([^)]*\)\]\(docs/BIBLIOGRAFIA\.md\)")
FRASE_OBRAS = re.compile(r"En total, \*\*[\d.]+ obras\*\*[\s\S]*?normativas\*\*—\.")

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECCION_FUENTES = "## 📗 Fuentes y verificación"

TITULOS_TIPO = {
    "book": "Libros",
    "paper": "Artículos y capítulos",
    "standard": "Normas y documentación oficial",
    "reference": "Obras de referencia",
    "dataset": "Conjuntos de datos",
}


def error(fallos: list[str], mensaje: str) -> None:
    fallos.append(mensaje)


# --------------------------------------------------------------------------- #
# Siembra: el registro sigue a los manifiestos, nunca al revés
# --------------------------------------------------------------------------- #

def sembrar(registro: dict, usos: dict[str, list[str]]) -> list[str]:
    """Añade las obras nuevas y actualiza `used_in`. No borra nada jamás.

    Una obra que desaparece de los manifiestos deja su entrada huérfana y el
    verificador lo dice: quitarla es una decisión editorial, no automática.
    """
    cambios: list[str] = []
    por_cita = {e["cita"]: e for e in registro["entries"]}
    tomados = {e["id"] for e in registro["entries"]}

    for cita, rutas in usos.items():
        entrada = por_cita.get(cita)
        if entrada is None:
            datos = F.parsear(cita)
            entrada = {
                "id": F.identificador(cita, tomados),
                "type": F.clasificar(cita),
                "cita": cita,
                "authors": datos["authors"],
                "title": datos["title"],
                "published": datos["published"],
                "locator": "",
                "authority": "",
                "accessed": "",
                "used_in": list(rutas),
                "status": "pendiente",
                "nota": "sin localizador comprobado todavía: ejecuta scripts/refrescar_fuentes.py",
            }
            tomados.add(entrada["id"])
            registro["entries"].append(entrada)
            por_cita[cita] = entrada
            cambios.append(f"nueva obra: {entrada['id']}")
        elif entrada["used_in"] != list(rutas):
            entrada["used_in"] = list(rutas)
            cambios.append(f"usos actualizados: {entrada['id']}")

    registro["entries"].sort(key=lambda e: (e["type"], e["id"]))
    return cambios


# --------------------------------------------------------------------------- #
# Validación
# --------------------------------------------------------------------------- #

def validar_esquema(registro: dict, fallos: list[str]) -> None:
    if registro.get("schema_version") != F.ESQUEMA:
        error(fallos, f"schema_version debe ser {F.ESQUEMA}")
    if not F.FECHA_RE.match(str(registro.get("verified_on", ""))):
        error(fallos, "verified_on debe tener forma AAAA-MM-DD")
    if not str(registro.get("policy", "")).strip():
        error(fallos, "falta la política del registro")
    if not isinstance(registro.get("entries"), list) or not registro["entries"]:
        error(fallos, "entries debe ser una lista no vacía")


def validar_entrada(entrada: dict, fallos: list[str]) -> None:
    ident = entrada.get("id", "«sin id»")
    if not ID_RE.match(entrada.get("id", "")):
        error(fallos, f"{ident}: el id no es kebab-case")
    if entrada.get("type") not in F.TIPOS:
        error(fallos, f"{ident}: tipo desconocido «{entrada.get('type')}»")
    if entrada.get("status") not in F.ESTADOS:
        error(fallos, f"{ident}: estado desconocido «{entrada.get('status')}»")
    if not str(entrada.get("title", "")).strip():
        error(fallos, f"{ident}: sin título")
    if not isinstance(entrada.get("authors"), list):
        error(fallos, f"{ident}: authors debe ser una lista")
    if not entrada.get("used_in"):
        error(fallos, f"{ident}: ninguna clase ni portada de parte la usa")
    for ruta in entrada.get("used_in", []):
        if not (RAIZ / ruta).exists():
            error(fallos, f"{ident}: used_in apunta a una ruta inexistente → {ruta}")

    tipo, estado = entrada.get("type"), entrada.get("status")
    isbn, doi = entrada.get("isbn13", ""), entrada.get("doi", "")
    locator = entrada.get("locator", "")

    if estado == "verificada":
        if tipo == "book":
            if not F.isbn13_valido(isbn):
                error(fallos, f"{ident}: libro verificado sin ISBN-13 válido → «{isbn}»")
        elif tipo == "paper":
            if not F.doi_valido(doi):
                error(fallos, f"{ident}: artículo verificado sin DOI válido → «{doi}»")
        else:
            if not F.URL_RE.match(locator):
                error(fallos, f"{ident}: {tipo} verificado sin URL https → «{locator}»")
            if not F.FECHA_RE.match(entrada.get("accessed", "")):
                error(fallos, f"{ident}: {tipo} verificado sin fecha de consulta")
        canonico = F.locator_canonico(entrada)
        if canonico and locator != canonico:
            error(fallos, f"{ident}: el locator no es la forma canónica → «{locator}»")
        if not str(entrada.get("authority", "")).strip():
            error(fallos, f"{ident}: verificada sin declarar quién responde por la fuente")
    else:
        # Un hueco declarado es información; un hueco relleno a ojo es una invención.
        for campo in ("isbn13", "doi", "locator"):
            if str(entrada.get(campo, "")).strip():
                error(fallos, f"{ident}: pendiente pero trae {campo}; o se verifica o se vacía")
        if not str(entrada.get("nota", "")).strip():
            error(fallos, f"{ident}: pendiente sin nota que explique por qué")

    if isbn and not F.isbn13_valido(isbn):
        error(fallos, f"{ident}: ISBN-13 con dígito de control inválido → «{isbn}»")
    if doi and not F.doi_valido(doi):
        error(fallos, f"{ident}: DOI mal formado → «{doi}»")


def validar_cobertura(registro: dict, usos: dict[str, list[str]], fallos: list[str]) -> None:
    por_cita = {e["cita"]: e for e in registro["entries"]}
    for cita in usos:
        if cita not in por_cita:
            error(fallos, f"obra usada y ausente del registro → {cita[:70]}")
    for entrada in registro["entries"]:
        if entrada["cita"] not in usos:
            error(fallos, f"{entrada['id']}: entrada del registro que ya no cita nadie")
        elif entrada["used_in"] != usos[entrada["cita"]]:
            error(fallos, f"{entrada['id']}: used_in no coincide con los manifiestos")
    ids = [e["id"] for e in registro["entries"]]
    for repetido in sorted({i for i in ids if ids.count(i) > 1}):
        error(fallos, f"id duplicado en el registro → {repetido}")


def bloque_de_fuentes(texto: str) -> str:
    if SECCION_FUENTES not in texto:
        return ""
    cuerpo = texto.split(SECCION_FUENTES, 1)[1]
    cuerpo = cuerpo.split("\n## ", 1)[0]
    return " ".join(cuerpo.split())


def validar_bloques(fallos: list[str]) -> int:
    """Ninguna clase puede apoyarse en el mismo bloque de fuentes que otra."""
    vistos: dict[str, str] = {}
    contados = 0
    for archivo in sorted(CURRICULO.glob("part-*/class-*/README.md")):
        relativo = archivo.relative_to(RAIZ).as_posix()
        bloque = bloque_de_fuentes(archivo.read_text(encoding="utf-8"))
        if not bloque:
            error(fallos, f"{relativo}: sin bloque de fuentes")
            continue
        contados += 1
        if bloque in vistos:
            error(fallos, f"{relativo}: bloque de fuentes idéntico al de {vistos[bloque]}")
        else:
            vistos[bloque] = relativo
    return contados


# --------------------------------------------------------------------------- #
# Documento generado y cifras del README
# --------------------------------------------------------------------------- #

def enlace_locator(entrada: dict) -> str:
    if entrada["status"] != "verificada" or not entrada.get("locator"):
        motivo = entrada.get("nota", "sin localizador comprobado").replace("|", "·")
        return f"⏳ pendiente — {motivo}"
    etiqueta = entrada.get("isbn13") or entrada.get("doi") or entrada["locator"]
    return f"[{etiqueta}]({entrada['locator']})"


def etiquetas_de_ruta() -> dict[str, str]:
    """Ruta publicada → cómo se nombra en el registro: «106» o «parte 08»."""
    curriculo, _packs, _clases = F.cargar_manifiestos()
    etiquetas: dict[str, str] = {}
    for clase in curriculo:
        base = f"curriculum/{clase['part_slug']}"
        etiquetas[f"{base}/{clase['slug']}/README.md"] = f"{clase['global_class']:03d}"
        etiquetas[f"{base}/README.md"] = f"parte {clase['part']:02d}"
    return etiquetas


def documento_registro(registro: dict) -> str:
    datos = F.resumen(registro)
    etiquetas = etiquetas_de_ruta()
    lineas = [
        "# Registro de fuentes con localizador",
        "",
        f"Las **{datos['obras']} obras** que citan las clases y las portadas de parte, cada una "
        f"con el localizador que permite llegar a ella: **{datos['verificadas']} verificadas** "
        f"({datos['cobertura']} %) y **{datos['pendientes']} pendientes**.",
        "",
        "Se genera con `python scripts/verificar_fuentes.py` a partir de "
        "[`sources/bibliography.json`](../sources/bibliography.json), que es el registro real. "
        "Las cifras de esta página y las del README las produce el verificador: **ninguna se "
        "escribe a mano**.",
        "",
        "| Estado | Qué significa |",
        "|---|---|",
        "| ✅ verificada | una API o el sitio del organismo respondió por la obra: ISBN-13, DOI "
        "o URL oficial comprobada |",
        "| ⏳ pendiente | no se consiguió un localizador que resolviera. **La obra no se borra: "
        "se declara el hueco.** |",
        "",
        "> [!IMPORTANT]",
        "> El localizador prueba que la obra existe y dónde encontrarla, no que su contenido",
        "> respalde lo que la clase afirma. Eso lo comprueba quien lee la obra.",
        "",
        "El tipo de esta página es el del **localizador** —ISBN-13, DOI o URL oficial—, no la "
        "naturaleza editorial de la obra: un informe de un organismo con ISBN aparece aquí como "
        "libro. El [índice de obras citadas](OBRAS_CITADAS.md) separa autores de organismos con "
        "el otro criterio, el de quién publica.",
        "",
        "| Tipo | Obras | Con localizador |",
        "|---|---:|---:|",
    ]
    for tipo, titulo in TITULOS_TIPO.items():
        deltipo = [e for e in registro["entries"] if e["type"] == tipo]
        if not deltipo:
            continue
        verificadas = sum(1 for e in deltipo if e["status"] == "verificada")
        lineas.append(f"| [{titulo}](#{tipo}) | {len(deltipo)} | {verificadas} |")
    lineas.append("")

    for tipo, titulo in TITULOS_TIPO.items():
        deltipo = [e for e in registro["entries"] if e["type"] == tipo]
        if not deltipo:
            continue
        lineas += [
            f'<a id="{tipo}"></a>',
            "",
            f"## {titulo}",
            "",
            "| Obra | Localizador | Responde | Usada en |",
            "|---|---|---|---:|",
        ]
        for entrada in sorted(deltipo, key=lambda e: e["id"]):
            usos = ", ".join(
                f"[{etiquetas.get(r, r)}](../{r})" for r in entrada["used_in"]
            )
            obra = entrada["cita"].replace("|", "·").rstrip(".")
            autoridad = entrada.get("authority") or "—"
            lineas.append(
                f'| <a id="{entrada["id"]}"></a>{obra} | {enlace_locator(entrada)} | '
                f"{autoridad} | {usos} |"
            )
        lineas.append("")

    lineas += [
        "---",
        "",
        "| Anterior | Índice | Siguiente |",
        "|---|---|---|",
        "| [Obras citadas](OBRAS_CITADAS.md) | [Programa](../README.md) · "
        "[Documentos](../FILE_INDEX.md) | [Fuentes oficiales](FUENTES.md) |",
        "",
    ]
    return "\n".join(lineas)


def sin_bloque_de_registro(texto: str) -> str:
    """Quita del README el bloque de cifras del registro, si quedara alguno.

    El README presenta el programa; auditarlo es tarea de STATUS.md y del propio
    documento del registro. Repetir ahí la misma tabla obligaba a leer dos veces
    lo mismo sin añadir nada, así que el bloque se retira y no se vuelve a poner.
    """
    if MARCA_INICIO not in texto or MARCA_FIN not in texto:
        return texto
    inicio = texto.index(MARCA_INICIO)
    fin = texto.index(MARCA_FIN) + len(MARCA_FIN)
    return texto[:inicio].rstrip("\n") + "\n\n" + texto[fin:].lstrip("\n")


def aplicar_readme(texto: str, registro: dict) -> str:
    d = F.resumen(registro)
    texto = sin_bloque_de_registro(texto)
    texto = NAV_BIBLIOGRAFIA.sub(
        f"[📚 Bibliografía ({d['obras']} obras · {d['verificadas']} con localizador)]"
        "(docs/BIBLIOGRAFIA.md)",
        texto,
    )
    # La frase que abre «Sobre qué está construido» también lleva cifras: se
    # reescribe desde el registro para que no pueda envejecer sola.
    return FRASE_OBRAS.sub(
        f"En total, **{d['obras']} obras** sostienen las 300 clases y sus 25 partes con "
        f"**{d['citas_en_clases']} citas** —**{d['academicas']} libros\ny artículos** de "
        f"investigación y **{d['institucionales']} fuentes institucionales o normativas**—.",
        texto,
    )


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si el registro o las cifras no están al día")
    args = parser.parse_args()

    if not F.REGISTRO.exists():
        print(f"ERROR: falta {F.REGISTRO.relative_to(RAIZ).as_posix()}", file=sys.stderr)
        return 1

    registro = F.cargar_registro()
    usos = F.usos_por_cita()
    fallos: list[str] = []

    cambios = sembrar(registro, usos)
    if cambios and args.check:
        for cambio in cambios[:10]:
            error(fallos, f"registro desactualizado ({cambio})")

    validar_esquema(registro, fallos)
    for entrada in registro["entries"]:
        validar_entrada(entrada, fallos)
    validar_cobertura(registro, usos, fallos)
    clases = validar_bloques(fallos)

    documento = documento_registro(registro)
    readme = aplicar_readme(README.read_text(encoding="utf-8"), registro)

    if args.check:
        actual = F.DOC_REGISTRO.read_text(encoding="utf-8") if F.DOC_REGISTRO.exists() else ""
        if actual != documento:
            error(fallos, "docs/REGISTRO_DE_FUENTES.md no está al día: "
                          "ejecuta python scripts/verificar_fuentes.py")
        if README.read_text(encoding="utf-8") != readme:
            error(fallos, "las cifras del README no coinciden con el registro: "
                          "ejecuta python scripts/verificar_fuentes.py")
    else:
        F.guardar_registro(registro)
        F.DOC_REGISTRO.write_text(documento, encoding="utf-8")
        README.write_text(readme, encoding="utf-8")

    # Dos citas que resuelven al mismo localizador son la misma obra escrita de dos
    # maneras. No es un error —el registro sigue siendo correcto— pero conviene
    # saberlo: unificar la cita en los manifiestos ahorra una entrada duplicada.
    compartidos: dict[str, list[str]] = {}
    for entrada in registro["entries"]:
        if entrada.get("locator"):
            compartidos.setdefault(entrada["locator"], []).append(entrada["id"])
    repetidos = {k: v for k, v in compartidos.items() if len(v) > 1}

    d = F.resumen(registro)
    if fallos:
        print(f"FALLOS ({len(fallos)}):", file=sys.stderr)
        for fallo in fallos:
            print(f"  - {fallo}", file=sys.stderr)
        return 1

    print(f"OK: {d['obras']} obras · {d['verificadas']} con localizador verificado "
          f"({d['cobertura']} %) · {d['pendientes']} pendientes declaradas")
    print(f"    {d['en_registro']}/{d['usadas']} obras usadas están en el registro · "
          f"{d['citas']} usos en {clases} clases y 25 portadas de parte")
    if repetidos:
        print(f"    aviso: {len(repetidos)} localizadores los comparten dos citas distintas "
              "de la misma obra (candidatas a unificar en los manifiestos)")
    if not args.check:
        print("    escritos: sources/bibliography.json, docs/REGISTRO_DE_FUENTES.md, README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
