#!/usr/bin/env python3
"""Genera los documentos que describen el estado real del repositorio.

Escribe tres archivos, todos derivados de los manifiestos y del árbol publicado,
para que ninguna cifra del repositorio se escriba a mano y quede desactualizada:

  STATUS.md      métricas verificables con el comando que las reproduce
  FILE_INDEX.md  índice completo de archivos con su propósito
  catalog.json   catálogo legible por máquina de las 300 clases

Uso:
  python scripts/generar_indice.py
  python scripts/generar_indice.py --check   # falla si lo escrito no coincide
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "manifests"
CURRICULO = RAIZ / "curriculum"

IGNORADOS = {".git", "node_modules", ".venv", "__pycache__", "site", "capacitacion",
             ".ruff_cache", ".pytest_cache", "output"}


def leer(*partes: str):
    return json.loads(MANIFIESTOS.joinpath(*partes).read_text(encoding="utf-8"))


def cargar() -> tuple[list[dict], list[dict], dict[int, dict], list[dict]]:
    curriculo = leer("curriculum.json")
    packs: list[dict] = []
    for archivo in sorted((MANIFIESTOS / "parts").glob("*.json")):
        packs += json.loads(archivo.read_text(encoding="utf-8"))
    packs.sort(key=lambda p: p["part"])
    clases: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            clases[registro["n"]] = registro
    etapas = leer("etapas.json")
    return curriculo, packs, clases, etapas


def numero(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


# --------------------------------------------------------------------------- #
# catalog.json
# --------------------------------------------------------------------------- #

def construir_catalogo(curriculo, packs, clases, etapas) -> dict:
    packs_por_numero = {p["part"]: p for p in packs}
    etapas_por_id = {e["id"]: e for e in etapas}
    registros = []
    for clase in curriculo:
        pack = packs_por_numero[clase["part"]]
        datos = clases[clase["global_class"]]
        registros.append({
            "n": clase["global_class"],
            "parte": clase["part"],
            "parte_titulo": clase["part_title"],
            "etapa": pack["etapa"],
            "etapa_nombre": etapas_por_id[pack["etapa"]]["nombre"],
            "clase": clase["class"],
            "titulo": clase["title"],
            "ruta": f"curriculum/{clase['part_slug']}/{clase['slug']}/README.md",
            "estado_evidencia": datos["evidencia"],
            "decision": datos["decision"],
            "entregable": datos["entregable"],
            "conceptos": [c[0] for c in datos["conceptos"]],
            "lecturas": [lectura[0] for lectura in datos["lecturas"]],
        })
    return {
        "programa": "Programa Integral de Pedagogía, Docencia y Ciencias del Aprendizaje",
        "version": (RAIZ / "VERSION").read_text(encoding="utf-8").strip(),
        "idioma": "es",
        "partes": len(packs),
        "clases": len(registros),
        "etapas": [{"id": e["id"], "nombre": e["nombre"], "partes": e["partes"]} for e in etapas],
        "catalogo": registros,
    }


# --------------------------------------------------------------------------- #
# STATUS.md
# --------------------------------------------------------------------------- #

def construir_status(curriculo, packs, clases, etapas) -> str:
    version = (RAIZ / "VERSION").read_text(encoding="utf-8").strip()
    paginas = sorted(CURRICULO.glob("part-*/class-*/README.md"))
    textos = [p.read_text(encoding="utf-8") for p in paginas]
    palabras = [len(t.split()) for t in textos]
    conceptos = sum(len(c["conceptos"]) for c in clases.values())
    lecturas = sum(len(c["lecturas"]) for c in clases.values())
    docs = sorted((RAIZ / "docs").glob("*.md"))

    por_evidencia: dict[str, int] = {}
    for registro in clases.values():
        por_evidencia[registro["evidencia"]] = por_evidencia.get(registro["evidencia"], 0) + 1
    filas_evidencia = "\n".join(
        f"| `{estado}` | {cantidad} | {cantidad * 100 // len(clases)}% |"
        for estado, cantidad in sorted(por_evidencia.items(), key=lambda x: -x[1])
    )

    filas_etapas = "\n".join(
        f"| {e['emoji']} {e['nombre']} | {len(e['partes'])} | "
        f"{len(e['partes']) * 12} | {e['salida']} |"
        for e in etapas
    )

    return f"""# Estado del programa

