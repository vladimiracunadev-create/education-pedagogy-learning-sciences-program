# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Versionado semántico: `MAYOR.MENOR.PARCHE`.

- **MAYOR:** cambia la estructura del programa (partes, contrato pedagógico).
- **MENOR:** se agrega contenido o material de apoyo sin romper la estructura.
- **PARCHE:** correcciones de contenido, fuentes, enlaces o generadores.

## [1.1.0] — 2026-08-19

### Añadido

- **14 guías de carrera por rol** en `rutas/`: docente de básica, de media, educador/a de
  párvulos, docente técnico-profesional, educador/a diferencial, jefatura técnico-pedagógica,
  dirección escolar, formador de adultos, docente universitario, diseñador instruccional,
  especialista en evaluación, especialista en IA educativa, investigador educativo y formador de
  formadores. Cada una con qué es el rol, un día en el puesto, qué necesitas saber, la ruta exacta
  en el programa, credenciales y marco chileno, progresión, mitos del oficio y siguientes pasos.
- **Índice de rutas** (`rutas/README.md`) con el recorrido recomendado, la evidencia de salida y
  la credencial de referencia de cada rol.
- **Validación de las guías de rol en CI**: secciones obligatorias, extensión mínima, enlace desde
  el índice y navegación de retorno.
- **Dependabot** para mantener las acciones de GitHub al día, y **zizmor con versión fijada**
  para que una release nueva de la herramienta no vuelva rojo el CI.
- **Plantillas de issue y de pull request** alineadas con las exigencias de contribución.

### Cambiado

- **README reconstruido**: portada con cobertura por ciclo y función, anatomía de una clase,
  estado verificable ampliado, resultado principal por parte, tabla de rutas por rol, distribución
  de estados de evidencia, material de práctica y sección de migración a LMS.
- El **sitio publica las rutas por rol** y las incorpora al menú lateral.
- La **validación de enlaces** cubre ahora `rutas/`, `templates/`, `projects/`, `cases/` y
  `assessments/`: 3.713 enlaces internos verificados.
- Los workflows declaran **tiempos máximos por job** y fijan la versión de las herramientas de
  auditoría, para que el CI no se vuelva rojo por un cambio externo.

## [1.0.0] — 2026-08-18

Primera versión completa y publicada del programa.

### Añadido

- **Currículo completo:** 18 partes y 216 clases con 301.694 palabras, generadas desde
  `manifests/` como fuente única de verdad.
- **Contrato pedagógico de 13 secciones** por clase, verificado en CI: propósito, resultados,
  conceptos, diagrama, desarrollo en tres capas, taller, evidencia de aprendizaje, reto,
  criterios de logro, errores frecuentes, diversidad y ética, preguntas de comprobación,
  lecturas y conexiones.
- **Estados de evidencia** declarados clase por clase: `ROBUSTA`, `CONSISTENTE`, `EMERGENTE`,
  `EN-DEBATE`, `MARCO-NORMATIVO` y `PRACTICA-PROFESIONAL`, con su distribución publicada en
  `STATUS.md`.
- **864 conceptos con definición operacional** y glosario generado de 806 términos con enlace a
  la clase que define cada uno.
- **432 citas bibliográficas en clase** sobre unas 250 obras y fuentes oficiales catalogadas en
  `docs/BIBLIOGRAFIA.md` y `docs/FUENTES.md`.
- **234 diagramas mermaid:** uno por clase y uno por parte.
- **17 documentos transversales** en `docs/`: metodología, estándares de evidencia, guías del
  estudiante y del formador, rutas de aprendizaje, sistema de evaluación, inclusión y DUA,
  accesibilidad, IA en educación, marco chileno, migración a capacitación, arquitectura y
  preguntas frecuentes.
- **Protocolo de práctica responsable** aplicable a las 216 clases, con resguardos de datos,
  criterios de derivación y condiciones de aplicación con estudiantes reales.
- **Generadores sin dependencias externas:** `generar_clases.py`, `generar_indice.py`,
  `generar_sitio.py` y `exportar_capacitacion.py`.
- **Validadores:** `validar_estructura.py` (conteos, secciones, enlaces, manifiestos) y
  `validar_encoding.py` (UTF-8 sin BOM ni mojibake).
- **Sitio estático** para GitHub Pages con buscador de las 216 clases, tema claro y oscuro,
  diagramas y verificación de enlaces internos.
- **Paquete de capacitación exportable** a LMS: página autocontenida y fragmento HTML por
  lección, `manifiesto.json`, `programa.csv` y guía de migración.
- **`catalog.json`**: catálogo del programa legible por máquina.
- **Integración continua:** estructura, enlaces, codificación, Markdown, pruebas, compilación del
  sitio y del paquete en cada push.

### Cambiado

- Migración de la estructura anterior de 18 carpetas de módulo con clases breves a
  `curriculum/part-NN-slug/class-NN-slug/`, generada desde manifiestos. Los 216 títulos del
  currículo original se conservan íntegros.
- Los documentos de estado —`STATUS.md`, `SYLLABUS.md`, `FILE_INDEX.md`, `docs/GLOSARIO.md` y
  `catalog.json`— pasan a generarse: ninguna cifra del repositorio se escribe a mano.

### Notas

- El programa no otorga título, grado ni habilitación legal para ejercer la docencia.
- La capa normativa es Chile-first y describe el marco vigente a la fecha de redacción.
