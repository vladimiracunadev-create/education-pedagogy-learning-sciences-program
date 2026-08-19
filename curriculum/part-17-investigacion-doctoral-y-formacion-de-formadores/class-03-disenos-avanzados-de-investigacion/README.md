# Clase 207 — Diseños avanzados de investigación

> **Parte 17 · Investigación doctoral y formación de formadores** — clase 3 de 12

**Estado de evidencia:** `ROBUSTA` · **Etapa:** 🔴 Etapa E — Investigación avanzada y formación de formadores · **Población de referencia:** nivel doctoral, dirección de tesis y formación docente<br>
**Decisión que habilita:** determinar qué diseño avanzado corresponde a la estructura real de tu problema y de tus datos<br>
**Evidencia de aprendizaje:** la justificación de un diseño avanzado con sus supuestos, sus amenazas y su plan de análisis

## 🎯 Propósito

Seleccionar diseños avanzados —longitudinales, con series temporales, con variables instrumentales, con emparejamiento— según la estructura del problema y los datos disponibles.

## 📚 Resultados de aprendizaje

Al finalizar esta clase podrás:

1. **Definir** con precisión los cuatro conceptos centrales de la clase y reconocerlos en una situación educativa real, no solo en su enunciado.
2. **Explicar** qué diseños permiten responder preguntas que los diseños básicos no alcanzan.
3. **Decidir** —qué diseño avanzado corresponde a la estructura real de tu problema y de tus datos— y sostener la decisión con un fundamento escrito.
4. **Producir** la evidencia de la clase —la justificación de un diseño avanzado con sus supuestos, sus amenazas y su plan de análisis— y contrastarla contra el criterio de logro.
5. **Distinguir** lo que la evidencia sostiene de lo que es práctica instalada, preferencia personal o costumbre de la institución.

## 🧭 Agenda sugerida (90 minutos)

| Minutos | Bloque | Qué ocurre |
|---:|---|---|
| 0–10 | Activación | Recuperar sin mirar la clase anterior y responder la pregunta de foco. |
| 10–25 | Conceptos | Definir los cuatro conceptos y reconocerlos en un caso real. |
| 25–45 | Modelo mental | Recorrer el método: delimitar el contexto y comprobar —no suponer— qué saben ya los estudiantes. |
| 45–70 | Ejemplo trabajado | Aplicar el método al caso de la parte, paso a paso y con evidencia. |
| 70–85 | Taller | Trasladar la decisión al contexto propio y anticipar su alternativa. |
| 85–90 | Cierre | Fijar responsable, plazo e indicador de la evidencia de aprendizaje. |

Fuera de la sesión, la clase exige aproximadamente **una hora y media** de práctica y de
producción de la evidencia. Si el tiempo se recorta, se recorta el ejemplo trabajado, nunca la
producción de evidencia: es la única parte que prueba el aprendizaje.

## 🧩 Conceptos centrales

| Concepto | Comprensión verificable |
|---|---|
| **Diseño longitudinal** | medición repetida de los mismos sujetos que permite estudiar trayectorias y cambio |
| **Emparejamiento** | procedimiento que construye grupos comparables a partir de características observadas |
| **Discontinuidad en la regresión** | diseño que aprovecha un punto de corte administrativo para estimar efectos |
| **Supuesto de identificación** | condición que debe cumplirse para que el diseño permita la inferencia causal declarada |

## 🧠 Modelo mental

El método de esta clase, en cinco pasos que se ejecutan en orden:

1. Delimitar el contexto y comprobar —no suponer— qué saben ya los estudiantes.
2. Clasificar la situación distinguiendo **Diseño longitudinal** de **Emparejamiento**.
3. Decidir con fundamento, usando **Discontinuidad en la regresión** como criterio y declarando la fuente.
4. Anticipar qué evidencia confirmaría la decisión y cuál la refutaría, con **Supuesto de identificación** a la vista.
5. Registrar lo ocurrido y contrastarlo contra el criterio de logro antes de avanzar.

Lo que hace profesional a este método no son los pasos sino la evidencia que exige en cada uno.
Estas son las señales observables con las que se comprueba, y que deben quedar definidas **antes**
de recogerlas:

| Señal observable | Cómo se recoge y qué significa |
|---|---|
| **Evidencia de partida** | qué sabían o podían hacer los estudiantes antes de la decisión, comprobado y no supuesto |
| **Evidencia de proceso** | qué se observó mientras la decisión se aplicaba, con fecha, contexto y responsable del registro |
| **Evidencia de logro** | qué muestra la justificación de un diseño avanzado con sus supuestos, sus amenazas y su plan de análisis frente al criterio declarado de antemano |

**Frontera de aplicación.** El método vale mientras las condiciones que lo sostienen se cumplan.
Estos diseños exigen competencia estadística específica y, en muchos casos, colaboración con especialistas. Cuando esa condición falla, el paso siguiente no es forzar el método:
es declarar el límite y decidir con menos certeza, dejándolo por escrito.

## 🗺️ Flujo de razonamiento

```mermaid
flowchart TB
    C["Situacion educativa<br/>nivel · grupo · proposito"]
    C --> A1["Diseño longitudinal"]
    C --> A2["Emparejamiento"]
    C --> A3["Discontinuidad en la<br/>regresión"]
    C --> A4["Supuesto de<br/>identificación"]
    A1 & A2 & A3 & A4 --> D{{"determinar qué diseño<br/>avanzado corresponde a<br/>la estructura real de tu<br/>problema y de tus datos"}}
    D --> E["Evidencia de aprendizaje<br/>la justificación de un<br/>diseño avanzado con sus<br/>supuestos, sus amenazas<br/>y su plan de análisis"]
    E --> V{"Cumple el<br/>criterio de logro?"}
    V -->|si| S["Evidencia archivada<br/>y clase siguiente"]
    V -->|no| C
```

## 📖 Desarrollo

### 1. El fondo del asunto

Los diseños avanzados no son técnicas más sofisticadas por sí mismas: son estrategias para identificar efectos cuando la aleatorización no es posible. Cada uno descansa en supuestos de identificación que deben declararse y, cuando es posible, someterse a prueba. Un diseño avanzado con supuestos incumplidos produce estimaciones precisas de algo que no es el efecto buscado. Conviene tener presente el orden real de trabajo: primero se examina qué generó la variación observada en el mundo, y solo después se elige la técnica que puede aprovecharla.

### 2. Frontera conceptual: qué es y qué no es

Los cuatro conceptos de esta clase se confunden entre sí con facilidad, y esa confusión no es
inocua: produce decisiones que atacan el problema equivocado. **Diseño longitudinal** no es lo
mismo que **Emparejamiento** —procedimiento que construye grupos comparables a partir de características observadas—, y tratarlos como sinónimos hace
que la intervención se dirija al lugar incorrecto. Del mismo modo, **Discontinuidad en la regresión** y
**Supuesto de identificación** describen aspectos distintos de la misma situación: el primero
diseño que aprovecha un punto de corte administrativo para estimar efectos, mientras el segundo condición que debe cumplirse para que el diseño permita la inferencia causal declarada.

La prueba de que la distinción está entendida es operacional, no verbal: dos personas que
observan la misma clase deben poder clasificar el mismo episodio de la misma manera. Si no
coinciden, el problema está en la definición y no en el observador. El error de clasificación más
frecuente en esta materia es el primero de los que se listan más abajo, y conviene anticiparlo
antes de aplicar nada.

### 3. Cómo se observa y se mide

Nada de lo anterior sirve si no se puede observar. Estas son las señales que esta clase usa y
cómo se recogen:

- **Evidencia de partida.** Qué sabían o podían hacer los estudiantes antes de la decisión, comprobado y no supuesto. Se registra con fecha y contexto; sin eso, la señal no distingue una tendencia de una casualidad.
- **Evidencia de proceso.** Qué se observó mientras la decisión se aplicaba, con fecha, contexto y responsable del registro. Se registra con fecha y contexto; sin eso, la señal no distingue una tendencia de una casualidad.
- **Evidencia de logro.** Qué muestra la justificación de un diseño avanzado con sus supuestos, sus amenazas y su plan de análisis frente al criterio declarado de antemano. Se registra con fecha y contexto; sin eso, la señal no distingue una tendencia de una casualidad.

Ninguna de estas señales es el aprendizaje: son indicios de él. Confundir el indicio con el
fenómeno es el error clásico de la medición educativa, y por eso cada señal se interpreta junto
con el contexto, el punto de partida del grupo y lo que el propio estudiante puede explicar sobre
su trabajo.