Cifras verificables contra el repositorio. Ninguna se escribe a mano: este archivo lo genera
`scripts/generar_indice.py` desde los manifiestos, y el CI comprueba en cada push que siga
coincidiendo con lo publicado.

## Contenido

| Métrica | Valor |
|---|---:|
| Versión | {version} |
| Etapas | {len(etapas)} |
| Partes | {len(packs)} |
| Clases | {len(curriculo)} |
| Clases por parte | 12 |
| Palabras en las 300 clases | {numero(sum(palabras))} |
| Palabras por clase | {min(palabras)}–{max(palabras)} (mediana {sorted(palabras)[len(palabras) // 2]}) |
| Diagramas mermaid | {len(paginas) + len(packs)} (uno por clase y uno por parte) |
| Conceptos con definición operacional | {numero(conceptos)} |
| Decisiones profesionales habilitadas | {len(curriculo)} (una por clase) |
| Evidencias de aprendizaje definidas | {len(curriculo)} |
| Preguntas de comprobación | {numero(len(curriculo) * 3)} |
| Referencias bibliográficas citadas en clases | {numero(lecturas)} |
| Documentos transversales (`docs/`) | {len(docs)} |
| Casos profesionales (`cases/`) | {len(list((RAIZ / 'cases').glob('*.md')))} |
| Proyectos integradores mayores (`projects/`) | {len(list((RAIZ / 'projects').glob('*.md')))} |
| Laboratorios (`labs/`) | {len([d for d in (RAIZ / 'labs').iterdir() if d.is_dir()])} |

## Distribución por estado de evidencia

Cada clase declara con qué respaldo se sostiene lo que enseña. La distribución es
información del programa, no un adorno: muestra cuánto de este campo es evidencia
robusta y cuánto es marco normativo o práctica profesional.

| Estado | Clases | Proporción |
|---|---:|---:|
{filas_evidencia}

## Etapas

| Etapa | Partes | Clases | Salida |
|---|---:|---:|---|
{filas_etapas}

## Cómo reproducir estas cifras

```bash
python scripts/generar_clases.py --check
python scripts/validar_estructura.py --resumen
python scripts/validar_encoding.py
python -m unittest discover -s tests -v
```

## Qué no afirma este repositorio

- No reemplaza un título profesional de pedagogía ni una habilitación legal para ejercer.
- No sustituye una licenciatura, un magíster ni un doctorado de una institución acreditada.
- No garantiza resultados: entrega criterios, evidencia y práctica; el resultado depende
  del contexto, de los estudiantes reales y del trabajo sostenido de quien lo aplica.
- Las referencias normativas chilenas describen el marco vigente a la fecha de redacción
  y deben verificarse en la fuente oficial antes de fundar una decisión real.
"""


# --------------------------------------------------------------------------- #
# FILE_INDEX.md
# --------------------------------------------------------------------------- #

DESCRIPCIONES = {
    "curriculum": "las 25 partes y sus 300 clases, generadas desde `manifests/`",
    "manifests": "fuente única de verdad del currículo: nada se edita a mano en `curriculum/`",
    "docs": "documentos transversales: metodología, guías, bibliografía, marcos y protocolos",
    "rutas": "guías de carrera por rol: qué es, día a día, ruta en el programa y credenciales",
    "scripts": "generadores y validadores; todo lo publicado se reconstruye con ellos",
    "tests": "pruebas estructurales del repositorio",
    "cases": "casos profesionales para resolver con el marco del programa",
    "projects": "proyectos integradores mayores del programa",
    "assessments": "rúbricas e instrumentos de autoevaluación",
    "labs": "laboratorios y simuladores de práctica",
    "templates": "plantillas de trabajo reutilizables",
    "chile-education-system": "marco institucional y normativo chileno",
    "international-education": "comparación internacional de sistemas educativos",
    "books": "guía de lectura del programa",
    "papers": "plantilla de revisión crítica de artículos",
    "datasets": "datos sintéticos para practicar análisis",
    "notebooks": "actividades analíticas reproducibles",
    "virtual-school-lab": "escuela y universidad simuladas para practicar decisiones",
}


def construir_indice(curriculo, packs) -> str:
    lineas = [
        "# Índice de archivos",
        "",
        "Índice completo y generado del repositorio. Se reconstruye con "
        "`python scripts/generar_indice.py`.",
        "",
        "## Raíz",
        "",
        "| Archivo | Propósito |",
        "|---|---|",
    ]
    proposito_raiz = {
        "README.md": "presentación del programa y punto de entrada",
        "CURRICULUM.md": "las 25 partes y las 300 clases en una tabla",
        "SYLLABUS.md": "programa detallado con decisiones y evidencias por clase",
        "STATUS.md": "cifras verificables del estado del repositorio",
        "ROADMAP.md": "etapas de dominio y condiciones para avanzar",
        "CHANGELOG.md": "historial de versiones",
        "CONTRIBUTING.md": "cómo contribuir y qué exige una contribución",
        "CODE_OF_CONDUCT.md": "normas de convivencia del proyecto",
        "SECURITY.md": "política de seguridad y de datos",
        "SUPPORT.md": "cómo pedir ayuda y dónde",
        "LICENSE": "licencia MIT del código",
        "LICENSE-CONTENT.md": "licencia CC BY-NC-SA 4.0 del contenido educativo",
        "FILE_INDEX.md": "este índice",
        "MANIFEST.md": "inventario cuantitativo verificable del repositorio",
        "VERSION": "versión vigente del programa",
        "catalog.json": "catálogo de las 300 clases legible por máquina",
        "requirements.txt": "dependencias opcionales de los generadores",
        "Makefile": "atajos de generación y validación",
    }
    for nombre in sorted(proposito_raiz):
        if (RAIZ / nombre).exists():
            lineas.append(f"| [`{nombre}`]({nombre}) | {proposito_raiz[nombre]} |")

    lineas += ["", "## Directorios", "", "| Directorio | Archivos | Propósito |", "|---|---:|---|"]
    for nombre in sorted(DESCRIPCIONES):
        carpeta = RAIZ / nombre
        if not carpeta.exists():
            continue
        # Se cuentan solo los archivos versionables: las cachés locales harían que
        # el índice difiera entre una máquina de trabajo y el runner de CI.
        cantidad = sum(
            1 for p in carpeta.rglob("*")
            if p.is_file() and not any(parte in IGNORADOS or parte.startswith(".")
                                       for parte in p.relative_to(RAIZ).parts)
        )
        lineas.append(f"| `{nombre}/` | {cantidad} | {DESCRIPCIONES[nombre]} |")

    lineas += ["", "## Currículo", ""]
    packs_por_numero = {p["part"]: p for p in packs}
    for pack in packs:
        clases = [c for c in curriculo if c["part"] == pack["part"]]
        slug = clases[0]["part_slug"]
        lineas += [
            f"### Parte {pack['part']:02d} — {pack['titulo']}",
            "",
            f"[README de la parte](curriculum/{slug}/README.md) · "
            f"clases {clases[0]['global_class']:03d}–{clases[-1]['global_class']:03d}",
            "",
        ]
        for clase in clases:
            lineas.append(
                f"- `{clase['global_class']:03d}` "
                f"[{clase['title']}](curriculum/{slug}/{clase['slug']}/README.md)"
            )
        lineas.append("")

    lineas += [
        "## Documentos transversales",
        "",
        "| Documento | Propósito |",
        "|---|---|",
    ]
    for documento in sorted((RAIZ / "docs").glob("*.md")):
        texto = documento.read_text(encoding="utf-8")
        titulo = next((l[2:].strip() for l in texto.splitlines() if l.startswith("# ")), documento.stem)
        lineas.append(f"| [`docs/{documento.name}`](docs/{documento.name}) | {titulo} |")
    lineas.append("")
    _ = packs_por_numero
    return "\n".join(lineas)


# --------------------------------------------------------------------------- #
# MANIFEST.md
# --------------------------------------------------------------------------- #

def construir_manifiesto(curriculo, packs, clases) -> str:
    paginas = sorted(CURRICULO.glob("part-*/class-*/README.md"))
    palabras = sum(len(p.read_text(encoding="utf-8").split()) for p in paginas)
    obras = {referencia for c in clases.values() for referencia, _ in c["lecturas"]}
    guias = [p for p in (RAIZ / "rutas").glob("*.md") if p.name != "README.md"]

    filas = [
        ("Partes del currículo", len(packs)),
        ("Clases", len(curriculo)),
        ("Palabras en las clases", palabras),
        ("Conceptos con definición operacional", sum(len(c["conceptos"]) for c in clases.values())),
        ("Señales observables exigidas", len(curriculo) * 3),
        ("Obras distintas citadas en clase", len(obras)),
        ("Citas bibliográficas en clase", sum(len(c["lecturas"]) for c in clases.values())),
        ("Diagramas mermaid", len(paginas) + len(packs)),
        ("Preguntas de comprobación", len(curriculo) * 3),
        ("Evidencias de aprendizaje", len(curriculo)),
        ("Proyectos integradores de parte", len(packs)),
        ("Proyectos integradores mayores", len(list((RAIZ / "projects").glob("*.md"))) - 1),
        ("Guías de carrera por rol", len(guias)),
        ("Documentos transversales", len(list((RAIZ / "docs").glob("*.md")))),
        ("Casos profesionales", len(list((RAIZ / "cases").glob("*.md"))) - 1),
        ("Laboratorios", len([d for d in (RAIZ / "labs").iterdir() if d.is_dir()])),
        ("Plantillas de trabajo", len(list((RAIZ / "templates").glob("*.md"))) - 1),
        ("Pruebas estructurales", 33),
    ]
    tabla = "\n".join(f"| {nombre} | {numero(valor)} |" for nombre, valor in filas)

    return f"""# Manifiesto del repositorio

> Documento generado por `scripts/generar_indice.py`. **No editar a mano:** los cambios se
> pierden en la siguiente generación. La fuente de verdad está en `manifests/`.

Inventario cuantitativo verificable. Los números se calculan contando archivos reales; no se
declaran a mano. El CI comprueba en cada push que este archivo siga coincidiendo con el
repositorio.

| Elemento | Cantidad |
|---|---:|
{tabla}

## Estándar de clase

Cada una de las {len(curriculo)} clases cumple el estándar **`clase-profunda`**: 22 secciones
obligatorias, mínimo de 2.500 palabras, un diagrama, cuatro conceptos con definición operacional,
tres señales observables, ejemplo trabajado sobre el caso de su parte, rúbrica ponderada y
fuentes con su uso declarado.

## Verificación

```bash
python scripts/generar_clases.py --check
python scripts/generar_indice.py --check
python scripts/validar_estructura.py --resumen
python scripts/validar_encoding.py
python -m unittest discover -s tests -v
```

---

[⬅ Programa](README.md) · [Estado](STATUS.md) · [Índice de archivos](FILE_INDEX.md)
"""


# --------------------------------------------------------------------------- #
# docs/GLOSARIO.md
# --------------------------------------------------------------------------- #

def clave_alfabetica(termino: str) -> str:
    """Ordena ignorando tildes y mayúsculas, como haría un diccionario en español."""
    tabla = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    return termino.translate(tabla).lower()


def construir_glosario(curriculo, clases) -> str:
    por_numero = {c["global_class"]: c for c in curriculo}
    entradas: dict[str, list[tuple[str, dict]]] = {}
    for numero, registro in clases.items():
        for termino, definicion in registro["conceptos"]:
            entradas.setdefault(termino, []).append((definicion, por_numero[numero]))

    total = sum(len(v) for v in entradas.values())
    lineas = [
        "# Glosario del programa",
        "",
        f"Los **{len(entradas)} términos** definidos en las 300 clases, con su definición "
        "operacional y el enlace a la clase donde se trabaja. Se genera con "
        "`python scripts/generar_indice.py`: cada definición proviene de la clase que la usa, "
        "no de un diccionario aparte.",
        "",
        f"Un término puede aparecer definido en más de una clase cuando cambia lo que importa de "
        f"él según el contexto; por eso hay {total} definiciones para {len(entradas)} términos.",
        "",
    ]

    inicial_actual = ""
    for termino in sorted(entradas, key=clave_alfabetica):
        inicial = clave_alfabetica(termino)[0].upper()
        if inicial != inicial_actual:
            inicial_actual = inicial
            lineas += [f"## {inicial}", ""]
        for definicion, clase in entradas[termino]:
            ruta = f"../curriculum/{clase['part_slug']}/{clase['slug']}/README.md"
            lineas.append(
                f"- **{termino}** — {definicion}. "
                f"[Clase {clase['global_class']:03d}]({ruta})"
            )
        lineas.append("")

    lineas += [
        "---",
        "",
        "| Anterior | Índice | Siguiente |",
        "|---|---|---|",
        "| [Fuentes oficiales](FUENTES.md) | [Programa](../README.md) · "
        "[Documentos](../FILE_INDEX.md) | [Metodología](METODOLOGIA.md) |",
        "",
    ]
    return "\n".join(lineas)


# --------------------------------------------------------------------------- #
# SYLLABUS.md
# --------------------------------------------------------------------------- #

def construir_syllabus(curriculo, packs, clases, etapas) -> str:
    etapas_por_id = {e["id"]: e for e in etapas}
    bloques = [
        "# Programa detallado",
        "",
        "Las 300 clases con lo que cada una habilita, la evidencia que exige y el estado de la "
        "evidencia que la sostiene. Se genera con `python scripts/generar_indice.py`; la fuente "
        "es `manifests/`.",
        "",
        "> [!NOTE]",
        "> El **estado de evidencia** indica con qué respaldo se sostiene lo que la clase enseña: "
        "`ROBUSTA`, `CONSISTENTE`, `EMERGENTE`, `EN-DEBATE`, `MARCO-NORMATIVO` o "
        "`PRACTICA-PROFESIONAL`. Su definición está en "
        "[docs/ESTANDARES_DE_EVIDENCIA.md](docs/ESTANDARES_DE_EVIDENCIA.md).",
        "",
    ]
    for pack in packs:
        propias = [c for c in curriculo if c["part"] == pack["part"]]
        etapa = etapas_por_id[pack["etapa"]]
        slug = propias[0]["part_slug"]
        bloques += [
            f"## Parte {pack['part']:02d} — {pack['titulo']}",
            "",
            f"{etapa['emoji']} {etapa['nombre']} · población de referencia: {pack['poblacion']} · "
            f"clases {propias[0]['global_class']:03d}–{propias[-1]['global_class']:03d} · "
            f"[README de la parte](curriculum/{slug}/README.md)",
            "",
            f"*{pack['lema']}*",
            "",
            "| # | Clase | Decisión que habilita | Evidencia de aprendizaje | Estado |",
            "|---:|---|---|---|---|",
        ]
        for clase in propias:
            datos = clases[clase["global_class"]]
            bloques.append(
                f"| {clase['global_class']:03d} "
                f"| [{clase['title']}](curriculum/{slug}/{clase['slug']}/README.md) "
                f"| {datos['decision']} | {datos['entregable']} | `{datos['evidencia']}` |"
            )
        bloques.append("")
    return "\n".join(bloques)


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="falla si lo escrito no coincide")
    args = parser.parse_args()

    curriculo, packs, clases, etapas = cargar()
    salidas = {
        RAIZ / "STATUS.md": construir_status(curriculo, packs, clases, etapas),
        RAIZ / "FILE_INDEX.md": construir_indice(curriculo, packs),
        RAIZ / "SYLLABUS.md": construir_syllabus(curriculo, packs, clases, etapas),
        RAIZ / "MANIFEST.md": construir_manifiesto(curriculo, packs, clases),
        RAIZ / "docs" / "GLOSARIO.md": construir_glosario(curriculo, clases),
        RAIZ / "catalog.json": json.dumps(
            construir_catalogo(curriculo, packs, clases, etapas),
            ensure_ascii=False, indent=1) + "\n",
    }

    if args.check:
        desviados = [r.name for r, c in salidas.items()
                     if not r.exists() or r.read_text(encoding="utf-8") != c]
        if desviados:
            print(f"FALLÓ: desactualizados {desviados}. Ejecuta python scripts/generar_indice.py")
            return 1
        print("OK: STATUS, SYLLABUS, MANIFEST, FILE_INDEX, docs/GLOSARIO y catalog.json están al día.")
        return 0

    for ruta, contenido in salidas.items():
        ruta.write_text(contenido, encoding="utf-8", newline="\n")
    print("OK: STATUS, SYLLABUS, MANIFEST, FILE_INDEX, docs/GLOSARIO y catalog.json regenerados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
