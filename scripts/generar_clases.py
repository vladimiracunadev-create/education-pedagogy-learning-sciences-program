#!/usr/bin/env python3
"""Genera el currículo completo desde los manifiestos.

Fuente única de verdad: `manifests/`. Este script escribe, y vuelve a escribir,
todos los `README.md` de `curriculum/`. Nada del árbol de clases se edita a mano:
lo que no está en un manifiesto no existe en el currículo.

Estándar de clase: `clase-profunda`. Cada clase publica propósito, resultados,
agenda, conceptos operacionales, modelo mental, desarrollo en seis capas, lectura
comparada, ejemplo trabajado sobre el caso de la parte, comparación de caminos,
lectura por nivel de rol, taller, caso profesional, evidencia, rúbrica ponderada,
errores frecuentes, contexto normativo, preguntas y fuentes verificables.

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


# --------------------------------------------------------------------------- #
# Registro de fuentes: la cita de clase apunta al localizador, no solo al listado
# --------------------------------------------------------------------------- #

REGISTRO = RAIZ / "sources" / "bibliography.json"
_FUENTES: dict[str, dict] | None = None


def registro_de_fuentes() -> dict[str, dict]:
    """Cita → entrada del registro. Se lee una vez y se reutiliza."""
    global _FUENTES
    if _FUENTES is None:
        datos = json.loads(REGISTRO.read_text(encoding="utf-8"))
        _FUENTES = {entrada["cita"]: entrada for entrada in datos["entries"]}
    return _FUENTES


def localizador(cita: str, subir: str) -> str:
    """Referencia cruzada de una cita: su ficha en el registro y, si resolvió, su
    localizador. Sin esto, «Autor (Año)» obliga a buscar la obra a mano.
    """
    entrada = registro_de_fuentes().get(cita.strip())
    if entrada is None:
        raise SystemExit(
            f"la obra no está en sources/bibliography.json: {cita[:70]}\n"
            "Ejecuta: python scripts/verificar_fuentes.py"
        )
    ficha = f"[ficha]({subir}docs/REGISTRO_DE_FUENTES.md#{entrada['id']})"
    if entrada["status"] != "verificada" or not entrada.get("locator"):
        return f"**Localizar:** {ficha} — sin localizador verificado todavía."
    if entrada.get("isbn13"):
        etiqueta = f"ISBN {entrada['isbn13']}"
    elif entrada.get("doi"):
        etiqueta = f"DOI {entrada['doi']}"
    else:
        etiqueta = "fuente oficial"
    return f"**Localizar:** [{etiqueta}]({entrada['locator']}) · {ficha}"


def cargar() -> tuple[list[dict], list[dict], dict[int, dict], dict, dict, dict]:
    curriculo = leer("curriculum.json")
    packs: list[dict] = []
    for archivo in sorted((MANIFIESTOS / "parts").glob("*.json")):
        packs += json.loads(archivo.read_text(encoding="utf-8"))
    packs.sort(key=lambda p: p["part"])
    etapas = {e["id"]: e for e in leer("etapas.json")}
    pedagogia = leer("pedagogia", "marco.json")
    casos = leer("pedagogia", "casos.json")

    clases: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in json.loads(archivo.read_text(encoding="utf-8")):
            if registro["n"] in clases:
                raise SystemExit(f"clase duplicada en los manifiestos: {registro['n']}")
            clases[registro["n"]] = registro

    return curriculo, packs, clases, etapas, pedagogia, casos


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


def minuscula(texto: str) -> str:
    return texto[0].lower() + texto[1:] if texto else texto


def mayuscula(texto: str) -> str:
    return texto[0].upper() + texto[1:] if texto else texto


def frase(texto: str) -> str:
    """Primera oración de un párrafo, para reutilizarla sin repetir el párrafo entero."""
    partes = re.split(r"(?<=[.:;])\s+", texto.strip())
    return partes[0] if partes else texto


# --------------------------------------------------------------------------- #
# Secciones de la clase
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


def metodo_de_clase(datos: dict) -> list[str]:
    """El método del programa, instanciado con los conceptos de esta clase.

    No es un método distinto por clase: es el mismo ciclo profesional —delimitar,
    clasificar, decidir, anticipar, registrar— aplicado a los conceptos que la
    clase pone en juego. Que sea siempre el mismo es deliberado: se aprende
    repitiéndolo hasta que deja de necesitar la lista.
    """
    conceptos = [c[0] for c in datos["conceptos"]]
    return [
        "delimitar el contexto y comprobar —no suponer— qué saben ya los estudiantes",
        f"clasificar la situación distinguiendo **{conceptos[0]}** de **{conceptos[1]}**",
        f"decidir con fundamento, usando **{conceptos[2]}** como criterio y declarando la fuente",
        f"anticipar qué evidencia confirmaría la decisión y cuál la refutaría, con "
        f"**{conceptos[3]}** a la vista",
        "registrar lo ocurrido y contrastarlo contra el criterio de logro antes de avanzar",
    ]


def senales_de_clase(datos: dict) -> list[tuple[str, str]]:
    """Las tres señales observables que toda clase del programa exige recoger."""
    return [
        ("Evidencia de partida",
         "qué sabían o podían hacer los estudiantes antes de la decisión, comprobado y no supuesto"),
        ("Evidencia de proceso",
         "qué se observó mientras la decisión se aplicaba, con fecha, contexto y responsable del registro"),
        ("Evidencia de logro",
         f"qué muestra {minuscula(datos['entregable'])} frente al criterio declarado de antemano"),
    ]


def agenda(datos: dict) -> str:
    pasos = metodo_de_clase(datos)
    return f"""| Minutos | Bloque | Qué ocurre |