### 4. Cómo se traduce en decisiones de enseñanza

La elección parte de la estructura del problema y de los datos existentes: si hay un punto de corte administrativo, si hay mediciones repetidas, si hay una fuente de variación exógena. En educación, los datos administrativos ofrecen oportunidades reales para estos diseños, y su uso exige tanto competencia técnica como resguardo de los datos. Antes de comprometerse conviene escribir el supuesto de identificación en lenguaje corriente y mostrárselo a alguien del establecimiento: si esa persona conoce una razón por la que el supuesto no se cumple, el diseño se cae ahí y no seis meses después.

### 5. Qué sostiene la evidencia y qué no

Estos diseños exigen competencia estadística específica y, en muchos casos, colaboración con especialistas. Además, sus supuestos son fuertes y en ocasiones no verificables: la honestidad consiste en declararlos y en analizar la sensibilidad de los resultados a su incumplimiento. Hay además un límite de alcance que se comunica mal: varios de estos diseños estiman el efecto para un subgrupo particular —quienes están cerca del punto de corte, por ejemplo— y ese resultado no autoriza a hablar del efecto para toda la población.

> **Cómo leer el estado de evidencia `ROBUSTA`.** Hay evidencia convergente de varios equipos, países y diseños de investigación, incluidos estudios experimentales o cuasiexperimentales, y el efecto se sostiene al replicarlo. Puedes apoyar una decisión profesional en ella, sin olvidar que ningún efecto promedio describe a un estudiante concreto.

### 6. Integración: de los conceptos a una decisión defendible

Una decisión es defendible cuando puede explicarse a alguien que no estuvo presente. Esta clase
te deja en condiciones de qué diseño avanzado corresponde a la estructura real de tu problema y de tus datos, y esa decisión se sostiene solo si
declara cuatro cosas: la evidencia que la funda, el supuesto que asume, el indicador que la
comprobaría y la condición que la haría cambiar.

Ese es también el criterio con el que se evalúa la evidencia de aprendizaje de la clase. Un
análisis que podría copiarse a otra clase, a otro curso o a otro establecimiento sin cambiar una
palabra no es una decisión: es una declaración general, y el oficio empieza justo donde las
declaraciones generales terminan.

## 📚 Lectura comparada

Las obras no cumplen el mismo papel. Esta tabla indica qué lente aporta cada una;
después de leer, escribe una discrepancia real entre al menos dos fuentes.

| Fuente | Lente que aporta | Pregunta crítica |
|---|---|---|
| Angrist, J. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. | tratamiento accesible de diseños de identificación causal aplicables a datos educativos. | ¿Qué supuesto de esta clase ayuda a poner a prueba? |
| Murnane, R. & Willett, J. (2011). *Methods Matter*. | aplica estos diseños específicamente a preguntas de investigación educativa. | ¿Qué supuesto de esta clase ayuda a poner a prueba? |

La lectura se evalúa por **uso**, no por cantidad de páginas. Tu nota de lectura debe indicar qué
tesis modifica tu diagnóstico, qué evidencia del caso la tensiona y qué decisión concreta
cambiarías después del contraste. Una nota que solo resume el texto no cumple el criterio.

## 🧮 Ejemplo trabajado

**Situación.** La red quiere formar a sus 42 docentes con un programa propio y sostenerlo tres años. El diseño inicial es un taller de ocho horas por semestre, sin acompañamiento en el aula y con evaluación por encuesta de satisfacción.

**Paso 1 — Delimitar el contexto y comprobar —no suponer— qué saben ya los estudiantes.** El equipo escribe primero el supuesto asociado a **Diseño longitudinal** y se prohíbe tratarlo como hecho. Contrasta ese supuesto con **Evidencia de partida** y anota qué parte del dato todavía no existe. Del paso sale un registro fechado y una frase explícita: «cambiaríamos de decisión si…».

**Paso 2 — Clasificar la situación distinguiendo Diseño longitudinal de Emparejamiento.** El trabajo aquí es separar lo observado de lo interpretado sobre **Emparejamiento**. La evidencia que ordena la conversación es **Evidencia de proceso**; si su definición no está escrita, escribirla es parte del paso. Nada avanza mientras el equipo no acuerde qué contaría como refutación.

