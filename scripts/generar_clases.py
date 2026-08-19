#!/usr/bin/env python3
"""Genera el currículo completo desde los manifiestos.

Fuente única de verdad: `manifests/`. Este script escribe, y vuelve a escribir,
todos los `README.md` de `curriculum/`. Nada del árbol de clases se edita a mano:
lo que no está en un manifiesto no existe en el currículo.

Uso:
  python scripts/generar_clases.py            # escribe curriculum/
  python scripts/generar_clases.py --check    # falla si lo escrito no coincide
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "manifests"
CURRICULO = RAIZ / "curriculum"


# --------------------------------------------------------------------------- #
# Carga de manifiestos
# --------------------------------------------------------------------------- #

def leer(*partes: str):
    return json.loads(MANIFIESTOS.joinpath(*partes).read_text(encoding="utf-8"))


def cargar() -> tuple[list[dict], list[dict], dict[int, dict], dict, dict]:
    curriculo = leer("curriculum.json")
    packs: list[dict] = []
    for archivo in sorted((MANIFIESTOS / "parts").glob("*.json")):
        packs += json.loads(archivo.read_text(encoding="utf-8"))
    packs.sort(key=lambda p: p["part"])
    etapas = {e["id"]: e for e in leer("etapas.json")}
    pedagogia = leer("pedagogia", "marco.json")
    clases: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            if registro["n"] in clases:
                raise SystemExit(f"clase duplicada en los manifiestos: {registro['n']}")
            clases[registro["n"]] = registro
    return curriculo, packs, clases, etapas, pedagogia


# --------------------------------------------------------------------------- #
# Utilidades de redacción
# --------------------------------------------------------------------------- #

def vinetas(elementos: list[str], marca: str = "-") -> str:
    return "\n".join(f"{marca} {e}" for e in elementos)


def casillas(elementos: list[str]) -> str:
    return "\n".join(f"- [ ] {e}" for e in elementos)


def numerada(elementos: list[str]) -> str:
    return "\n".join(f"{i}. {e}" for i, e in enumerate(elementos, 1))


def envolver(texto: str, ancho: int = 26) -> str:
    """Parte un rótulo largo en varias líneas para que quepa dentro de un nodo mermaid."""
    lineas: list[str] = []
    actual = ""
    for palabra in texto.split():
        if len(actual) + len(palabra) + 1 > ancho and actual:
            lineas.append(actual)
            actual = palabra
        else:
            actual = f"{actual} {palabra}".strip()
    if actual:
        lineas.append(actual)
    return "<br/>".join(lineas)


def limpio(texto: str) -> str:
    """Texto apto para el interior de un nodo mermaid."""
    for original, reemplazo in (('"', "'"), ("(", ""), (")", ""), ("#", ""), ("{", ""), ("}", "")):
        texto = texto.replace(original, reemplazo)
    return texto


def nodo(texto: str, ancho: int = 24, tope: int = 96) -> str:
    """Rótulo de nodo: recortado para que el diagrama no se deforme."""
    if len(texto) > tope:
        texto = texto[:tope].rsplit(" ", 1)[0] + "…"
    return limpio(envolver(texto, ancho))


def sin_verbo(decision: str) -> str:
    """Quita el verbo inicial de la decisión para no repetirlo tras «**Decidir**»."""
    return re.sub(r"^(decidir|definir|determinar|escoger|establecer|priorizar)\s+", "", decision)


# --------------------------------------------------------------------------- #
# Página de clase
# --------------------------------------------------------------------------- #

def mapa_de_clase(datos: dict) -> str:
    conceptos = "\n".join(
        f'    C --> A{i}["{nodo(nombre, 22)}"]'
        for i, (nombre, _) in enumerate(datos["conceptos"], 1)
    )
    enlaces = " & ".join(f"A{i}" for i in range(1, len(datos["conceptos"]) + 1))
    return f"""```mermaid
flowchart TB
    C["Situacion educativa<br/>nivel · grupo · proposito"]
{conceptos}
    {enlaces} --> D{{{{"{nodo(datos['decision'])}"}}}}
    D --> E["Evidencia de aprendizaje<br/>{nodo(datos['entregable'])}"]
    E --> V{{"Cumple el<br/>criterio de logro?"}}
    V -->|si| S["Evidencia archivada<br/>y clase siguiente"]
    V -->|no| C
```"""


def pagina_de_clase(clase: dict, datos: dict, pack: dict, etapa: dict,
                    pedagogia: dict, vecinas: tuple[dict | None, dict | None]) -> str:
    anterior, siguiente = vecinas
    conceptos = "\n".join(f"| **{n}** | {d} |" for n, d in datos["conceptos"])
    contextos = "\n".join(f"| {n} | {r} |" for n, r in pack["contextos"])
    lecturas = "\n\n".join(
        f"**{referencia}**  \n*Qué aporta a esta clase:* {nota}"
        for referencia, nota in datos["lecturas"]
    )
    nivel = pedagogia["niveles_evidencia"][datos["evidencia"]]

    resultados = [
        "**Definir** con precisión los cuatro conceptos centrales de la clase y reconocerlos "
        "en una situación educativa real, no solo en su enunciado.",
        f"**Explicar** {datos['foco']}.",
        f"**Decidir** —{sin_verbo(datos['decision'])}— y sostener la decisión con un fundamento escrito.",
        f"**Producir** la evidencia de la clase —{datos['entregable']}— y contrastarla contra "
        f"el criterio de logro.",
        "**Distinguir** lo que la evidencia sostiene de lo que es práctica instalada, "
        "preferencia personal o costumbre de la institución.",
    ]

    anterior_md = (
        f"[← {anterior['global_class']:03d} · {anterior['title']}](../{anterior['slug']}/README.md)"
        if anterior and anterior["part"] == clase["part"]
        else f"[← Parte {clase['part']:02d}](../README.md)"
    )
    siguiente_md = (
        f"[{siguiente['global_class']:03d} · {siguiente['title']} →](../{siguiente['slug']}/README.md)"
        if siguiente and siguiente["part"] == clase["part"]
        else "[Programa completo →](../../../README.md)"
    )

    return f"""# Clase {clase['global_class']:03d} — {clase['title']}