|---:|---|---|
| 0–10 | Activación | Recuperar sin mirar la clase anterior y responder la pregunta de foco. |
| 10–25 | Conceptos | Definir los cuatro conceptos y reconocerlos en un caso real. |
| 25–45 | Modelo mental | Recorrer el método: {minuscula(pasos[0])}. |
| 45–70 | Ejemplo trabajado | Aplicar el método al caso de la parte, paso a paso y con evidencia. |
| 70–85 | Taller | Trasladar la decisión al contexto propio y anticipar su alternativa. |
| 85–90 | Cierre | Fijar responsable, plazo e indicador de la evidencia de aprendizaje. |

Fuera de la sesión, la clase exige aproximadamente **una hora y media** de práctica y de
producción de la evidencia. Si el tiempo se recorta, se recorta el ejemplo trabajado, nunca la
producción de evidencia: es la única parte que prueba el aprendizaje."""


def modelo_mental(datos: dict) -> str:
    pasos = numerada([mayuscula(p) + "." for p in metodo_de_clase(datos)])
    senales = "\n".join(f"| **{nombre}** | {definicion} |"
                        for nombre, definicion in senales_de_clase(datos))
    return f"""El método de esta clase, en cinco pasos que se ejecutan en orden:

{pasos}

Lo que hace profesional a este método no son los pasos sino la evidencia que exige en cada uno.
Estas son las señales observables con las que se comprueba, y que deben quedar definidas **antes**
de recogerlas:

| Señal observable | Cómo se recoge y qué significa |
|---|---|
{senales}

**Frontera de aplicación.** El método vale mientras las condiciones que lo sostienen se cumplan.
{frase(datos['limites'])} Cuando esa condición falla, el paso siguiente no es forzar el método:
es declarar el límite y decidir con menos certeza, dejándolo por escrito."""


def desarrollo(datos: dict, pack: dict, nivel: str) -> str:
    conceptos = datos["conceptos"]
    senales = "\n".join(
        f"- **{nombre}.** {mayuscula(definicion)}. Se registra con fecha y contexto; sin eso, "
        f"la señal no distingue una tendencia de una casualidad."
        for nombre, definicion in senales_de_clase(datos)
    )
    return f"""### 1. El fondo del asunto

