#!/usr/bin/env python3
"""Exporta el programa como paquete de capacitación listo para migrar a un LMS.

El currículo vive en Markdown porque es lo que se puede versionar y revisar. Pero
una plataforma de capacitación necesita otra cosa: HTML por lección, metadatos
estructurados y una tabla que el equipo administrativo pueda cargar. Este script
produce las tres cosas sin tocar la fuente.

Genera en `capacitacion/`:

  index.html              índice navegable del paquete completo
  paginas/clase-NNN.html  página autocontenida por clase (estilos incluidos)
  contenido/clase-NNN.html fragmento HTML para pegar en el editor del LMS
  manifiesto.json         metadatos por módulo y lección para carga automatizada
  programa.csv            tabla plana para carga manual o revisión administrativa
  LEEME.md                instrucciones de migración y decisiones del formato

Uso:
  python scripts/exportar_capacitacion.py
  python scripts/exportar_capacitacion.py --check   # valida sin escribir
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_sitio import markdown_a_html  # noqa: E402  reutiliza el mismo conversor

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "capacitacion"
CURRICULO = RAIZ / "curriculum"

# Horas estimadas por clase para la programación de la capacitación: 1 hora de
# trabajo con el material y 1,5 de práctica y producción de la evidencia.
HORAS_MATERIAL = 1.0
HORAS_PRACTICA = 1.5

ESTILOS = """
:root{--fondo:#fff;--texto:#12181f;--tenue:#5a6572;--borde:#dfe4ea;--acento:#0b62d0;--codigo:#f2f4f7}
body{margin:0 auto;max-width:52rem;padding:2rem 1.2rem 4rem;background:var(--fondo);color:var(--texto);
 font:16px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
h1{font-size:1.8rem;line-height:1.2;margin:.2rem 0 1rem}
h2{font-size:1.25rem;margin:2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--borde)}
h3{font-size:1.02rem;margin:1.4rem 0 .4rem}
a{color:var(--acento)}
table{border-collapse:collapse;width:100%;font-size:.93rem;margin:1rem 0}
th,td{text-align:left;padding:.5rem .7rem;border:1px solid var(--borde);vertical-align:top}
th{background:#f5f7fa}
blockquote{margin:1rem 0;padding:.7rem 1rem;background:#f5f7fa;border-left:3px solid var(--acento);
 border-radius:0 8px 8px 0;color:var(--tenue)}
blockquote p{margin:0}
code{background:var(--codigo);padding:.13em .38em;border-radius:5px;font:.87em ui-monospace,Consolas,monospace}
pre{background:var(--codigo);border:1px solid var(--borde);border-radius:10px;padding:.9rem 1rem;overflow-x:auto}
pre.mermaid{color:var(--tenue);font-size:.85em}
li.tarea{list-style:none;margin-left:-1.2rem}
hr{border:none;border-top:1px solid var(--borde);margin:2rem 0}
.pie{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--borde);color:var(--tenue);font-size:.85rem}
"""


def cargar() -> tuple[list[dict], dict[int, dict], list[dict]]:
    manifiestos = RAIZ / "manifests"
    curriculo = json.loads((manifiestos / "curriculum.json").read_text(encoding="utf-8"))
    clases: dict[int, dict] = {}
    for archivo in sorted((manifiestos / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            clases[registro["n"]] = registro
    packs: list[dict] = []
    for archivo in sorted((manifiestos / "parts").glob("*.json")):
        packs += json.loads(archivo.read_text(encoding="utf-8"))
    packs.sort(key=lambda p: p["part"])
    return curriculo, clases, packs


def fragmento(clase: dict) -> str:
    """HTML del contenido de la clase, sin cabecera ni navegación del repositorio."""
    origen = CURRICULO / clase["part_slug"] / clase["slug"] / "README.md"
    texto = origen.read_text(encoding="utf-8")
    # La tabla de navegación final y el separador previo no tienen sentido en un LMS,
    # que construye su propia navegación entre lecciones.
    texto = texto.rsplit("\n---\n", 1)[0].rstrip() + "\n"
    return markdown_a_html(texto, origen.parent)


def pagina(clase: dict, cuerpo: str, anterior: dict | None, siguiente: dict | None) -> str:
    navegacion = []
    if anterior:
        navegacion.append(f'<a href="clase-{anterior["global_class"]:03d}.html">← anterior</a>')
    navegacion.append('<a href="../index.html">índice</a>')
    if siguiente:
        navegacion.append(f'<a href="clase-{siguiente["global_class"]:03d}.html">siguiente →</a>')
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clase {clase['global_class']:03d} · {html.escape(clase['title'])}</title>
<style>{ESTILOS}</style>
</head>
<body>
{cuerpo}
<p class="pie">{' · '.join(navegacion)}<br>
Material de formación profesional. No reemplaza un título de pedagogía ni una habilitación legal
para ejercer.</p>
</body>
</html>
"""


def construir(curriculo, clases, packs) -> tuple[dict[Path, str], dict]:
    archivos: dict[Path, str] = {}
    packs_por_numero = {p["part"]: p for p in packs}
    modulos: list[dict] = []
    filas: list[dict] = []

    for indice, clase in enumerate(curriculo):
        datos = clases[clase["global_class"]]
        cuerpo = fragmento(clase)
        anterior = curriculo[indice - 1] if indice > 0 else None
        siguiente = curriculo[indice + 1] if indice + 1 < len(curriculo) else None
        numero = f"{clase['global_class']:03d}"
        archivos[SALIDA / "contenido" / f"clase-{numero}.html"] = cuerpo + "\n"
        archivos[SALIDA / "paginas" / f"clase-{numero}.html"] = pagina(
            clase, cuerpo, anterior, siguiente)

        filas.append({
            "modulo": f"{clase['part']:02d}",
            "modulo_titulo": clase["part_title"],
            "leccion": clase["class"],
            "codigo": f"PED-{numero}",
            "titulo": clase["title"],
            "estado_evidencia": datos["evidencia"],
            "horas_material": HORAS_MATERIAL,
            "horas_practica": HORAS_PRACTICA,
            "decision": datos["decision"],
            "evidencia_de_aprendizaje": datos["entregable"],
            "archivo_html": f"contenido/clase-{numero}.html",
        })

    for pack in packs:
        propias = [c for c in curriculo if c["part"] == pack["part"]]
        modulos.append({
            "modulo": f"{pack['part']:02d}",
            "titulo": pack["titulo"],
            "etapa": pack["etapa"],
            "poblacion": pack["poblacion"],
            "resultados": pack["resultados"],
            "horas_estimadas": round(len(propias) * (HORAS_MATERIAL + HORAS_PRACTICA), 1),
            "lecciones": [{
                "codigo": f"PED-{c['global_class']:03d}",
                "orden": c["class"],
                "titulo": c["title"],
                "estado_evidencia": clases[c["global_class"]]["evidencia"],
                "objetivo": clases[c["global_class"]]["proposito"],
                "decision": clases[c["global_class"]]["decision"],
                "evidencia_de_aprendizaje": clases[c["global_class"]]["entregable"],
                "criterios_de_logro": clases[c["global_class"]]["criterios"],
                "preguntas_de_comprobacion": clases[c["global_class"]]["preguntas"],
                "contenido_html": f"contenido/clase-{c['global_class']:03d}.html",
                "pagina_html": f"paginas/clase-{c['global_class']:03d}.html",
            } for c in propias],
        })

    manifiesto = {
        "programa": "Programa Integral de Pedagogía, Docencia y Ciencias del Aprendizaje",
        "version": (RAIZ / "VERSION").read_text(encoding="utf-8").strip(),
        "idioma": "es",
        "modalidad": "autoformación con evidencia; adaptable a capacitación tutorizada",
        "horas_totales_estimadas": round(len(curriculo) * (HORAS_MATERIAL + HORAS_PRACTICA), 1),
        "supuesto_de_horas": (f"{HORAS_MATERIAL} h de trabajo con el material y "
                              f"{HORAS_PRACTICA} h de práctica y producción de evidencia por clase"),
        "modulos": modulos,
    }
    archivos[SALIDA / "manifiesto.json"] = json.dumps(manifiesto, ensure_ascii=False, indent=1) + "\n"

    buffer = io.StringIO()
    escritor = csv.DictWriter(buffer, fieldnames=list(filas[0]), lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(filas)
    archivos[SALIDA / "programa.csv"] = buffer.getvalue()

    enlaces = ""
    for modulo in modulos:
        enlaces += f"<h2>Módulo {modulo['modulo']} — {html.escape(modulo['titulo'])}</h2><ol>"
        for leccion in modulo["lecciones"]:
            enlaces += (f'<li><a href="{leccion["pagina_html"]}">'
                        f'{html.escape(leccion["titulo"])}</a></li>')
        enlaces += "</ol>"
    archivos[SALIDA / "index.html"] = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paquete de capacitación · {html.escape(manifiesto['programa'])}</title>
<style>{ESTILOS}</style>
</head>
<body>
<h1>Paquete de capacitación</h1>
<p>{html.escape(manifiesto['programa'])} · versión {manifiesto['version']} ·
{len(modulos)} módulos · {len(curriculo)} lecciones ·
{manifiesto['horas_totales_estimadas']:.0f} horas estimadas.</p>
<p>Cada lección incluye su página autocontenida y un fragmento HTML listo para pegar en el
editor de contenidos de una plataforma. Los metadatos están en
<a href="manifiesto.json">manifiesto.json</a> y la tabla plana en
<a href="programa.csv">programa.csv</a>.</p>
{enlaces}
<p class="pie">Material de formación profesional. No reemplaza un título de pedagogía ni una
habilitación legal para ejercer.</p>
</body>
</html>
"""

    archivos[SALIDA / "LEEME.md"] = f"""# Paquete de capacitación

Generado con `python scripts/exportar_capacitacion.py`. **No se edita a mano**: la fuente es
`manifests/` y el árbol `curriculum/`.

## Qué contiene

| Archivo | Para qué sirve |
|---|---|
| `index.html` | índice navegable del paquete completo |
| `paginas/clase-NNN.html` | página autocontenida por clase, con estilos incluidos |
| `contenido/clase-NNN.html` | fragmento HTML para pegar en el editor del LMS |
| `manifiesto.json` | metadatos por módulo y lección para carga automatizada |
| `programa.csv` | tabla plana para carga manual o revisión administrativa |

## Cifras del paquete

- Módulos: **{len(modulos)}**
- Lecciones: **{len(curriculo)}**
- Horas estimadas: **{manifiesto['horas_totales_estimadas']:.0f}**
  ({manifiesto['supuesto_de_horas']})

## Cómo migrarlo

1. Carga la estructura de módulos y lecciones desde `manifiesto.json` o `programa.csv`.
2. Para cada lección, usa `contenido/clase-NNN.html` como cuerpo de la lección.
3. Registra `evidencia_de_aprendizaje` como tarea entregable y `criterios_de_logro` como
   rúbrica de aprobación.
4. Usa `preguntas_de_comprobacion` como cuestionario de cierre de lección.
5. Mantén visible el `estado_evidencia` de cada lección: es parte del contenido, no un
   metadato interno. Distingue lo que la evidencia sostiene de lo que es práctica o norma.

## Decisiones del formato

- Los fragmentos no incluyen `<html>`, `<head>` ni navegación: la plataforma aporta lo suyo.
- Los diagramas se exportan como bloques `pre.mermaid`. Si la plataforma no renderiza
  mermaid, el bloque queda como texto legible y la lección sigue siendo completa.
- La tabla de navegación entre clases se elimina del fragmento porque la plataforma
  construye su propia secuencia.
- Las horas son una estimación declarada, no una medición. Ajusta el supuesto en
  `scripts/exportar_capacitacion.py` si tu contexto exige otra carga.
"""
    return archivos, manifiesto


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="valida sin escribir en disco")
    args = parser.parse_args()

    if not CURRICULO.exists():
        print("FALLÓ: no existe curriculum/. Ejecuta python scripts/generar_clases.py")
        return 1

    curriculo, clases, packs = cargar()
    archivos, manifiesto = construir(curriculo, clases, packs)

    if args.check:
        vacios = [r.name for r, c in archivos.items() if len(c.strip()) < 40]
        if vacios:
            print(f"FALLÓ: {len(vacios)} archivo(s) exportados quedarían vacíos: {vacios[:5]}")
            return 1
        print(f"OK: el paquete compila con {len(archivos)} archivos y "
              f"{len(curriculo)} lecciones.")
        return 0

    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    for ruta, contenido in archivos.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8", newline="\n")

    print(f"OK: paquete de capacitación en capacitacion/ con {len(manifiesto['modulos'])} módulos, "
          f"{len(curriculo)} lecciones y {len(archivos)} archivos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