**Paso 3 — Decidir con fundamento, usando Discontinuidad en la regresión como criterio y declarando la fuente.** El riesgo de este paso es cerrar demasiado rápido alrededor de **Discontinuidad en la regresión**. Antes de concluir, se enumeran dos explicaciones alternativas del mismo patrón y se revisa si **Evidencia de logro** logra distinguirlas. Si no lo logra, hace falta otra evidencia y así debe quedar registrado.

**Paso 4 — Anticipar qué evidencia confirmaría la decisión y cuál la refutaría, con Supuesto de identificación a la vista.** Con **Supuesto de identificación** ya delimitado, la pregunta pasa a ser de consecuencia: qué cambia para los estudiantes, para el tiempo de clase y para la carga del equipo. **Evidencia de partida** entrega la lectura observable; el juicio profesional sigue siendo humano y debe quedar firmado por quien lo hace.

**Paso 5 — Registrar lo ocurrido y contrastarlo contra el criterio de logro antes de avanzar.** El cierre exige compromiso: responsable, fecha, indicador de logro y condición de detención. **Evidencia de proceso** se convierte en la señal de seguimiento, y se acuerda con qué frecuencia se revisa y quién puede declarar que no funcionó sin costo político.

**Síntesis.** La recomendación termina con responsable, fecha, evidencia de logro y señal de
detención. Omitir cualquiera de esas cuatro piezas convierte el análisis en una opinión que nadie
podrá auditar dentro de tres meses, y que por lo tanto nadie corregirá.

## 🔀 Comparación de caminos y límites

Ante la misma situación caben varios cursos de acción. La decisión profesional no es
elegir el «correcto», sino saber qué privilegia cada uno y qué arriesga.

| Camino | Qué privilegia | Cuándo elegirlo | Riesgo principal |
|---|---|---|---|
| Intervenir sobre **Diseño longitudinal** | Medición repetida de los mismos sujetos que permite estudiar trayectorias y cambio | Cuando **Evidencia de partida** es observable y accionable dentro del plazo de la decisión. | Sobrerreaccionar a una señal parcial. |
| Intervenir sobre **Emparejamiento** | Procedimiento que construye grupos comparables a partir de características observadas | Cuando la primera explicación no distingue mecanismo ni responsable. | Convertir el concepto en etiqueta y no en intervención. |
| Observar antes de decidir | Reducir la incertidumbre antes de comprometer tiempo y credibilidad | Cuando la decisión es reversible y la evidencia disponible no distingue causas. | Observar indefinidamente y no decidir nunca. |
| Derivar o escalar | Poner la decisión donde están la competencia y la responsabilidad | Cuando hay normativa, resguardo de datos, salud o vulneración de derechos en juego. | Delegar hacia arriba lo que sí correspondía decidir en el aula. |

**Frontera de aplicación.** Estos diseños exigen competencia estadística específica y, en muchos casos, colaboración con especialistas. Fuera de esa frontera, la comparación
anterior deja de ser válida y la decisión debe tomarse con evidencia distinta.

## 🪜 El mismo tema según el rol

La misma materia cambia de forma según quién decida. Al subir de nivel aumentan las
personas, el tiempo y las consecuencias que quedan dentro de la decisión.

| Nivel | Responsabilidad sobre diseños avanzados de investigación |
|---|---|
| **Docente de aula** | Aplica, observa y registra la evidencia; declara qué no puede resolver desde su rol. |
| **Equipo de apoyo o educación diferencial** | Verifica que la decisión no deje fuera a quien más barreras enfrenta y aporta los apoyos. |
| **Jefatura técnico-pedagógica** | Convierte la decisión en criterio compartido, tiempo protegido y acompañamiento. |
| **Dirección** | Decide si esto cambia condiciones institucionales, recursos o el plan de mejora. |
| **Formación e investigación** | Pregunta si la decisión es generalizable, con qué evidencia y qué haría falta para probarlo. |

Si trabajas en uno de esos niveles, la [guía de carrera de tu rol](../../../rutas/README.md)
indica en qué orden conviene recorrer el programa y qué artefactos acreditan tu competencia.

## 🧪 Taller guiado