> **Parte {clase['part']:02d} · {clase['part_title']}** — clase {clase['class']} de 12

**Estado de evidencia:** `{datos['evidencia']}` · **Etapa:** {etapa['emoji']} {etapa['nombre']} · \
**Población de referencia:** {pack['poblacion']}<br>
**Decisión que habilita:** {datos['decision']}<br>
**Evidencia de aprendizaje:** {datos['entregable']}

## 🎯 Propósito

{datos['proposito']}

## 📚 Resultados de aprendizaje

Al finalizar esta clase podrás:

{numerada(resultados)}

## 🧩 Conceptos centrales

| Concepto | Comprensión verificable |
|---|---|
{conceptos}

## 🗺️ Flujo de razonamiento

{mapa_de_clase(datos)}

## 📖 Desarrollo

### 1. El fondo del asunto

{datos['desarrollo']}

### 2. Cómo se traduce en decisiones de enseñanza

{datos['practica']}

### 3. Qué sostiene la evidencia y qué no

{datos['limites']}

> **Cómo leer el estado de evidencia `{datos['evidencia']}`.** {nivel}

## 🧪 Taller guiado

Aplica la clase a **uno** de los contextos siguientes y repite después el ejercicio en un
contexto de exigencia distinta. Cambiar de contexto es parte del aprendizaje: lo que funciona
con un grupo no se traslada intacto a otro.

| Contexto | Rasgo que cambia la decisión |
|---|---|
{contextos}

**Secuencia de trabajo:**

1. Delimita el contexto: nivel, edad, tamaño del grupo, asignatura o experiencia y tiempo real disponible.
2. Declara qué saben ya los estudiantes y **cómo lo comprobaste**, no cómo lo supones.
3. Formula la decisión pedagógica que esta clase habilita y escribe su fundamento.
4. Anticipa qué observarías si la decisión funciona y qué observarías si no funciona.
5. Diseña de antemano la alternativa que aplicarás si la primera estrategia falla.
6. Ejecuta o simula, y registra lo observado con fecha, contexto y evidencia concreta.
7. Produce la evidencia de aprendizaje de la clase.
8. Contrástala contra el criterio de logro, corrige y recién entonces avanza.

