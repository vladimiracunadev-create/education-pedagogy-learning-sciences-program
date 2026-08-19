#!/usr/bin/env python3
"""Genera el banco de actividades prácticas desde los manifiestos.

Produce:

  actividades/README.md            índice con los cuatro filtros del banco
  actividades/por-ciclo.md         actividades agrupadas por ciclo o edad
  actividades/por-asignatura.md    actividades agrupadas por asignatura
  actividades/por-contexto.md      actividades por modalidad y por contexto educativo
  actividades/<familia>.md         la ficha completa de cada actividad, por familia

Nada de esto se edita a mano: la fuente son manifests/pedagogia/actividades-*.json.
Usa solo la biblioteca estándar.

  python scripts/generar_actividades.py            regenera el banco
  python scripts/generar_actividades.py --check    falla si lo publicado difiere
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "manifests" / "pedagogia"
DESTINO = RAIZ / "actividades"

CICLOS = ["Parvularia", "Básica", "Media", "Técnico-profesional", "Adultos", "Superior"]


def slug(texto: str) -> str:
    plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", plano).strip("-").lower()


def cargar() -> list[dict]:
    actividades: list[dict] = []
    for archivo in sorted(MANIFIESTOS.glob("actividades-*.json")):
        actividades.extend(json.loads(archivo.read_text(encoding="utf-8")))
    actividades.sort(key=lambda a: a["id"])
    return actividades


def familias(actividades: list[dict]) -> dict[str, list[dict]]:
    agrupadas: dict[str, list[dict]] = defaultdict(list)
    for actividad in actividades:
        agrupadas[actividad["familia"]].append(actividad)
    return agrupadas


def ruta_de(familia: str) -> str:
    return f"{slug(familia)}.md"


def enlace(actividad: dict) -> str:
    destino = f"{ruta_de(actividad['familia'])}#{slug(actividad['id'] + ' ' + actividad['nombre'])}"
    return f"[{actividad['id']} · {actividad['nombre']}]({destino})"


def encabezado(titulo: str, bajada: str) -> list[str]:
    return [
        f"# {titulo}",
        "",
        bajada,
        "",
        "> Generado por `scripts/generar_actividades.py` desde `manifests/pedagogia/`. No editar a mano.",
        "",
    ]


def pie(volver: str = "README.md") -> list[str]:
    return [
        "",
        "---",
        "",
        f"[← Volver al banco de actividades]({volver}) · "
        "[Índice del programa](../SYLLABUS.md) · "
        "[Rutas por rol](../rutas/README.md)",
        "",
    ]


def construir_ficha(actividad: dict) -> list[str]:
    pasos = "\n".join(f"{i}. {paso}" for i, paso in enumerate(actividad["pasos"], 1))
    return [
        f"## {actividad['id']} · {actividad['nombre']}",
        "",
        f"**Para qué sirve.** {actividad['proposito']}",
        "",
        f"| Ciclo o edad | Asignaturas | Modalidad | Contexto | Duración | Agrupamiento |",
        "|---|---|---|---|---:|---|",
        f"| {' · '.join(actividad['ciclos'])} | {' · '.join(actividad['asignaturas'])} | "
        f"{' · '.join(actividad['modalidades'])} | {' · '.join(actividad['contextos'])} | "
        f"{actividad['duracion']} min | {actividad['agrupamiento']} |",
        "",
        "**Cómo se hace.**",
        "",
        pasos,
        "",
        f"**Con estudiantes menores.** {actividad['variante_menor']}",
        "",
        f"**Con estudiantes mayores.** {actividad['variante_mayor']}",
        "",
        f"**Adecuación para la diversidad.** {actividad['adecuacion']}",
        "",
        f"**Qué observar.** {actividad['senal']}",
        "",
        f"**Fundamento.** Clase {actividad['clase']:03d} del programa.",
        "",
    ]


def construir_familia(familia: str, actividades: list[dict]) -> str:
    lineas = encabezado(
        familia,
        f"**{len(actividades)} actividades.** Cada ficha declara para qué sirve, cómo se ejecuta, "
        "cómo se adapta por edad, qué adecuación exige la diversidad del curso y qué observar "
        "para saber si funcionó.",
    )
    for actividad in actividades:
        lineas.extend(construir_ficha(actividad))
    lineas.extend(pie())
    return "\n".join(lineas)


def construir_indice(actividades: list[dict], agrupadas: dict[str, list[dict]]) -> str:
    lineas = encabezado(
        "🧰 Banco de actividades prácticas",
        f"**{len(actividades)} actividades de aula**, listas para usar y adaptables a distintas "
        "edades, asignaturas, modalidades y contextos educativos. Cada una declara su fundamento "
        "en una clase del programa: ninguna es una idea suelta.",
    )
    lineas += [
        "## Cómo se usa este banco",
        "",
        "1. **Parte por el problema, no por la actividad.** Identifica qué falla —conocimiento previo "
        "no comprobado, práctica insuficiente, clima deteriorado— y busca en esa familia.",
        "2. **Verifica el contexto.** Cada ficha declara en qué contextos funciona: aula numerosa, "
        "multigrado, baja conectividad, alta diversidad lingüística.",
        "3. **Ajusta por edad con la variante indicada**, no improvisando.",
        "4. **Aplica la adecuación declarada.** Está escrita para que ningún estudiante quede fuera.",
        "5. **Observa la señal.** Cada actividad indica qué mirar para saber si sirvió.",
        "",
        "## Índice por familia",
        "",
        "| Familia | Actividades | Para qué sirve |",
        "|---|---:|---|",
    ]
    proposito_familia = {
        "Activación y conocimiento previo": "comprobar qué saben antes de enseñar",
        "Comprensión y procesamiento": "hacer visible el razonamiento y construir significado",
        "Práctica y consolidación": "convertir lo comprendido en aprendizaje disponible",
        "Colaboración y discusión": "trabajar entre pares con responsabilidad real",
        "Evaluación formativa y retroalimentación": "obtener evidencia y devolverla a tiempo",
        "Convivencia, motivación y clima": "sostener las condiciones que hacen posible enseñar",
    }
    for familia, lista in agrupadas.items():
        lineas.append(
            f"| **[{familia}]({ruta_de(familia)})** | {len(lista)} | "
            f"{proposito_familia.get(familia, '')} |"
        )
    lineas += [
        "",
        "## Otras entradas al banco",
        "",
        "- 👶 **[Por ciclo y edad](por-ciclo.md)** — de parvularia a educación superior.",
        "- 📚 **[Por asignatura](por-asignatura.md)** — qué sirve para lenguaje, matemática, ciencias o taller.",
        "- 🏫 **[Por modalidad y contexto](por-contexto.md)** — aula numerosa, multigrado, rural, "
        "baja conectividad, alta diversidad lingüística o presencial, híbrida y en línea.",
        "",
        "## Todas las actividades",
        "",
        "| Código | Actividad | Familia | Ciclos | Duración |",
        "|---|---|---|---|---:|",
    ]
    for actividad in actividades:
        lineas.append(
            f"| `{actividad['id']}` | {enlace(actividad)} | {actividad['familia']} | "
            f"{' · '.join(actividad['ciclos'])} | {actividad['duracion']} min |"
        )
    lineas += [
        "",
        "---",
        "",
        "Las actividades no reemplazan la decisión pedagógica: la ejecutan. Elegir cuál usar exige "
        "el diagnóstico que enseñan las partes del programa, y cada ficha remite a la clase que la "
        "fundamenta.",
        "",
        "[Índice del programa](../SYLLABUS.md) · [Rutas por rol](../rutas/README.md) · "
        "[Plantillas](../templates/README.md)",
        "",
    ]
    return "\n".join(lineas)


def construir_agrupado(titulo: str, bajada: str, grupos: dict[str, list[dict]]) -> str:
    lineas = encabezado(titulo, bajada)
    for clave, lista in grupos.items():
        if not lista:
            continue
        lineas += [f"## {clave}", "", f"*{len(lista)} actividades.*", "", "| Código | Actividad | Duración | Agrupamiento |", "|---|---|---:|---|"]
        for actividad in sorted(lista, key=lambda a: a["id"]):
            lineas.append(
                f"| `{actividad['id']}` | {enlace(actividad)} | {actividad['duracion']} min | "
                f"{actividad['agrupamiento']} |"
            )
        lineas.append("")
    lineas.extend(pie())
    return "\n".join(lineas)


def agrupar_por(actividades: list[dict], campo: str, orden: list[str] | None = None) -> dict[str, list[dict]]:
    grupos: dict[str, list[dict]] = defaultdict(list)
    for actividad in actividades:
        for valor in actividad[campo]:
            grupos[valor].append(actividad)
    if orden:
        return {clave: grupos[clave] for clave in orden if clave in grupos}
    return dict(sorted(grupos.items()))


def construir_todo() -> dict[Path, str]:
    actividades = cargar()
    agrupadas = familias(actividades)
    archivos: dict[Path, str] = {DESTINO / "README.md": construir_indice(actividades, agrupadas)}
    for familia, lista in agrupadas.items():
        archivos[DESTINO / ruta_de(familia)] = construir_familia(familia, lista)

    por_ciclo = agrupar_por(actividades, "ciclos", CICLOS)
    archivos[DESTINO / "por-ciclo.md"] = construir_agrupado(
        "👶 Actividades por ciclo y edad",
        "La misma actividad rinde distinto según la edad. Cada ficha trae su variante para "
        "estudiantes menores y mayores; aquí están agrupadas por el ciclo donde se aplican.",
        por_ciclo,
    )

    archivos[DESTINO / "por-asignatura.md"] = construir_agrupado(
        "📚 Actividades por asignatura",
        "Las actividades marcadas como transversales sirven en cualquier asignatura; el resto "
        "declara el campo donde tiene sentido aplicarlas.",
        agrupar_por(actividades, "asignaturas"),
    )

    contexto = agrupar_por(actividades, "modalidades")
    contexto.update(agrupar_por(actividades, "contextos"))
    archivos[DESTINO / "por-contexto.md"] = construir_agrupado(
        "🏫 Actividades por modalidad y contexto",
        "Una actividad viable en un aula de veinte estudiantes con conectividad puede ser "
        "impracticable en un multigrado rural. Estas listas declaran dónde cada una funciona.",
        contexto,
    )
    return archivos


def main() -> int:
    solo_verificar = "--check" in sys.argv
    archivos = construir_todo()
    if solo_verificar:
        diferencias = [
            ruta.relative_to(RAIZ).as_posix()
            for ruta, contenido in archivos.items()
            if not ruta.exists() or ruta.read_text(encoding="utf-8") != contenido
        ]
        if diferencias:
            print("ERROR: el banco de actividades está desactualizado:")
            for ruta in diferencias:
                print(f"  - {ruta}")
            print("Ejecuta: python scripts/generar_actividades.py")
            return 1
        print(f"OK: el banco de {len(archivos)} archivos está al día.")
        return 0

    DESTINO.mkdir(parents=True, exist_ok=True)
    for ruta, contenido in archivos.items():
        ruta.write_text(contenido, encoding="utf-8")
    total = sum(len(json.loads(a.read_text(encoding="utf-8"))) for a in MANIFIESTOS.glob("actividades-*.json"))
    print(f"OK: {total} actividades en {len(archivos)} archivos de actividades/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