Aplica la clase a **uno** de los contextos siguientes y repite después el ejercicio en un
contexto de exigencia distinta. Cambiar de contexto es parte del aprendizaje: lo que funciona
con un grupo no se traslada intacto a otro.

| Contexto | Rasgo que cambia la decisión |
|---|---|
| Tesis doctoral en curso | la contribución debe delimitarse y defenderse |
| Investigación con datos anidados | estudiantes en cursos, cursos en escuelas |
| Síntesis de evidencia acumulada | calidad de estudios y sesgo de publicación |
| Investigación basada en diseño | intervención y teoría se construyen a la vez |
| Dirección de tesis de otros | el método pasa a ser la relación de supervisión |
| Programa de formación docente | el criterio final es el cambio en la práctica |

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

**Situación.** La red quiere formar a sus 42 docentes con un programa propio y sostenerlo tres años. El diseño inicial es un taller de ocho horas por semestre, sin acompañamiento en el aula y con evaluación por encuesta de satisfacción.

Entrega un **informe de decisión** de una página que contenga:

1. **Hechos y fuentes** — qué está documentado y con qué evidencia, separado de lo que se supone.
2. **Hipótesis** — la explicación más probable y una alternativa que también encajaría.
3. **Dos opciones defendibles** — no una recomendación y un espantapájaros.
4. **Efecto esperado** — sobre los estudiantes, el tiempo de clase, el equipo y los apoyos.
5. **Recomendación** — con su fundamento y la fuente que la respalda.
6. **Condición de revisión** — qué resultado te haría cambiar de decisión.
7. **Responsable y fecha** — quién ejecuta y cuándo se revisa.

Usa al menos **dos** fuentes de la lectura comparada para desafiar tu primera respuesta. Una
recomendación que ninguna fuente pone en duda casi siempre está poco examinada.

## 📥 Evidencia de aprendizaje

La justificación de un diseño avanzado con sus supuestos, sus amenazas y su plan de análisis.

Guárdala en `evidence/P17-C207-disenos-avanzados-de-investigacion/` con estos archivos:

| Archivo | Qué contiene |
|---|---|
| `decision.md` | contexto, decisión, fundamento, fuentes con fecha, indicador de logro y riesgos |
| `senales.md` | definición operacional de las tres señales, cómo se recogieron y qué no distinguen |
| `nota-de-lectura.md` | dos fuentes contrastadas, con edición y páginas consultadas |
| `revision-critica.md` | la objeción más fuerte a tu decisión y qué evidencia la invalidaría |

Esta evidencia alimenta el artefacto de la parte: **propuesta doctoral defendible y programa de formación de formadores con acompañamiento en el puesto y evaluación de cambio de práctica**.

## 🏆 Reto verificable

Escoge un diseño avanzado para tu pregunta y escribe sus supuestos. Diseña una prueba de sensibilidad para el supuesto más frágil.

## ✅ Evaluación de la clase

| Criterio | Peso | Evidencia esperada |
|---|---:|---|
| Precisión conceptual | 25 % | Distinciones correctas y observables entre los cuatro conceptos, aplicadas a un caso real. |
| Diagnóstico y evidencia | 30 % | Conocimiento previo comprobado, evidencia recogida con fecha y contexto, y límites del dato declarados. |
| Decisión y alternativas | 30 % | Decisión fundada, alternativa prevista si falla, y condición explícita que la haría cambiar. |
| Responsabilidad y comunicación | 15 % | Diversidad y resguardos considerados, fuentes citadas y evidencia archivada de forma reproducible. |

**Aprobación:** 80 de 100 y ningún criterio bajo el 60 %. Una respuesta que podría copiarse sin
cambios a otra clase, a otro curso o a otro establecimiento se considera insuficiente, aunque
esté bien escrita.

**Criterio de logro de la evidencia:**

- [ ] los supuestos de identificación están declarados y, cuando es posible, examinados;
- [ ] el plan de análisis incluye pruebas de sensibilidad a los supuestos clave;
- [ ] cada afirmación sobre «lo que funciona» está atribuida a una fuente identificable, con autor y fecha;
- [ ] la decisión es ejecutable con el tiempo, el espacio, el número de estudiantes y los recursos que realmente tienes;
- [ ] la evidencia queda archivada de forma reproducible: otra persona podría revisarla sin que tú se la expliques.

