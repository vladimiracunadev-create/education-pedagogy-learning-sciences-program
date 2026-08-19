# Migración a capacitación

El programa vive en Markdown porque es lo que se versiona, se revisa y se corrige. Pero una
plataforma de capacitación necesita otra cosa: HTML por lección, metadatos estructurados y una
tabla que el equipo administrativo pueda cargar. Este documento explica cómo pasar de una forma
a la otra sin duplicar el contenido ni perder trazabilidad.

## 1. Generar el paquete

```bash
python scripts/exportar_capacitacion.py
```

Produce `capacitacion/` con esta estructura:

```text
capacitacion/
├── index.html                  índice navegable del paquete completo
├── manifiesto.json             metadatos por módulo y lección
├── programa.csv                tabla plana para carga o revisión administrativa
├── LEEME.md                    instrucciones y decisiones del formato
├── paginas/clase-NNN.html      página autocontenida por clase, con estilos incluidos
└── contenido/clase-NNN.html    fragmento HTML para pegar en el editor del LMS
```

El paquete no se versiona: se regenera. La fuente sigue siendo `manifests/` y `curriculum/`.

## 2. Qué archivo usar según la plataforma

| Situación | Usa |
|---|---|
| El LMS tiene editor de contenido HTML | `contenido/clase-NNN.html` |
| El LMS acepta subir páginas completas | `paginas/clase-NNN.html` |
| Carga masiva por API o importador | `manifiesto.json` |
| Carga manual o revisión con el área administrativa | `programa.csv` |
| Necesitas el catálogo del programa sin el contenido | `catalog.json` en la raíz |

## 3. Correspondencia entre el programa y un LMS

| En este programa | En la plataforma |
|---|---|
| Parte (18) | Módulo o unidad |
| Clase (216) | Lección |
| Decisión que habilita | Objetivo de la lección |
| Evidencia de aprendizaje | Tarea entregable |
| Criterios de logro | Rúbrica de aprobación |
| Preguntas de comprobación | Cuestionario de cierre |
| Proyecto integrador (clase 12 de cada parte) | Evaluación del módulo |
| Estado de evidencia | Metadato visible de la lección |

El último punto importa: el estado de evidencia es **contenido**, no un metadato interno. Que un
participante sepa si lo que está aprendiendo es `ROBUSTA` o `PRACTICA-PROFESIONAL` es parte de su
formación profesional.

## 4. Carga horaria

El paquete declara un supuesto explícito: **1 hora de trabajo con el material y 1,5 horas de
práctica y producción de evidencia por clase**, es decir 2,5 horas por lección y 540 horas por el
programa completo.

Es una estimación declarada, no una medición. Si tu contexto exige otra carga, ajusta las
constantes `HORAS_MATERIAL` y `HORAS_PRACTICA` en `scripts/exportar_capacitacion.py` y
regenera: el manifiesto y el CSV recalculan solos.

## 5. Recomendaciones de implementación

1. **No cargues las 216 lecciones de una vez.** Empieza por una parte completa, mide y ajusta.
2. **Configura la tarea entregable desde el inicio.** Sin entrega, el programa se convierte en
   lectura y su efecto se pierde.
3. **Publica la rúbrica antes del trabajo**, no después: la clase 113 explica por qué.
4. **Programa el seguimiento de rezago** en la semana dos de cada módulo. La clase 087 documenta
   que la deserción se decide temprano.
5. **Contempla acompañamiento humano.** La clase 215 es explícita: sin acompañamiento en el
   puesto, el cambio de práctica no se sostiene.
6. **Conserva la trazabilidad.** Cada lección conserva su número de clase: `PED-001` a `PED-216`.
   Eso permite volver a la fuente cuando algo deba corregirse.

## 6. Qué revisar después de cargar

- ¿Los encabezados se conservaron como encabezados y no como texto en negrita?
- ¿Las tablas mantienen su fila de encabezado?
- ¿Los bloques de diagrama se ven como texto legible si la plataforma no renderiza mermaid?
- ¿Los enlaces internos entre clases apuntan a las lecciones correctas de la plataforma?
- ¿La lección es legible en un teléfono y con zoom al 200 %?

## 7. Actualizaciones

Cuando el contenido cambie:

1. edita el manifiesto correspondiente en `manifests/`;
2. ejecuta `python scripts/generar_clases.py` y las validaciones;
3. regenera el paquete con `python scripts/exportar_capacitacion.py`;
4. vuelve a cargar solo las lecciones modificadas, identificándolas por su código `PED-NNN`.

Nunca edites el contenido directamente en la plataforma: se pierde la trazabilidad y la próxima
regeneración lo sobrescribe.

## 8. Licencia y atribución

El contenido educativo se publica bajo **CC BY-NC-SA 4.0**
(ver [LICENSE-CONTENT.md](../LICENSE-CONTENT.md)). Si lo cargas en una plataforma:

- mantén la atribución visible;
- conserva la misma licencia en las obras derivadas;
- **no lo uses con fines comerciales** sin autorización previa del autor.

Si necesitas uso comercial, escribe al autor antes de cargarlo.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [Marco chileno](MARCO_CHILE.md) | [Programa](../README.md) · [Documentos](../FILE_INDEX.md) | [Arquitectura](ARQUITECTURA.md) |