{datos['desarrollo']}

### 2. Frontera conceptual: qué es y qué no es

Los cuatro conceptos de esta clase se confunden entre sí con facilidad, y esa confusión no es
inocua: produce decisiones que atacan el problema equivocado. **{conceptos[0][0]}** no es lo
mismo que **{conceptos[1][0]}** —{minuscula(conceptos[1][1])}—, y tratarlos como sinónimos hace
que la intervención se dirija al lugar incorrecto. Del mismo modo, **{conceptos[2][0]}** y
**{conceptos[3][0]}** describen aspectos distintos de la misma situación: el primero
{minuscula(frase(conceptos[2][1]))}, mientras el segundo {minuscula(frase(conceptos[3][1]))}.

La prueba de que la distinción está entendida es operacional, no verbal: dos personas que
observan la misma clase deben poder clasificar el mismo episodio de la misma manera. Si no
coinciden, el problema está en la definición y no en el observador. El error de clasificación más
frecuente en esta materia es el primero de los que se listan más abajo, y conviene anticiparlo
antes de aplicar nada.

### 3. Cómo se observa y se mide

Nada de lo anterior sirve si no se puede observar. Estas son las señales que esta clase usa y
cómo se recogen:

{senales}

Ninguna de estas señales es el aprendizaje: son indicios de él. Confundir el indicio con el
fenómeno es el error clásico de la medición educativa, y por eso cada señal se interpreta junto
con el contexto, el punto de partida del grupo y lo que el propio estudiante puede explicar sobre
su trabajo.

### 4. Cómo se traduce en decisiones de enseñanza

{datos['practica']}

### 5. Qué sostiene la evidencia y qué no

{datos['limites']}

> **Cómo leer el estado de evidencia `{datos['evidencia']}`.** {nivel}

### 6. Integración: de los conceptos a una decisión defendible

Una decisión es defendible cuando puede explicarse a alguien que no estuvo presente. Esta clase
te deja en condiciones de {sin_verbo(datos['decision'])}, y esa decisión se sostiene solo si
declara cuatro cosas: la evidencia que la funda, el supuesto que asume, el indicador que la
comprobaría y la condición que la haría cambiar.

Ese es también el criterio con el que se evalúa la evidencia de aprendizaje de la clase. Un
análisis que podría copiarse a otra clase, a otro curso o a otro establecimiento sin cambiar una
palabra no es una decisión: es una declaración general, y el oficio empieza justo donde las
declaraciones generales terminan."""


def lectura_comparada(datos: dict) -> str:
    filas = "\n".join(
        f"| {referencia.replace('**', '')} | {nota} | ¿Qué supuesto de esta clase ayuda a poner a prueba? |"
        for referencia, nota in datos["lecturas"]
    )
    return f"""Las obras no cumplen el mismo papel. Esta tabla indica qué lente aporta cada una;
después de leer, escribe una discrepancia real entre al menos dos fuentes.

| Fuente | Lente que aporta | Pregunta crítica |
|---|---|---|
{filas}