## ⚠️ Errores frecuentes

**Propios de esta clase:**

- Aplicar un diseño avanzado sin declarar ni examinar sus supuestos de identificación.
- Presentar la sofisticación técnica como sustituto de la validez del constructo medido.

**Característicos de la parte 17:**

- Confundir novedad temática con contribución al conocimiento.
- Analizar datos anidados como si fueran independientes.

Los cuatro comparten estructura: un síntoma visible, una causa que no se ve y una corrección que
casi siempre es de diseño y no de esfuerzo. Antes de atribuir el problema a los estudiantes o a
ti, comprueba cuál de ellos está operando y qué evidencia lo distinguiría de los otros tres.

## ♿ Diversidad, accesibilidad y ética

Los diseños basados en datos administrativos suelen subrepresentar a estudiantes con trayectorias interrumpidas, que son quienes desaparecen de los registros. Analizar quién falta es parte del análisis, no una limitación menor.

Antes de aplicar cualquier decisión de esta clase con estudiantes reales, revisa el
[protocolo de práctica responsable](../../../docs/ETICA_Y_PRACTICA_RESPONSABLE.md):
consentimiento, resguardo de datos personales, proporcionalidad de la intervención y derecho
de cada estudiante a no ser objeto de un ensayo que no le reporta beneficio.

## 🇨🇱 Contexto chileno y cumplimiento

Riesgo característico de esta parte: **Confundir novedad temática con contribución al conocimiento.** Antes de aplicar
cualquier decisión de esta clase en un establecimiento real, verifica el marco vigente:

- Marco institucional y normativo: [`docs/MARCO_CHILE.md`](../../../docs/MARCO_CHILE.md).
- Inclusión y apoyos: [`docs/INCLUSION_Y_DUA.md`](../../../docs/INCLUSION_Y_DUA.md).
- Datos personales, IA y resguardos: [`docs/IA_EN_EDUCACION.md`](../../../docs/IA_EN_EDUCACION.md).
- Fuentes oficiales con cómo leerlas: [`docs/FUENTES.md`](../../../docs/FUENTES.md).

La regla del programa es simple: **la fuente oficial manda sobre el material pedagógico**. Si la
norma cambió después de la fecha de esta clase, gana la norma.

## ❓ Preguntas de comprobación

1. ¿Qué supuesto debe cumplirse para que tu estimación signifique lo que dices?
2. ¿Qué ocurre con tus conclusiones si ese supuesto falla parcialmente?
3. ¿Necesitas colaborar con un especialista en este diseño?

## 📗 Fuentes y verificación

- Angrist, J. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. **Uso en esta clase:** tratamiento accesible de diseños de identificación causal aplicables a datos educativos. Lectura selectiva: índice y capítulos pertinentes; registra edición y páginas consultadas.
- Murnane, R. & Willett, J. (2011). *Methods Matter*. **Uso en esta clase:** aplica estos diseños específicamente a preguntas de investigación educativa. Lectura selectiva: índice y capítulos pertinentes; registra edición y páginas consultadas.

Catálogo completo: [bibliografía del programa](../../../docs/BIBLIOGRAFIA.md) ·
[glosario](../../../docs/GLOSARIO.md) ·
[fuentes oficiales y cómo leerlas](../../../docs/FUENTES.md).

> **Regla de fuentes.** Las obras anteriores estructuran las perspectivas de esta materia.
> Cualquier norma, decreto, orientación ministerial o política institucional mencionada debe
> comprobarse en su fuente primaria vigente antes de usarse con estudiantes reales. El desarrollo
> de esta clase es original y no reproduce capítulos protegidos por derechos de autor.

## 🔗 Conexión con el resto del programa

Profundiza la clase 197 y se complementa con la clase 208.

> [!IMPORTANT]
> Material de formación profesional. No reemplaza un título de pedagogía, una habilitación
> legal para ejercer, ni el juicio de un equipo educativo que conoce a sus estudiantes.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [← 206 · Contribución al conocimiento](../class-02-contribucion-al-conocimiento/README.md) | [Parte 17](../README.md) · [Programa](../../../README.md) | [208 · Modelos longitudinales y multinivel →](../class-04-modelos-longitudinales-y-multinivel/README.md) |