### 📦 Evidencia de aprendizaje

{datos['entregable'][0].upper()}{datos['entregable'][1:]}.

Debe incluir contexto, decisión, fundamento, fuentes consultadas con su fecha, indicador de
logro observable, riesgos previstos y qué harías distinto en la siguiente iteración.

## 🏆 Reto verificable

{datos['reto']}

## ✅ Criterio de logro

{casillas(datos['criterios'] + pedagogia['criterios_comunes'])}

## ⚠️ Errores frecuentes

**Propios de esta clase:**

{vinetas(datos['errores'])}

**Característicos de la parte {clase['part']:02d}:**

{vinetas(pack['riesgos'][:2])}

## ♿ Diversidad, accesibilidad y ética

{datos['inclusion']}

Antes de aplicar cualquier decisión de esta clase con estudiantes reales, revisa el
[protocolo de práctica responsable](../../../docs/ETICA_Y_PRACTICA_RESPONSABLE.md):
consentimiento, resguardo de datos personales, proporcionalidad de la intervención y derecho
de cada estudiante a no ser objeto de un ensayo que no le reporta beneficio.

## ❓ Preguntas de comprobación

{numerada(datos['preguntas'])}

## 📕 Lecturas base

{lecturas}

Catálogo completo: [bibliografía del programa](../../../docs/BIBLIOGRAFIA.md) ·
[glosario](../../../docs/GLOSARIO.md) ·
[fuentes oficiales y cómo leerlas](../../../docs/FUENTES.md).

## 🔗 Conexión con el resto del programa

{datos['conexion']}

> [!IMPORTANT]
> Material de formación profesional. No reemplaza un título de pedagogía, una habilitación
> legal para ejercer, ni el juicio de un equipo educativo que conoce a sus estudiantes.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| {anterior_md} | [Parte {clase['part']:02d}](../README.md) · [Programa](../../../README.md) | {siguiente_md} |
"""


# --------------------------------------------------------------------------- #
# Página de parte
# --------------------------------------------------------------------------- #

def pagina_de_parte(pack: dict, clases: list[dict], etapa: dict, datos: dict[int, dict],
                    vecinas: tuple[dict | None, dict | None]) -> str:
    previa, siguiente = vecinas
    nav_anterior = (
        f"[← Parte {previa['part']:02d} · {previa['titulo']}](../{previa['slug']}/README.md)"
        if previa else "[← Inicio del programa](../../README.md)"
    )
    nav_siguiente = (
        f"[Parte {siguiente['part']:02d} · {siguiente['titulo']} →](../{siguiente['slug']}/README.md)"
        if siguiente else "[Proyectos integradores →](../../projects/README.md)"
    )
    filas = "\n".join(
        f"| {c['global_class']:03d} | [{c['title']}]({c['slug']}/README.md) | "
        f"{datos[c['global_class']]['decision']} | `{datos[c['global_class']]['evidencia']}` |"
        for c in clases
    )
    conceptos = sum(len(datos[c["global_class"]]["conceptos"]) for c in clases)
    lecturas = vinetas([f"**{ref}** — {nota}" for ref, nota in pack["lecturas"]])
    resumen = "\n\n".join(pack["resumen"])
    return f"""# Parte {pack['part']:02d} — {pack['titulo']}

> *{pack['lema']}*

{etapa['emoji']} **{etapa['nombre']}** · salida de la etapa: {etapa['salida']}

**Clases:** 12 ({clases[0]['global_class']:03d}–{clases[-1]['global_class']:03d}) · \
**Población de referencia:** {pack['poblacion']} · \
**Conceptos con definición operacional:** {conceptos}<br>
**Contenido central:** {pack['contenido_central']}

## 🎯 De qué trata esta parte

{resumen}

## 📚 Resultados de la parte

Al terminar esta parte podrás:

{numerada([f"**{r}**." for r in pack['resultados']])}

## 🗺️ Mapa de la parte

{pack['mapa']}

