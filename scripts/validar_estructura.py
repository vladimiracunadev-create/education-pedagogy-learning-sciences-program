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

PARTES_ESPERADAS = 18
CLASES_ESPERADAS = 216
CLASES_POR_PARTE = 12

SECCIONES_CLASE = [
    "## 🎯 Propósito",
    "## 📚 Resultados de aprendizaje",
    "## 🧩 Conceptos centrales",
    "## 🗺️ Flujo de razonamiento",
    "## 📖 Desarrollo",
    "## 🧪 Taller guiado",
    "## 🏆 Reto verificable",
    "## ✅ Criterio de logro",
    "## ⚠️ Errores frecuentes",
    "## ♿ Diversidad, accesibilidad y ética",
    "## ❓ Preguntas de comprobación",
    "## 📕 Lecturas base",
    "## 🔗 Conexión con el resto del programa",
]

SECCIONES_PARTE = [
    "## 🎯 De qué trata esta parte",
    "## 📚 Resultados de la parte",
    "## 🗺️ Mapa de la parte",
    "## 🧠 Marco de referencia",
    "## 📋 Las 12 clases",
    "## ⚠️ Riesgos característicos",
    "## 📕 Lecturas de referencia de la parte",
    "## ✅ Evidencia mínima para dar la parte por cerrada",
]

ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


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
        if len(texto.split()) < 900:
            error(fallos, f"{relativo}: tiene menos de 900 palabras")
    for parte in partes:
        texto = (parte / "README.md").read_text(encoding="utf-8")
        for seccion in SECCIONES_PARTE:
            if seccion not in texto:
                error(fallos, f"{parte.name}/README.md: falta la sección «{seccion}»")


def validar_enlaces(fallos: list[str]) -> int:
    """Comprueba que todo enlace relativo del repositorio apunte a algo existente."""
    comprobados = 0
    for documento in list(RAIZ.glob("*.md")) + sorted(RAIZ.glob("curriculum/**/*.md")) \
            + sorted(RAIZ.glob("docs/*.md")):
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
        error(fallos, "la numeración global de curriculum.json no es correlativa de 1 a 216")

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
    }


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
    enlaces = validar_enlaces(fallos)
    validar_manifiestos(fallos)

    if fallos:
        print(f"FALLÓ: {len(fallos)} problema(s) de estructura.")
        for fallo in fallos[:40]:
            print(f"  - {fallo}")
        if len(fallos) > 40:
            print(f"  … y {len(fallos) - 40} más.")
        return 1

    print(f"OK: {len(partes)} partes, {len(clases)} clases, {enlaces} enlaces internos verificados.")
    if args.resumen:
        for clave, valor in metricas().items():
            print(f"  {clave}: {valor:,}".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
