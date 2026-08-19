# Guía del formador

Cómo usar este programa para formar a otros: en una institución educativa, en un programa de
capacitación, en una universidad o en un equipo docente.

## 1. Qué entrega el programa y qué debes poner tú

| El programa entrega | Tú aportas |
|---|---|
| 300 clases con decisión, evidencia y criterios | el contexto real de tus participantes |
| estados de evidencia declarados | el juicio sobre qué aplica en tu institución |
| talleres con contextos alternativos | acompañamiento y retroalimentación |
| rúbricas y criterios de logro | la calibración entre evaluadores |
| paquete exportable a LMS | la secuencia y los tiempos de tu programa |

El programa no se dicta: se usa como base de un dispositivo de formación que tú diseñas. La
clase 215 explica qué caracteriza al desarrollo profesional que efectivamente cambia la práctica,
y ese es el estándar que conviene aplicar aquí.

## 2. Cuatro formatos probados

### a) Programa completo por etapas (12 a 18 meses)

Las cinco etapas en orden, con un encuentro quincenal por parte y revisión de evidencias.
Adecuado para formación inicial docente o para un plan institucional de largo aliento.

### b) Módulo focalizado (6 a 10 semanas)

Una parte completa —por ejemplo, la 11 sobre evaluación o la 08 sobre inclusión— con
acompañamiento en el aula. Es el formato con mejor relación entre esfuerzo y cambio observable.

### c) Comunidad profesional de aprendizaje (permanente)

Una clase por reunión, aplicada entre sesiones, con evidencia real de estudiantes sobre la mesa.
Ver clase 185 para las condiciones que lo hacen funcionar.

### d) Capacitación laboral (2 a 5 días + seguimiento)

Selección de clases con foco en una decisión concreta, más plan de transferencia acordado con la
jefatura. Ver clases 089 y 096: sin plan de transferencia, el efecto es cero.

## 3. Cómo seleccionar clases para un programa corto

Regla práctica: escoge por **decisión**, no por tema. Toma la tabla de
[SYLLABUS.md](../SYLLABUS.md), filtra las decisiones que tus participantes deben poder tomar al
terminar, y arma la secuencia con esas clases. Diez clases bien elegidas y aplicadas producen
más cambio que una parte completa recorrida sin práctica.

## 4. Diseño de la sesión presencial

Una sesión de dos horas sobre una clase del programa que funciona:

| Tiempo | Actividad |
|---|---|
| 10 min | recuperación: qué se aplicó desde la sesión anterior y qué pasó |
| 15 min | la pregunta de foco de la clase, discutida antes de leer |
| 25 min | desarrollo: exposición breve con verificación de comprensión |
| 30 min | taller guiado en contextos reales de los participantes |
| 25 min | producción parcial de la evidencia de aprendizaje |
| 15 min | criterios de logro, compromiso de aplicación y fecha de revisión |

La regla que más cambia el resultado: **nunca cerrar una sesión sin un compromiso de aplicación
con fecha**.

## 5. Evaluación de los participantes

Usa lo que el programa ya trae:

- **evidencia de aprendizaje** de cada clase como entrega evaluable;
- **criterios de logro** como rúbrica de aprobación;
- **preguntas de comprobación** como cuestionario de cierre;
- **proyecto integrador** de la parte como evaluación sumativa.

Calibra con otro formador antes de evaluar: la clase 138 explica el procedimiento y por qué es
indispensable.

## 6. Errores frecuentes al formar con este material

- **Dictar las clases como exposición.** El material ya está escrito: la sesión debe usarse para
  lo que no se puede hacer leyendo —practicar, discutir casos, recibir retroalimentación—.
- **Omitir la sección de límites.** Es la parte que forma criterio profesional; saltarla convierte
  el programa en un recetario.
- **Evaluar con satisfacción.** Ver clase 095: la satisfacción correlaciona poco con el
  aprendizaje y casi nada con el cambio de práctica.
- **No acordar condiciones de aplicación.** Si la institución no da tiempo ni respaldo, el
  participante no podrá aplicar y el programa fracasará por razones ajenas a su diseño.
- **Formar sin acompañamiento en el puesto.** Es el componente que más se recorta por costo y el
  que más determina el resultado.

## 7. Migración a una plataforma

Si vas a llevar el programa a un LMS, el paquete exportable y las instrucciones de carga están en
[MIGRACION_A_CAPACITACION.md](MIGRACION_A_CAPACITACION.md). Genera el paquete con:

```bash
python scripts/exportar_capacitacion.py
```

## 8. Adaptación a otro país

El programa es Chile-first en su capa normativa y general en su capa de evidencia. Para adaptarlo:

1. sustituye las fuentes de [FUENTES.md](FUENTES.md) por las de tu jurisdicción;
2. revisa las clases marcadas `MARCO-NORMATIVO`: son las que cambian por completo;
3. conserva las marcadas `ROBUSTA` y `CONSISTENTE`: describen mecanismos generales;
4. ajusta los contextos de los talleres a la estructura de tu sistema educativo.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [Guía del estudiante](GUIA_DEL_ESTUDIANTE.md) | [Programa](../README.md) · [Documentos](../FILE_INDEX.md) | [Rutas de aprendizaje](RUTAS_DE_APRENDIZAJE.md) |