La lectura se evalúa por **uso**, no por cantidad de páginas. Tu nota de lectura debe indicar qué
tesis modifica tu diagnóstico, qué evidencia del caso la tensiona y qué decisión concreta
cambiarías después del contraste. Una nota que solo resume el texto no cumple el criterio."""


def ejemplo_trabajado(datos: dict, caso: str) -> str:
    conceptos = [c[0] for c in datos["conceptos"]]
    senales = [s[0] for s in senales_de_clase(datos)]
    pasos = metodo_de_clase(datos)
    guiones = [
        (f"El equipo escribe primero el supuesto asociado a **{conceptos[0]}** y se prohíbe "
         f"tratarlo como hecho. Contrasta ese supuesto con **{senales[0]}** y anota qué parte del "
         f"dato todavía no existe. Del paso sale un registro fechado y una frase explícita: "
         f"«cambiaríamos de decisión si…»."),
        (f"El trabajo aquí es separar lo observado de lo interpretado sobre **{conceptos[1]}**. "
         f"La evidencia que ordena la conversación es **{senales[1]}**; si su definición no está "
         f"escrita, escribirla es parte del paso. Nada avanza mientras el equipo no acuerde qué "
         f"contaría como refutación."),
        (f"El riesgo de este paso es cerrar demasiado rápido alrededor de **{conceptos[2]}**. "
         f"Antes de concluir, se enumeran dos explicaciones alternativas del mismo patrón y se "
         f"revisa si **{senales[2]}** logra distinguirlas. Si no lo logra, hace falta otra "
         f"evidencia y así debe quedar registrado."),
        (f"Con **{conceptos[3]}** ya delimitado, la pregunta pasa a ser de consecuencia: qué "
         f"cambia para los estudiantes, para el tiempo de clase y para la carga del equipo. "
         f"**{senales[0]}** entrega la lectura observable; el juicio profesional sigue siendo "
         f"humano y debe quedar firmado por quien lo hace."),
        (f"El cierre exige compromiso: responsable, fecha, indicador de logro y condición de "
         f"detención. **{senales[1]}** se convierte en la señal de seguimiento, y se acuerda con "
         f"qué frecuencia se revisa y quién puede declarar que no funcionó sin costo político."),
    ]
    # El rótulo del paso va en negrita, así que el énfasis interno de los conceptos se
    # retira: negrita dentro de negrita no se renderiza y ensucia el texto.
    cuerpo = "\n\n".join(
        f"**Paso {i} — {mayuscula(paso.replace('**', ''))}.** {guion}"
        for i, (paso, guion) in enumerate(zip(pasos, guiones), 1)
    )
    return f"""**Situación.** {caso}

{cuerpo}

**Síntesis.** La recomendación termina con responsable, fecha, evidencia de logro y señal de
detención. Omitir cualquiera de esas cuatro piezas convierte el análisis en una opinión que nadie
podrá auditar dentro de tres meses, y que por lo tanto nadie corregirá."""


def comparacion_de_caminos(datos: dict) -> str:
    conceptos = datos["conceptos"]
    senales = [s[0] for s in senales_de_clase(datos)]
    return f"""Ante la misma situación caben varios cursos de acción. La decisión profesional no es
elegir el «correcto», sino saber qué privilegia cada uno y qué arriesga.

| Camino | Qué privilegia | Cuándo elegirlo | Riesgo principal |
|---|---|---|---|
| Intervenir sobre **{conceptos[0][0]}** | {mayuscula(conceptos[0][1])} | Cuando **{senales[0]}** es observable y accionable dentro del plazo de la decisión. | Sobrerreaccionar a una señal parcial. |
| Intervenir sobre **{conceptos[1][0]}** | {mayuscula(conceptos[1][1])} | Cuando la primera explicación no distingue mecanismo ni responsable. | Convertir el concepto en etiqueta y no en intervención. |
| Observar antes de decidir | Reducir la incertidumbre antes de comprometer tiempo y credibilidad | Cuando la decisión es reversible y la evidencia disponible no distingue causas. | Observar indefinidamente y no decidir nunca. |
| Derivar o escalar | Poner la decisión donde están la competencia y la responsabilidad | Cuando hay normativa, resguardo de datos, salud o vulneración de derechos en juego. | Delegar hacia arriba lo que sí correspondía decidir en el aula. |

**Frontera de aplicación.** {frase(datos['limites'])} Fuera de esa frontera, la comparación
anterior deja de ser válida y la decisión debe tomarse con evidencia distinta."""


def mismo_tema_segun_rol(clase: dict) -> str:
    tema = minuscula(clase["title"])
    return f"""La misma materia cambia de forma según quién decida. Al subir de nivel aumentan las
personas, el tiempo y las consecuencias que quedan dentro de la decisión.

