#!/usr/bin/env python3
"""Núcleo compartido del registro de fuentes.

Aquí vive todo lo que necesitan por igual el verificador offline
(`verificar_fuentes.py`) y el resolutor en red (`refrescar_fuentes.py`):

  * de dónde salen las citas (los manifiestos, nunca el Markdown publicado);
  * cómo se parsea una cita «Autor (Año). *Título*» en autores, título y año;
  * qué es un localizador válido (ISBN-13 con dígito de control, DOI, URL https);
  * cómo se lee y se escribe `sources/bibliography.json`.

Regla que ordena el módulo: **nada de lo que se escribe aquí inventa un dato**.
Los campos bibliográficos se derivan de la cita que ya existía en el manifiesto;
los localizadores solo los añade el resolutor cuando una API los devuelve.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "manifests"
REGISTRO = RAIZ / "sources" / "bibliography.json"
DOC_REGISTRO = RAIZ / "docs" / "REGISTRO_DE_FUENTES.md"

ESQUEMA = 1
TIPOS = {"book", "paper", "standard", "reference", "dataset"}
ESTADOS = {"verificada", "pendiente"}

# Marcas de fuente institucional o normativa. Es la misma lista que usa
# generar_indice.py para separar obras de autor de normas y documentos oficiales:
# si las dos se separan con criterios distintos, las cifras dejan de cuadrar.
INSTITUCIONALES = (
    "mineduc", "ministerio", "biblioteca del congreso", "agencia de calidad",
    "superintendencia", "ocde", "unesco", "unicef", "organización", "organizacion",
    "comisión europea", "comision europea", "banco mundial", "foro económico",
    "education endowment", "casel", "cast", "ley ", "decreto ", "convención",
    "convencion", "national autism", "programa de educación", "sistema de créditos",
    "sistema de creditos", "normativa", "informe belmont", "declaration on research",
    "tuning", "aera", "who", "oit", "unevoc", "w3c", "aaidd", "comisión nacional",
    "comision nacional", "subsecretaría", "subsecretaria", "center on the developing",
    "international center for academic", "committee on publication",
    "what works clearinghouse",
)

# Pistas de artículo: una cita que nombra revista, volumen o número describe un
# artículo, y un artículo resuelve a DOI, no a ISBN.
REVISTA = re.compile(
    r"(?:Review|Journal|Psychological|Educational Researcher|Research|Quarterly|"
    r"Bulletin|Science|Nature|Pediatrics|Studies|Revista|Perspectives|Annals|"
    r"Reading Research|Teachers College Record|American Psychologist|"
    r"Educational Psychologist|Cognitive Science|Child Development)"
)
VOLUMEN = re.compile(r",\s*\d+\s*(?:\(\d+[^)]*\))?\s*\.?\s*$")

DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9<>\[\]+]+$")
ISBN13_RE = re.compile(r"^\d{13}$")
URL_RE = re.compile(r"^https://[^\s<>\"]+$")

FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- #
# Manifiestos: quién cita qué
# --------------------------------------------------------------------------- #

def cargar_manifiestos() -> tuple[list[dict], list[dict], dict[int, dict]]:
    curriculo = json.loads((MANIFIESTOS / "curriculum.json").read_text(encoding="utf-8"))
    packs: list[dict] = []
    for archivo in sorted((MANIFIESTOS / "parts").glob("*.json")):
        packs += json.loads(archivo.read_text(encoding="utf-8"))
    packs.sort(key=lambda p: p["part"])
    clases: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            clases[registro["n"]] = registro
    return curriculo, packs, clases


def usos_por_cita() -> dict[str, list[str]]:
    """Cita → rutas del repositorio que la usan, en el orden en que aparecen.

    La fuente es el manifiesto, no la página publicada: el Markdown se genera
    desde aquí, así que preguntarle a él sería preguntarle al eco.
    """
    curriculo, packs, clases = cargar_manifiestos()
    por_numero = {c["global_class"]: c for c in curriculo}
    usos: dict[str, list[str]] = {}

    def anotar(cita: str, ruta: str) -> None:
        rutas = usos.setdefault(cita.strip(), [])
        if ruta not in rutas:
            rutas.append(ruta)

    for numero, registro in sorted(clases.items()):
        clase = por_numero[numero]
        ruta = f"curriculum/{clase['part_slug']}/{clase['slug']}/README.md"
        for cita, _lente in registro["lecturas"]:
            anotar(cita, ruta)
    for pack in packs:
        parte = next(c for c in curriculo if c["part"] == pack["part"])
        ruta = f"curriculum/{parte['part_slug']}/README.md"
        for cita, _lente in pack["lecturas"]:
            anotar(cita, ruta)
    return usos


# --------------------------------------------------------------------------- #
# Parseo de la cita
# --------------------------------------------------------------------------- #

def sin_tildes(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def normalizar(texto: str) -> str:
    """Forma comparable de un título: sin tildes, sin puntuación, en minúsculas."""
    plano = sin_tildes(texto).lower()
    plano = re.sub(r"[^a-z0-9]+", " ", plano)
    return " ".join(plano.split())


def es_institucional(cita: str) -> bool:
    """¿La cita nombra a un organismo y no a un autor?

    Se exige que la marca termine en el límite de la palabra: «CAST (2024)» es el
    organismo que publica las pautas UDL, pero «Castles, A.» es una investigadora,
    y sin el límite las dos caerían del mismo lado.
    """
    minuscula = cita.strip().lower()
    for marca in INSTITUCIONALES:
        if not minuscula.startswith(marca):
            continue
        siguiente = minuscula[len(marca):len(marca) + 1]
        if marca.endswith(" ") or not siguiente.isalpha():
            return True
    return False


def parsear(cita: str) -> dict:
    """Descompone «Autores (Año). *Título*, cap. 1–2.» sin añadir nada.

    Lo que la cita no dice, queda vacío. Un autor que no está escrito no se
    deduce, y un año que no aparece no se estima.
    """
    texto = cita.strip()
    titulo = ""
    cursivas = re.findall(r"\*([^*]+)\*", texto)
    if cursivas:
        titulo = cursivas[0].strip().rstrip(".,;: ")
    anio = ""
    encabezado = texto.split("*", 1)[0] if cursivas else texto
    anios = re.findall(r"\((\d{4})\)", encabezado)
    if anios:
        anio = anios[0]

    autores_texto = encabezado
    if anio:
        autores_texto = encabezado.split(f"({anio})", 1)[0]
    autores_texto = autores_texto.strip().rstrip(".,;: ").strip()
    if not titulo:
        # Cita sin cursivas: es el nombre de un cuerpo normativo o de un sistema.
        titulo = re.sub(r"\s*\(edición vigente\)\.?$", "", texto).strip().rstrip(".")
        autores_texto = ""

    autores: list[str] = []
    if autores_texto:
        bruto = autores_texto.replace(" y ", " & ")
        # Se corta en «&», en «;» y en la coma que precede a un apellido nuevo:
        # «Serrano, S., Ponce de León, M. & Rengifo, F.» son tres personas, no una.
        trozos = re.split(r"\s*&\s*|\s*;\s*|,\s+(?=[A-ZÁÉÍÓÚÑ][\w'’-]+(?:\s+[a-zA-Zá-úÁ-Ú'’-]+)*,)",
                          bruto)
        for parte in trozos:
            parte = re.sub(r"\s*\((?:eds?\.|comps?\.|coords?\.)\)", "", parte)
            parte = parte.strip().strip(",").strip()
            if parte and re.search(r"[A-Za-zÁ-Úá-ú]$", parte) and re.search(
                    r"\b[A-ZÁÉÍÓÚÑ]$", parte):
                parte += "."  # inicial que perdió su punto al recortar la cita
            if parte:
                autores.append(parte)
    return {"authors": autores, "title": titulo, "published": anio}


def clasificar(cita: str) -> str:
    """Naturaleza declarada de la obra: norma, artículo o libro.

    Es una declaración, no una verificación: el resolutor puede corregirla
    cuando una API responde por la obra.
    """
    if es_institucional(cita):
        return "standard"
    cola = cita.split("*")[-1] if "*" in cita else cita
    if REVISTA.search(cola) or VOLUMEN.search(cita.strip()):
        return "paper"
    return "book"


def identificador(cita: str, tomados: set[str]) -> str:
    """id kebab-case estable: apellidos + año + primeras palabras del título."""
    datos = parsear(cita)
    apellidos = [a.split(",")[0] for a in datos["authors"][:2]]
    piezas = [normalizar(a) for a in apellidos if a]
    if datos["published"]:
        piezas.append(datos["published"])
    piezas += normalizar(datos["title"]).split()[:6]
    base = "-".join("-".join(p.split()) for p in piezas if p) or "fuente"
    base = re.sub(r"-+", "-", base).strip("-")[:80].rstrip("-")
    candidato, n = base, 2
    while candidato in tomados:
        candidato = f"{base}-{n}"
        n += 1
    return candidato


# --------------------------------------------------------------------------- #
# Localizadores
# --------------------------------------------------------------------------- #

def isbn13_valido(isbn: str) -> bool:
    if not ISBN13_RE.match(isbn or ""):
        return False
    suma = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(isbn[:12]))
    return (10 - suma % 10) % 10 == int(isbn[12])


def doi_valido(doi: str) -> bool:
    return bool(DOI_RE.match((doi or "").strip()))


def locator_canonico(entrada: dict) -> str | None:
    """Forma única que puede tener el localizador de esta entrada."""
    if entrada.get("isbn13"):
        return f"https://openlibrary.org/isbn/{entrada['isbn13']}"
    if entrada.get("doi"):
        return f"https://doi.org/{entrada['doi']}"
    return None


# --------------------------------------------------------------------------- #
# Lectura y escritura del registro
# --------------------------------------------------------------------------- #

ORDEN_CAMPOS = [
    "id", "type", "cita", "authors", "title", "published", "isbn13", "doi",
    "locator", "authority", "accessed", "used_in", "status", "nota", "resolucion",
]


def ordenar_entrada(entrada: dict) -> dict:
    ordenada = {k: entrada[k] for k in ORDEN_CAMPOS if k in entrada}
    ordenada.update({k: v for k, v in entrada.items() if k not in ordenada})
    return ordenada


def cargar_registro(ruta: Path = REGISTRO) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8"))


def guardar_registro(registro: dict, ruta: Path = REGISTRO) -> None:
    registro["entries"] = [ordenar_entrada(e) for e in registro["entries"]]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resumen(registro: dict) -> dict:
    """Las cifras que el README publica. Se calculan, no se escriben."""
    entradas = registro["entries"]
    verificadas = [e for e in entradas if e.get("status") == "verificada"]
    por_tipo: dict[str, int] = {}
    for entrada in verificadas:
        por_tipo[entrada["type"]] = por_tipo.get(entrada["type"], 0) + 1
    usos = usos_por_cita()
    citas = sum(len(rutas) for rutas in usos.values())
    en_clases = sum(1 for rutas in usos.values() for r in rutas if r.count("/") > 2)
    institucionales = sum(1 for e in entradas if es_institucional(e["cita"]))
    return {
        "academicas": len(entradas) - institucionales,
        "institucionales": institucionales,
        "citas_en_clases": en_clases,
        "obras": len(entradas),
        "verificadas": len(verificadas),
        "pendientes": len(entradas) - len(verificadas),
        "cobertura": round(100.0 * len(verificadas) / len(entradas), 1) if entradas else 0.0,
        "usadas": len(usos),
        "en_registro": sum(1 for cita in usos if cita in {e["cita"] for e in entradas}),
        "citas": citas,
        "libros": por_tipo.get("book", 0),
        "articulos": por_tipo.get("paper", 0),
        "normas": por_tipo.get("standard", 0),
    }
