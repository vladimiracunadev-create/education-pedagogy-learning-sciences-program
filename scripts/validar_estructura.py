#!/usr/bin/env python3
"""Validación estricta del repositorio.

Comprueba lo que el README afirma: número de partes y de clases, secciones
obligatorias de cada página, enlaces internos que existen, y coherencia entre
los manifiestos y el árbol publicado. Es la validación que corre en CI.

Uso:
  python scripts/validar_estructura.py
  python scripts/validar_estructura.py --resumen   # además imprime métricas
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CURRICULO = RAIZ / "curriculum"
MANIFIESTOS = RAIZ / "manifests"

PARTES_ESPERADAS = 25
CLASES_ESPERADAS = 300
CLASES_POR_PARTE = 12

# Estándar `clase-profunda`: por debajo de este umbral la clase perdió alguna de sus
# secciones o quedó reducida a un esquema. El CI lo comprueba en cada push.
MINIMO_PALABRAS_CLASE = 2500

SECCIONES_CLASE = [
    "## 🎯 Propósito",
    "## 📚 Resultados de aprendizaje",
    "## 🧭 Agenda sugerida",
    "## 🧩 Conceptos centrales",
    "## 🧠 Modelo mental",
    "## 🗺️ Flujo de razonamiento",
    "## 📖 Desarrollo",
    "## 📚 Lectura comparada",
    "## 🧮 Ejemplo trabajado",
    "## 🔀 Comparación de caminos y límites",
    "## 🪜 El mismo tema según el rol",
    "## 🧪 Taller guiado",
    "## 🏫 Caso profesional",
    "## 📥 Evidencia de aprendizaje",
    "## 🏆 Reto verificable",
    "## ✅ Evaluación de la clase",
    "## ⚠️ Errores frecuentes",
    "## ♿ Diversidad, accesibilidad y ética",
    "## 🇨🇱 Contexto chileno y cumplimiento",
    "## ❓ Preguntas de comprobación",
    "## 📗 Fuentes y verificación",
    "## 🔗 Conexión con el resto del programa",
]

SECCIONES_PARTE = [
    "## 🎯 De qué trata esta parte",
    "## 🏫 Caso de la parte",
    "## 📚 Resultados de la parte",
    "## 🗺️ Mapa de la parte",
    "## 🧠 Marco de referencia",
    "## 📋 Las 12 clases",
    "## ⚠️ Riesgos característicos",
    "## 📕 Lecturas de referencia de la parte",
    "## ✅ Evidencia mínima para dar la parte por cerrada",
    "## 🧭 Práctica y evaluación",
]

ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

SECCIONES_ROL = [
    "## 🧭 Qué es y por qué importa",
    "## 🗓️ Un día en el puesto",
    "## 🧠 Qué necesitas saber",
    "## 📚 Tu ruta en el programa",
    "## 📈 Progresión",
    "## ⚠️ Mitos y errores comunes",
    "## 🚀 Siguientes pasos",
]


def error(mensajes: list[str], texto: str) -> None:
    mensajes.append(texto)


def validar_conteos(fallos: list[str]) -> tuple[list[Path], list[Path]]:
    partes = sorted(p for p in CURRICULO.glob("part-*") if p.is_dir())
    clases = sorted(CURRICULO.glob("part-*/class-*/README.md"))
    if len(partes) != PARTES_ESPERADAS:
        error(fallos, f"se esperaban {PARTES_ESPERADAS} partes y hay {len(partes)}")
    if len(clases) != CLASES_ESPERADAS:
        error(fallos, f"se esperaban {CLASES_ESPERADAS} clases y hay {len(clases)}")
    for parte in partes:
        propias = list(parte.glob("class-*/README.md"))
        if len(propias) != CLASES_POR_PARTE:
            error(fallos, f"{parte.name} tiene {len(propias)} clases y debería tener {CLASES_POR_PARTE}")
        if not (parte / "README.md").exists():
            error(fallos, f"{parte.name} no tiene README.md")
    return partes, clases


def validar_secciones(fallos: list[str], partes: list[Path], clases: list[Path]) -> None:
    for clase in clases:
        texto = clase.read_text(encoding="utf-8")
        relativo = clase.relative_to(RAIZ).as_posix()
        for seccion in SECCIONES_CLASE:
            if seccion not in texto:
                error(fallos, f"{relativo}: falta la sección «{seccion}»")
        if "```mermaid" not in texto:
            error(fallos, f"{relativo}: no contiene diagrama mermaid")
        if not re.search(r"^# Clase \d{3} — .+$", texto, re.M):
            error(fallos, f"{relativo}: el título no sigue el formato «# Clase NNN — …»")
        if len(texto.split()) < MINIMO_PALABRAS_CLASE:
            error(fallos, f"{relativo}: tiene {len(texto.split())} palabras y el estándar "
                          f"exige {MINIMO_PALABRAS_CLASE}")
    for parte in partes:
        texto = (parte / "README.md").read_text(encoding="utf-8")
        for seccion in SECCIONES_PARTE:
            if seccion not in texto:
                error(fallos, f"{parte.name}/README.md: falta la sección «{seccion}»")


def validar_rutas_por_rol(fallos: list[str]) -> int:
    """Cada guía de rol debe estar completa y enlazada desde el índice de rutas."""
    carpeta = RAIZ / "rutas"
    if not carpeta.exists():
        error(fallos, "falta la carpeta rutas/ con las guías por rol")
        return 0

    indice = (carpeta / "README.md")
    if not indice.exists():
        error(fallos, "rutas/README.md no existe")
        return 0
    texto_indice = indice.read_text(encoding="utf-8")

    guias = sorted(p for p in carpeta.glob("*.md") if p.name != "README.md")
    if len(guias) < 10:
        error(fallos, f"se esperaban al menos 10 guías de rol y hay {len(guias)}")

    for guia in guias:
        texto = guia.read_text(encoding="utf-8")
        relativo = guia.relative_to(RAIZ).as_posix()
        for seccion in SECCIONES_ROL:
            if seccion not in texto:
                error(fallos, f"{relativo}: falta la sección «{seccion}»")
        if guia.name not in texto_indice:
            error(fallos, f"{relativo}: no está enlazada desde rutas/README.md")
        if len(texto.split()) < 700:
            error(fallos, f"{relativo}: tiene menos de 700 palabras")
        if "Volver al índice de rutas" not in texto:
            error(fallos, f"{relativo}: falta la navegación de retorno al índice")
    return len(guias)


def validar_enlaces(fallos: list[str]) -> int:
    """Comprueba que todo enlace relativo del repositorio apunte a algo existente."""
    comprobados = 0
    carpetas = (
        "curriculum/**", "docs", "rutas", "actividades",
        "templates", "projects", "cases", "assessments",
    )
    documentos = list(RAIZ.glob("*.md"))
    for carpeta in carpetas:
        documentos += sorted(RAIZ.glob(f"{carpeta}/*.md"))
    for documento in documentos:
        texto = documento.read_text(encoding="utf-8")
        for destino in ENLACE.findall(texto):
            if destino.startswith(("http://", "https://", "mailto:", "#")):
                continue
            objetivo = (documento.parent / destino.partition("#")[0]).resolve()
            comprobados += 1
            if not objetivo.exists():
                error(fallos, f"{documento.relative_to(RAIZ).as_posix()}: enlace roto → {destino}")
    return comprobados


def validar_manifiestos(fallos: list[str]) -> None:
    curriculo = json.loads((MANIFIESTOS / "curriculum.json").read_text(encoding="utf-8"))
    numeros = [c["global_class"] for c in curriculo]
    if numeros != list(range(1, CLASES_ESPERADAS + 1)):
        error(fallos, f"la numeración global de curriculum.json no es correlativa de 1 a {CLASES_ESPERADAS}")

    datos: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            datos[registro["n"]] = registro

    niveles = set(json.loads((MANIFIESTOS / "pedagogia" / "marco.json")
                             .read_text(encoding="utf-8"))["niveles_evidencia"])
    obligatorios = {"n", "evidencia", "foco", "proposito", "decision", "entregable", "conceptos",
                    "desarrollo", "practica", "limites", "errores", "criterios", "preguntas",
                    "lecturas", "inclusion", "reto", "conexion"}
    for numero, registro in datos.items():
        faltan = obligatorios - set(registro)
        if faltan:
            error(fallos, f"clase {numero}: faltan campos {sorted(faltan)}")
        if registro.get("evidencia") not in niveles:
            error(fallos, f"clase {numero}: estado de evidencia desconocido «{registro.get('evidencia')}»")
        if len(registro.get("conceptos", [])) != 4:
            error(fallos, f"clase {numero}: debe declarar exactamente 4 conceptos")
        if len(registro.get("lecturas", [])) < 2:
            error(fallos, f"clase {numero}: debe declarar al menos 2 lecturas")

    # Dos títulos se repiten entre partes a propósito —«Desarrollo socioemocional» en
    # parvularia y en desarrollo humano, «Evaluación auténtica» en media y en psicometría—
    # porque tratan lo mismo a distinta profundidad. Lo que no puede repetirse es un título
    # dentro de una misma parte: ahí sería contenido duplicado.
    for parte in {c["part"] for c in curriculo}:
        titulos = [c["title"] for c in curriculo if c["part"] == parte]
        if len(set(titulos)) != len(titulos):
            repetidos = sorted({t for t in titulos if titulos.count(t) > 1})
            error(fallos, f"parte {parte:02d}: títulos duplicados dentro de la parte: {repetidos}")


def metricas() -> dict[str, int]:
    clases = sorted(CURRICULO.glob("part-*/class-*/README.md"))
    textos = [c.read_text(encoding="utf-8") for c in clases]
    conceptos = sum(len(json.loads(a.read_text(encoding="utf-8"))) * 4
                    for a in (MANIFIESTOS / "classes").glob("*.json"))
    lecturas = sum(len(r["lecturas"])
                   for a in (MANIFIESTOS / "classes").glob("*.json")
                   for r in json.loads(a.read_text(encoding="utf-8")))
    return {
        "partes": len(list(CURRICULO.glob("part-*"))),
        "clases": len(clases),
        "palabras": sum(len(t.split()) for t in textos),
        "conceptos": conceptos,
        "preguntas": len(clases) * 3,
        "lecturas": lecturas,
        "diagramas": sum(t.count("```mermaid") for t in textos)
                     + sum((p / "README.md").read_text(encoding="utf-8").count("```mermaid")
                           for p in CURRICULO.glob("part-*")),
        "documentos": len(list(RAIZ.glob("docs/*.md"))),
        "guias_de_rol": len([p for p in RAIZ.glob("rutas/*.md") if p.name != "README.md"]),
    }


# Marcas de fuente institucional o normativa: útiles y necesarias, pero no
# sustituyen a un libro o a un artículo cuando la clase afirma algo sobre
# cómo se aprende o cómo se enseña.
INSTITUCIONALES = (
    "mineduc", "ministerio", "biblioteca del congreso", "agencia de calidad",
    "superintendencia", "ocde", "unesco", "unicef", "organización", "organizacion",
    "comisión europea", "comision europea", "banco mundial", "foro económico",
    "education endowment", "casel", "cast", "ley ", "decreto ", "convención",
    "convencion", "national autism", "programa de educación", "sistema de créditos",
    "sistema de creditos", "normativa", "informe belmont", "declaration on research",
    "tuning", "aera", "who", "oit", "unevoc", "w3c", "aaidd", "comisión nacional",
    "comision nacional", "subsecretaría", "subsecretaria", "center on the developing",
    "international center for academic", "committee on publication", "what works clearinghouse",
)

# Una fuente sirve para volver a ella. Se exige año de publicación o, para los
# documentos vivos, la marca explícita de que se cita la versión en curso.
ANIO = re.compile(r"\((?:\d{4}[a-z]?|eds?\.,? ?\d{4}|edición vigente|version vigente)\)")
VIGENTE = "edición vigente"


def es_institucional(cita: str) -> bool:
    minuscula = cita.strip().lower()
    return any(minuscula.startswith(marca) for marca in INSTITUCIONALES)


def validar_fuentes(fallos: list[str]) -> int:
    """Cada clase debe declarar fuentes identificables y volver a ellas debe ser posible.

    Tres reglas, en orden de importancia:

    1. toda cita permite localizar la obra: tiene año o declara versión vigente;
    2. ninguna clase se apoya solo en documentos institucionales: al menos un
       libro o artículo respalda lo que la clase afirma;
    3. toda obra citada aparece en el índice generado de obras citadas.
    """
    citas = 0
    indice = (RAIZ / "docs" / "OBRAS_CITADAS.md")
    texto_indice = indice.read_text(encoding="utf-8") if indice.exists() else ""
    if not texto_indice:
        error(fallos, "falta docs/OBRAS_CITADAS.md: ejecuta scripts/generar_indice.py")

    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            numero = registro["n"]
            lecturas = registro.get("lecturas", [])
            if not 2 <= len(lecturas) <= 3:
                error(fallos, f"clase {numero:03d}: cita {len(lecturas)} obras y debe citar 2 o 3")
            academicas = 0
            for cita, lente in lecturas:
                citas += 1
                cita = cita.strip()
                if not ANIO.search(cita):
                    error(fallos, f"clase {numero:03d}: cita sin año ni «{VIGENTE}» → {cita[:70]}")
                if len(lente.strip()) < 25:
                    error(fallos, f"clase {numero:03d}: el lente de «{cita[:40]}» no explica qué aporta")
                if not es_institucional(cita):
                    academicas += 1
                if texto_indice and cita.rstrip(".") not in texto_indice:
                    error(fallos, f"clase {numero:03d}: obra ausente del índice → {cita[:60]}")
            if lecturas and academicas == 0:
                error(
                    fallos,
                    f"clase {numero:03d}: se apoya solo en fuentes institucionales; "
                    "falta un libro o artículo",
                )
    return citas


# Piso de profundidad por campo del manifiesto. No mide calidad —eso lo revisa
# una persona— pero impide que una clase se degrade a ficha: cada campo debe
# desarrollar su idea, no enunciarla.
PISO = {"desarrollo": 62, "practica": 55, "limites": 45, "inclusion": 28}
PISO_CONCEPTO = 10


def validar_profundidad(fallos: list[str]) -> None:
    """Cada clase explica lo que afirma: desarrollo, práctica, límites e inclusión."""
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            numero = registro["n"]
            for campo, minimo in PISO.items():
                palabras = len(registro[campo].split())
                if palabras < minimo:
                    error(
                        fallos,
                        f"clase {numero:03d}: «{campo}» tiene {palabras} palabras y el piso es {minimo}",
                    )
            for termino, definicion in registro["conceptos"]:
                if len(definicion.split()) < PISO_CONCEPTO:
                    error(
                        fallos,
                        f"clase {numero:03d}: la definición de «{termino}» es demasiado breve "
                        f"({len(definicion.split())} palabras, piso {PISO_CONCEPTO})",
                    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resumen", action="store_true", help="imprime métricas del repositorio")
    args = parser.parse_args()

    if not CURRICULO.exists():
        print("FALLÓ: no existe curriculum/. Ejecuta python scripts/generar_clases.py")
        return 1

    fallos: list[str] = []
    partes, clases = validar_conteos(fallos)
    validar_secciones(fallos, partes, clases)
    guias = validar_rutas_por_rol(fallos)
    enlaces = validar_enlaces(fallos)
    validar_manifiestos(fallos)
    citas = validar_fuentes(fallos)
    validar_profundidad(fallos)

    if fallos:
        print(f"FALLÓ: {len(fallos)} problema(s) de estructura.")
        for fallo in fallos[:40]:
            print(f"  - {fallo}")
        if len(fallos) > 40:
            print(f"  … y {len(fallos) - 40} más.")
        return 1

    print(f"OK: {len(partes)} partes, {len(clases)} clases, {guias} guías de rol, "
          f"{citas} citas con fuente, {enlaces} enlaces internos verificados.")
    if args.resumen:
        for clave, valor in metricas().items():
            print(f"  {clave}: {valor:,}".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
