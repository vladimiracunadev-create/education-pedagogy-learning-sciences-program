# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Versionado semántico: `MAYOR.MENOR.PARCHE`.

- **MAYOR:** cambia la estructura del programa (partes, contrato pedagógico).
- **MENOR:** se agrega contenido o material de apoyo sin romper la estructura.
- **PARCHE:** correcciones de contenido, fuentes, enlaces o generadores.

## [2.0.0] — 2026-08-19

Amplía el programa con una sexta etapa de especialización. El currículo pasa de 216 a **300
clases** en **25 partes**, y se agrega un banco de actividades de aula. Es cambio mayor porque
modifica la estructura del programa: aparece la etapa F y siete partes nuevas.

### Añadido

- **Parte 18 · Alfabetización inicial y ciencia de la lectura** (217–228). Cierra el hueco más
  visible del programa: el problema faro del caso persistente —un tercio de los estudiantes sin
  fluidez lectora en 3.º básico— no tenía con qué resolverse. Conciencia fonológica,
  correspondencias en español, fluidez, vocabulario, comprensión, escritura inicial, dislexia,
  evaluación por componentes, intervención por niveles y alfabetización disciplinar.
- **Parte 19 · Metodologías y enfoques pedagógicos** (229–240). Criterios para comparar enfoques
  sin caer en modas: instrucción explícita, indagación guiada, tradiciones conductista,
  cognitivista y constructivista, Montessori, Waldorf, Reggio Emilia, Freinet, Escuela Nueva,
  pedagogía crítica, familias del aprendizaje basado en algo, aprendizaje-servicio, gamificación
  y enfoque por competencias.
- **Parte 20 · Estrategias pedagógicas para necesidades educativas específicas** (241–252). De la
  categoría diagnóstica a la estrategia de aula: TDAH, síndrome de Down, autismo, discapacidad
  intelectual, dificultades específicas del aprendizaje, discapacidad sensorial y motora,
  comunicación aumentativa, trastornos del lenguaje, altas capacidades y codocencia.
- **Parte 21 · Desafíos actuales del aula** (253–264). Desenganche y ausentismo crónico, pérdida
  de sentido, pantallas y atención, violencia escolar, acoso, ciberacoso, conductas agresivas,
  agresiones al docente, mediación restaurativa, aulas numerosas y derivación por riesgo.
- **Parte 22 · Diversidad cultural, lingüística y territorial** (265–276). Interculturalidad,
  educación intercultural bilingüe, estudiantes migrantes, castellano como segunda lengua,
  lenguas extranjeras, variedades lingüísticas, educación rural, aula multigrado, segregación
  escolar y financiamiento.
- **Parte 23 · Bienestar, salud mental y sostenibilidad del oficio** (277–288). Frontera del rol
  docente, ansiedad, riesgo suicida y protocolo, aprendizaje socioemocional, adversidad, crisis y
  postvención, afectividad y educación sexual integral, convivencia digital, carga docente,
  desgaste profesional y cuidado del equipo.
- **Parte 24 · Modelos educativos internacionales y evidencia comparada** (289–300). Cómo se lee
  un sistema sin copiarlo, pruebas internacionales, Finlandia, Singapur, Estonia, Japón, Shanghái,
  Ontario, Portugal y Polonia, Escuela Nueva de Colombia y Chile en perspectiva comparada.
- **Banco de 60 actividades prácticas** en `actividades/`, generado desde
  `manifests/pedagogia/actividades-*.json`. Seis familias, con duración, agrupamiento, variante
  por edad, adecuación para la diversidad, señal de verificación y la clase que la fundamenta.
  Se recorre por familia, por ciclo, por asignatura y por modalidad o contexto.
- **Etapa F** en el recorrido del programa, con sus siete partes y su lema propio.
- **Siete casos persistentes nuevos**, y la red del caso se amplía con la Escuela Rural El Maitén
  —multigrado, 48 estudiantes— para sostener las partes 22 y 24.
- **74 obras nuevas** en la bibliografía, con siete áreas nuevas.
- **`scripts/generar_actividades.py`**, con su verificación `--check` en CI y en `make todo`.
- **Cinco pruebas nuevas** (38 en total) sobre el contrato del banco de actividades.

### Cambiado

- Las 14 guías de carrera declaran ahora su **especialización de etapa F**, con las partes
  recomendadas en orden y la razón de esa prioridad para el rol.
- Validadores, generadores, portal y paquete de capacitación operan sobre 25 partes y 300 clases.
- La bibliografía, el glosario, el manifiesto y los índices se regeneraron completos.

## [1.2.0] — 2026-08-19

Sube el estándar de clase al nivel de los demás programas del autor, sin cambiar el currículo:
las mismas 216 clases, con casi tres veces más contenido por clase.

### Añadido

- **Estándar `clase-profunda`**: 22 secciones obligatorias por clase, verificadas en CI. Se
  suman agenda de 90 minutos, modelo mental con método y señales observables, desarrollo en seis
  capas, lectura comparada con el lente de cada obra, ejemplo trabajado paso a paso, comparación
  de caminos con su riesgo, lectura del tema por nivel de rol, caso profesional con informe de
  decisión, evidencia archivable, rúbrica ponderada y contexto normativo chileno por clase.
- **18 casos persistentes** (`manifests/pedagogia/casos.json`): cada parte trabaja sus 12 clases
  sobre la misma realidad —un establecimiento simulado— y declara el artefacto que produce.
- **`evidence/`**: carpeta de portafolio con su protocolo de anonimización; el contenido queda
  fuera del control de versiones a propósito.
- **`MANIFEST.md`** generado: inventario cuantitativo contado sobre archivos reales.
- **CodeQL** con acciones fijadas por SHA, permisos por job y ejecución semanal.
- Validación de profundidad: una clase por debajo de 2.500 palabras rompe el CI.
- Pruebas nuevas: profundidad, ausencia de negrita anidada y presencia del caso de la parte.

### Cambiado

- Las clases pasan de 1.302–1.577 palabras a **3.765–4.133** (mediana 3.875) y el currículo de
  301.694 a **840.621 palabras**.
- El README declara el estándar de clase, la profundidad verificada, los casos persistentes y
  los enlaces al glosario, la bibliografía y el manifiesto con sus conteos.
- Las páginas de parte publican su caso, su artefacto y sus enlaces de práctica.

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
