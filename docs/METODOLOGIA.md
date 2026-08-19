# Metodología del programa

Cómo está construido este programa, por qué cada clase tiene la forma que tiene y qué se exige
para dar un contenido por aprendido.

## 1. El principio que ordena todo

> Una clase no termina cuando se leyó. Termina cuando existe una evidencia observable de que
> alguien puede hacer algo que antes no podía.

De ahí se derivan las tres decisiones estructurales del programa:

1. **Cada clase habilita una decisión profesional**, no cubre un tema. El tema es el medio.
2. **Cada clase exige una evidencia de aprendizaje** concreta, con criterios de logro escritos
   antes de producirla.
3. **Cada clase declara el estado de la evidencia** que la sostiene, para que nadie confunda un
   hallazgo replicado con una tradición del oficio.

## 2. El ciclo pedagógico

Cada clase recorre el mismo ciclo, y las 300 lo repiten para que se vuelva un hábito
profesional:

```text
activar → comprender → modelar → practicar → retroalimentar → aplicar → evaluar → reflexionar
```

| Momento | Dónde ocurre en la clase |
|---|---|
| activar | propósito, pregunta de foco y conexión con el conocimiento previo |
| comprender | conceptos centrales con definición operacional y desarrollo |
| modelar | el apartado *Cómo se traduce en decisiones de enseñanza* |
| practicar | taller guiado, con contextos alternativos |
| retroalimentar | criterios de logro y preguntas de comprobación |
| aplicar | evidencia de aprendizaje, producida en un contexto real o simulado |
| evaluar | contraste contra el criterio de logro antes de avanzar |
| reflexionar | reto verificable y conexión con el resto del programa |

## 3. El contrato de cada clase

Toda clase contiene exactamente estas secciones, y el CI falla si falta alguna:

| Sección | Qué garantiza |
|---|---|
| Propósito | que exista una razón profesional para la clase |
| Resultados de aprendizaje | que el logro sea verificable, no declarativo |
| Conceptos centrales | cuatro términos con definición operacional, no de diccionario |
| Flujo de razonamiento | un diagrama que muestra cómo se decide, no qué se memoriza |
| Desarrollo en tres capas | fondo del asunto · traducción a decisiones · qué sostiene la evidencia y qué no |
| Taller guiado | práctica en un contexto declarado, repetida en un contexto distinto |
| Evidencia de aprendizaje | el producto que prueba el logro |
| Reto verificable | una aplicación que exige salir del material |
| Criterio de logro | dos criterios propios más tres comunes a todo el programa |
| Errores frecuentes | dos propios de la clase y dos característicos de la parte |
| Diversidad, accesibilidad y ética | qué cambia para los estudiantes con más barreras |
| Preguntas de comprobación | tres preguntas que exponen la comprensión superficial |
| Lecturas base | dos o tres fuentes con la razón de esa lectura y no de otra |
| Conexión con el programa | dónde se apoya y dónde se usa después |

## 4. Los tres criterios comunes

Además de sus criterios propios, toda evidencia de aprendizaje del programa debe cumplir:

1. cada afirmación sobre «lo que funciona» está atribuida a una fuente identificable, con autor
   y fecha;
2. la decisión es ejecutable con el tiempo, el espacio, el número de estudiantes y los recursos
   que realmente tienes;
3. la evidencia queda archivada de forma reproducible: otra persona podría revisarla sin que tú
   se la expliques.

El tercero es el más exigente y el que más distingue a un profesional: obliga a documentar.

## 5. Por qué el contenido se genera y no se escribe a mano

El currículo vive en `manifests/` y se genera en `curriculum/` con
`python scripts/generar_clases.py`. Esa decisión tiene tres consecuencias prácticas:

- **Coherencia estructural garantizada.** Ninguna clase puede quedarse sin criterios de logro o
  sin declarar su estado de evidencia: el generador no lo permite.
- **Cambios globales baratos.** Mejorar el contrato pedagógico de las 300 clases es una
  modificación en un solo lugar.
- **Verificabilidad.** El CI comprueba que lo publicado coincide exactamente con la fuente. Si
  alguien edita una clase a mano, la validación falla.

La arquitectura completa está en [ARQUITECTURA.md](ARQUITECTURA.md).

## 6. Qué hace este programa distinto

- **No promete lo que la evidencia no sostiene.** Cada clase declara sus límites en una sección
  propia, y el programa completo declara su distribución de estados de evidencia en
  [STATUS.md](../STATUS.md).
- **Trata los neuromitos de frente.** Estilos de aprendizaje, hemisferio dominante y ventanas
  críticas irreversibles se abordan explícitamente en [ESTANDARES_DE_EVIDENCIA.md](ESTANDARES_DE_EVIDENCIA.md).
- **Separa lo que es norma de lo que es evidencia.** Un decreto no es un hallazgo, y una
  costumbre institucional tampoco.
- **Exige contexto.** Cada taller se aplica en un contexto declarado y se repite en otro, porque
  ninguna decisión pedagógica se traslada intacta entre poblaciones.
- **Pone la ética antes que la práctica.** Ninguna actividad del programa se aplica con
  estudiantes reales sin pasar por el
  [protocolo de práctica responsable](ETICA_Y_PRACTICA_RESPONSABLE.md).

## 7. Cómo se decide que una parte está cerrada

No por haber leído las 12 clases. Cada parte declara su **evidencia mínima**: un conjunto de
productos que deben existir y poder revisarse. La regla de avance del programa es:

1. evidencia práctica producida;
2. autoevaluación con la rúbrica del programa;
3. revisión por un par cuando sea posible;
4. reflexión escrita sobre qué cambió en tu práctica;
5. proyecto integrador de la parte.

## 8. Límites del programa

- Es un programa de **formación profesional y autoformación**: no otorga título, grado ni
  habilitación legal para ejercer.
- Su contenido normativo es **Chile-first** y debe verificarse en la fuente oficial vigente.
- Su evidencia proviene mayoritariamente de investigación internacional; **la aplicación local
  exige comprobación en tu propio contexto**, y eso es parte del método, no una limitación
  vergonzante.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [Glosario](GLOSARIO.md) | [Programa](../README.md) · [Documentos](../FILE_INDEX.md) | [Ética y práctica responsable](ETICA_Y_PRACTICA_RESPONSABLE.md) |