| Nivel | Responsabilidad sobre {tema} |
|---|---|
| **Docente de aula** | Aplica, observa y registra la evidencia; declara qué no puede resolver desde su rol. |
| **Equipo de apoyo o educación diferencial** | Verifica que la decisión no deje fuera a quien más barreras enfrenta y aporta los apoyos. |
| **Jefatura técnico-pedagógica** | Convierte la decisión en criterio compartido, tiempo protegido y acompañamiento. |
| **Dirección** | Decide si esto cambia condiciones institucionales, recursos o el plan de mejora. |
| **Formación e investigación** | Pregunta si la decisión es generalizable, con qué evidencia y qué haría falta para probarlo. |

Si trabajas en uno de esos niveles, la [guía de carrera de tu rol](../../../rutas/README.md)
indica en qué orden conviene recorrer el programa y qué artefactos acreditan tu competencia."""


def caso_profesional(caso: str) -> str:
    return f"""**Situación.** {caso}

Entrega un **informe de decisión** de una página que contenga:

1. **Hechos y fuentes** — qué está documentado y con qué evidencia, separado de lo que se supone.
2. **Hipótesis** — la explicación más probable y una alternativa que también encajaría.
3. **Dos opciones defendibles** — no una recomendación y un espantapájaros.
4. **Efecto esperado** — sobre los estudiantes, el tiempo de clase, el equipo y los apoyos.
5. **Recomendación** — con su fundamento y la fuente que la respalda.
6. **Condición de revisión** — qué resultado te haría cambiar de decisión.
7. **Responsable y fecha** — quién ejecuta y cuándo se revisa.

Usa al menos **dos** fuentes de la lectura comparada para desafiar tu primera respuesta. Una
recomendación que ninguna fuente pone en duda casi siempre está poco examinada."""


def evidencia(datos: dict, clase: dict, pack: dict) -> str:
    numero = clase["global_class"]
    slug = clase["slug"].split("-", 2)[-1]
    return f"""{mayuscula(datos['entregable'])}.

Guárdala en `evidence/P{clase['part']:02d}-C{numero:03d}-{slug}/` con estos archivos:

| Archivo | Qué contiene |
|---|---|
| `decision.md` | contexto, decisión, fundamento, fuentes con fecha, indicador de logro y riesgos |
| `senales.md` | definición operacional de las tres señales, cómo se recogieron y qué no distinguen |
| `nota-de-lectura.md` | dos fuentes contrastadas, con edición y páginas consultadas |
| `revision-critica.md` | la objeción más fuerte a tu decisión y qué evidencia la invalidaría |

Esta evidencia alimenta el artefacto de la parte: **{pack['artefacto']}**."""


def rubrica(pedagogia: dict) -> str:
    filas = "\n".join(
        f"| {criterio} | {peso} % | {evidencia} |"
        for criterio, peso, evidencia in pedagogia["rubrica_de_clase"]
    )
    return f"""| Criterio | Peso | Evidencia esperada |
|---|---:|---|
{filas}

**Aprobación:** 80 de 100 y ningún criterio bajo el 60 %. Una respuesta que podría copiarse sin
cambios a otra clase, a otro curso o a otro establecimiento se considera insuficiente, aunque
esté bien escrita."""


def errores(datos: dict, pack: dict) -> str:
    return f"""**Propios de esta clase:**

{vinetas(datos["errores"])}

**Característicos de la parte {pack['part']:02d}:**

{vinetas(pack['riesgos'][:2])}

Los cuatro comparten estructura: un síntoma visible, una causa que no se ve y una corrección que
casi siempre es de diseño y no de esfuerzo. Antes de atribuir el problema a los estudiantes o a
ti, comprueba cuál de ellos está operando y qué evidencia lo distinguiría de los otros tres."""


def contexto_chileno(pack: dict) -> str:
    return f"""Riesgo característico de esta parte: **{pack['riesgos'][0]}** Antes de aplicar
cualquier decisión de esta clase en un establecimiento real, verifica el marco vigente:

- Marco institucional y normativo: [`docs/MARCO_CHILE.md`](../../../docs/MARCO_CHILE.md).
- Inclusión y apoyos: [`docs/INCLUSION_Y_DUA.md`](../../../docs/INCLUSION_Y_DUA.md).
- Datos personales, IA y resguardos: [`docs/IA_EN_EDUCACION.md`](../../../docs/IA_EN_EDUCACION.md).
- Fuentes oficiales con cómo leerlas: [`docs/FUENTES.md`](../../../docs/FUENTES.md).

La regla del programa es simple: **la fuente oficial manda sobre el material pedagógico**. Si la
norma cambió después de la fecha de esta clase, gana la norma."""


def fuentes(datos: dict) -> str:
    lineas = "\n".join(
        f"- {referencia.replace('**', '')} **Uso en esta clase:** {nota} Lectura selectiva: "
        f"índice y capítulos pertinentes; registra edición y páginas consultadas. "
        f"{localizador(referencia, '../../../')}"
        for referencia, nota in datos["lecturas"]
    )
    return f"""{lineas}

Catálogo completo: [registro de fuentes con localizador](../../../docs/REGISTRO_DE_FUENTES.md) ·
[bibliografía del programa](../../../docs/BIBLIOGRAFIA.md) ·
[glosario](../../../docs/GLOSARIO.md) ·
[fuentes oficiales y cómo leerlas](../../../docs/FUENTES.md).

> **Regla de fuentes.** Las obras anteriores estructuran las perspectivas de esta materia.
> Cualquier norma, decreto, orientación ministerial o política institucional mencionada debe
> comprobarse en su fuente primaria vigente antes de usarse con estudiantes reales. El desarrollo
> de esta clase es original y no reproduce capítulos protegidos por derechos de autor."""


# --------------------------------------------------------------------------- #
# Página de clase
# --------------------------------------------------------------------------- #

def pagina_de_clase(clase: dict, datos: dict, pack: dict, etapa: dict, pedagogia: dict,
                    caso: str, vecinas: tuple[dict | None, dict | None]) -> str:
    anterior, siguiente = vecinas
    conceptos = "\n".join(f"| **{n}** | {d} |" for n, d in datos["conceptos"])
    contextos = "\n".join(f"| {n} | {r} |" for n, r in pack["contextos"])
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

## 🧭 Agenda sugerida (90 minutos)

{agenda(datos)}

## 🧩 Conceptos centrales

| Concepto | Comprensión verificable |
|---|---|
{conceptos}

## 🧠 Modelo mental

{modelo_mental(datos)}

## 🗺️ Flujo de razonamiento

{mapa_de_clase(datos)}

## 📖 Desarrollo

{desarrollo(datos, pack, nivel)}

## 📚 Lectura comparada

{lectura_comparada(datos)}

## 🧮 Ejemplo trabajado

{ejemplo_trabajado(datos, caso)}

## 🔀 Comparación de caminos y límites

{comparacion_de_caminos(datos)}

## 🪜 El mismo tema según el rol

{mismo_tema_segun_rol(clase)}

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

## 🏫 Caso profesional

{caso_profesional(caso)}

## 📥 Evidencia de aprendizaje

{evidencia(datos, clase, pack)}

## 🏆 Reto verificable

{datos['reto']}

## ✅ Evaluación de la clase

{rubrica(pedagogia)}

**Criterio de logro de la evidencia:**

{casillas(datos['criterios'] + pedagogia['criterios_comunes'])}

## ⚠️ Errores frecuentes

{errores(datos, pack)}

## ♿ Diversidad, accesibilidad y ética

{datos['inclusion']}

Antes de aplicar cualquier decisión de esta clase con estudiantes reales, revisa el
[protocolo de práctica responsable](../../../docs/ETICA_Y_PRACTICA_RESPONSABLE.md):
consentimiento, resguardo de datos personales, proporcionalidad de la intervención y derecho
de cada estudiante a no ser objeto de un ensayo que no le reporta beneficio.

## 🇨🇱 Contexto chileno y cumplimiento

{contexto_chileno(pack)}

## ❓ Preguntas de comprobación

{numerada(datos['preguntas'])}

## 📗 Fuentes y verificación

{fuentes(datos)}

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
                    caso: dict, vecinas: tuple[dict | None, dict | None]) -> str:
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
    senales = len(clases) * 3
    lecturas = vinetas([f"**{ref}** — {nota} {localizador(ref, '../../')}"
                        for ref, nota in pack["lecturas"]])
    resumen = "\n\n".join(pack["resumen"])
    return f"""# Parte {pack['part']:02d} — {pack['titulo']}