## 🧠 Marco de referencia

{vinetas(pack['marco'])}

**Autoras y autores que conviene conocer:** {pack['autores']}

## 📋 Las 12 clases

| # | Clase | Decisión que habilita | Evidencia |
|---:|---|---|---|
{filas}

## ⚠️ Riesgos característicos

{vinetas(pack['riesgos'])}

## 📕 Lecturas de referencia de la parte

{lecturas}

## ✅ Evidencia mínima para dar la parte por cerrada

{casillas(pack['evidencias'])}

---

| Anterior | Índice | Siguiente |
|---|---|---|
| {nav_anterior} | [Programa](../../README.md) · [Currículo](../../CURRICULUM.md) | {nav_siguiente} |
"""


# --------------------------------------------------------------------------- #
# Ejecución
# --------------------------------------------------------------------------- #

def construir(parcial: bool = False) -> dict[Path, str]:
    curriculo, packs, datos, etapas, pedagogia = cargar()
    faltan = [c["global_class"] for c in curriculo if c["global_class"] not in datos]
    if faltan and not parcial:
        raise SystemExit(
            f"faltan {len(faltan)} clases en manifests/classes/: {faltan[:12]}…"
        )
    if faltan:
        print(f"AVISO: modo parcial, {len(faltan)} clase(s) sin manifiesto se omiten.")
        curriculo = [c for c in curriculo if c["global_class"] in datos]
        packs = [p for p in packs if any(c["part"] == p["part"] for c in curriculo)]

    packs_por_numero = {p["part"]: p for p in packs}
    archivos: dict[Path, str] = {}

    for indice, clase in enumerate(curriculo):
        pack = packs_por_numero[clase["part"]]
        etapa = etapas[pack["etapa"]]
        vecinas = (
            curriculo[indice - 1] if indice > 0 else None,
            curriculo[indice + 1] if indice + 1 < len(curriculo) else None,
        )
        destino = CURRICULO / clase["part_slug"] / clase["slug"] / "README.md"
        archivos[destino] = pagina_de_clase(
            clase, datos[clase["global_class"]], pack, etapa, pedagogia, vecinas
        )

    slugs = {c["part"]: c["part_slug"] for c in curriculo}
    for indice, pack in enumerate(packs):
        clases = [c for c in curriculo if c["part"] == pack["part"]]
        etapa = etapas[pack["etapa"]]
        vecinas = (
            {**packs[indice - 1], "slug": slugs[packs[indice - 1]["part"]]} if indice > 0 else None,
            {**packs[indice + 1], "slug": slugs[packs[indice + 1]["part"]]}
            if indice + 1 < len(packs) else None,
        )
        destino = CURRICULO / clases[0]["part_slug"] / "README.md"
        archivos[destino] = pagina_de_parte(pack, clases, etapa, datos, vecinas)

    return archivos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si el árbol no coincide con los manifiestos")
    parser.add_argument("--parcial", action="store_true",
                        help="genera solo las clases que ya tienen manifiesto (uso durante la redacción)")
    args = parser.parse_args()

    archivos = construir(parcial=args.parcial)

    if args.check:
        desviados = [
            ruta for ruta, contenido in archivos.items()
            if not ruta.exists() or ruta.read_text(encoding="utf-8") != contenido
        ]
        sobrantes = (
            [p for p in CURRICULO.rglob("README.md") if p not in archivos]
            if CURRICULO.exists() else []
        )
        if desviados or sobrantes:
            print(f"FALLÓ: {len(desviados)} archivo(s) desincronizados y "
                  f"{len(sobrantes)} sobrante(s).")
            for ruta in (desviados + sobrantes)[:10]:
                print(f"  {ruta.relative_to(RAIZ).as_posix()}")
            print("Ejecuta: python scripts/generar_clases.py")
            return 1
        print(f"OK: {len(archivos)} archivos del currículo coinciden con los manifiestos.")
        return 0

    for ruta, contenido in archivos.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8", newline="\n")

    palabras = sum(len(c.split()) for c in archivos.values())
    print(f"OK: {len(archivos)} archivos escritos en curriculum/ ({palabras:,} palabras).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
