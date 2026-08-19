# Estado del programa

Cifras verificables contra el repositorio. Ninguna se escribe a mano: este archivo lo genera
`scripts/generar_indice.py` desde los manifiestos, y el CI comprueba en cada push que siga
coincidiendo con lo publicado.

## Contenido

| Métrica | Valor |
|---|---:|
| Versión | 1.1.0 |
| Etapas | 5 |
| Partes | 18 |
| Clases | 216 |
| Clases por parte | 12 |
| Palabras en las 216 clases | 301.694 |
| Palabras por clase | 1302–1577 (mediana 1384) |
| Diagramas mermaid | 234 (uno por clase y uno por parte) |
| Conceptos con definición operacional | 864 |
| Decisiones profesionales habilitadas | 216 (una por clase) |
| Evidencias de aprendizaje definidas | 216 |
| Preguntas de comprobación | 648 |
| Referencias bibliográficas citadas en clases | 432 |
| Documentos transversales (`docs/`) | 17 |
| Casos profesionales (`cases/`) | 9 |
| Proyectos integradores mayores (`projects/`) | 6 |
| Laboratorios (`labs/`) | 10 |

## Distribución por estado de evidencia

Cada clase declara con qué respaldo se sostiene lo que enseña. La distribución es
información del programa, no un adorno: muestra cuánto de este campo es evidencia
robusta y cuánto es marco normativo o práctica profesional.

| Estado | Clases | Proporción |
|---|---:|---:|
| `CONSISTENTE` | 90 | 41% |
| `ROBUSTA` | 45 | 20% |
| `PRACTICA-PROFESIONAL` | 26 | 12% |
| `EN-DEBATE` | 20 | 9% |
| `MARCO-NORMATIVO` | 19 | 8% |
| `EMERGENTE` | 16 | 7% |

## Etapas

| Etapa | Partes | Clases | Salida |
|---|---:|---:|---|
| 🟢 Etapa A — Fundamentos | 3 | 36 | explicar cómo aprende una persona y qué hace la educación con ese hecho |
| 🔵 Etapa B — Enseñanza por ciclo vital | 5 | 60 | enseñar a una población concreta con decisiones ajustadas a su desarrollo |
| 🟣 Etapa C — Núcleo profesional docente | 6 | 72 | diseñar, enseñar, evaluar y gestionar un curso completo con evidencia |
| 🟠 Etapa D — Educación superior y liderazgo | 2 | 24 | sostener la calidad del trabajo de otros, no solo del propio |
| 🔴 Etapa E — Investigación avanzada y formación de formadores | 2 | 24 | producir conocimiento educativo defendible y formar a quienes enseñan |

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