> *{pack['lema']}*

{etapa['emoji']} **{etapa['nombre']}** · salida de la etapa: {etapa['salida']}

**Clases:** 12 ({clases[0]['global_class']:03d}–{clases[-1]['global_class']:03d}) · \
**Población de referencia:** {pack['poblacion']} · \
**Conceptos operacionales:** {conceptos} · **Señales observables:** {senales}<br>
**Contenido central:** {pack['contenido_central']}

## 🎯 De qué trata esta parte

{resumen}

## 🏫 Caso de la parte

Las doce clases trabajan sobre la misma realidad, para que puedas ver cómo cambia tu diagnóstico
a medida que avanzas:

> {caso['caso']}

**Artefacto que produces al terminar:** {caso['artefacto']}.

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

## 🧭 Práctica y evaluación de la parte

- [Rúbrica maestra e instrumentos de autoevaluación](../../assessments/README.md)
- [Casos profesionales para resolver con este marco](../../cases/README.md)
- [Laboratorios de decisión](../../labs/README.md)
- [Dónde se archiva la evidencia](../../evidence/README.md)

---

| Anterior | Índice | Siguiente |
|---|---|---|
| {nav_anterior} | [Programa](../../README.md) · [Currículo](../../CURRICULUM.md) | {nav_siguiente} |
"""


# --------------------------------------------------------------------------- #
# Ejecución
# --------------------------------------------------------------------------- #

def construir(parcial: bool = False) -> dict[Path, str]:
    curriculo, packs, datos, etapas, pedagogia, casos = cargar()
    faltan = [c["global_class"] for c in curriculo if c["global_class"] not in datos]
    if faltan and not parcial:
        raise SystemExit(f"faltan {len(faltan)} clases en manifests/classes/: {faltan[:12]}…")
    if faltan:
        print(f"AVISO: modo parcial, {len(faltan)} clase(s) sin manifiesto se omiten.")
        curriculo = [c for c in curriculo if c["global_class"] not in faltan]
        packs = [p for p in packs if any(c["part"] == p["part"] for c in curriculo)]

    packs_por_numero = {p["part"]: p for p in packs}
    archivos: dict[Path, str] = {}

    for indice, clase in enumerate(curriculo):
        pack = packs_por_numero[clase["part"]]
        pack = {**pack, "artefacto": casos["partes"][str(clase["part"])]["artefacto"]}
        etapa = etapas[pack["etapa"]]
        vecinas = (
            curriculo[indice - 1] if indice > 0 else None,
            curriculo[indice + 1] if indice + 1 < len(curriculo) else None,
        )
        destino = CURRICULO / clase["part_slug"] / clase["slug"] / "README.md"
        archivos[destino] = pagina_de_clase(
            clase, datos[clase["global_class"]], pack, etapa, pedagogia,
            casos["partes"][str(clase["part"])]["caso"], vecinas,
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
        archivos[destino] = pagina_de_parte(
            pack, clases, etapa, datos, casos["partes"][str(pack["part"])], vecinas
        )

    return archivos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si el árbol no coincide con los manifiestos")
    parser.add_argument("--parcial", action="store_true",
                        help="genera solo las clases completas (uso durante la redacción)")
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
