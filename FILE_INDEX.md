# Índice de archivos

Índice completo y generado del repositorio. Se reconstruye con `python scripts/generar_indice.py`.

## Raíz

| Archivo | Propósito |
|---|---|
| [`CHANGELOG.md`](CHANGELOG.md) | historial de versiones |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | normas de convivencia del proyecto |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | cómo contribuir y qué exige una contribución |
| [`CURRICULUM.md`](CURRICULUM.md) | las 25 partes y las 300 clases en una tabla |
| [`FILE_INDEX.md`](FILE_INDEX.md) | este índice |
| [`LICENSE`](LICENSE) | licencia MIT del código |
| [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md) | licencia CC BY-NC-SA 4.0 del contenido educativo |
| [`MANIFEST.md`](MANIFEST.md) | inventario cuantitativo verificable del repositorio |
| [`Makefile`](Makefile) | atajos de generación y validación |
| [`README.md`](README.md) | presentación del programa y punto de entrada |
| [`ROADMAP.md`](ROADMAP.md) | etapas de dominio y condiciones para avanzar |
| [`SECURITY.md`](SECURITY.md) | política de seguridad y de datos |
| [`STATUS.md`](STATUS.md) | cifras verificables del estado del repositorio |
| [`SUPPORT.md`](SUPPORT.md) | cómo pedir ayuda y dónde |
| [`SYLLABUS.md`](SYLLABUS.md) | programa detallado con decisiones y evidencias por clase |
| [`VERSION`](VERSION) | versión vigente del programa |
| [`catalog.json`](catalog.json) | catálogo de las 300 clases legible por máquina |
| [`requirements.txt`](requirements.txt) | dependencias opcionales de los generadores |

## Directorios

| Directorio | Archivos | Propósito |
|---|---:|---|
| `assessments/` | 3 | rúbricas e instrumentos de autoevaluación |
| `books/` | 1 | guía de lectura del programa |
| `cases/` | 9 | casos profesionales para resolver con el marco del programa |
| `chile-education-system/` | 9 | marco institucional y normativo chileno |
| `curriculum/` | 325 | las 25 partes y sus 300 clases, generadas desde `manifests/` |
| `datasets/` | 2 | datos sintéticos para practicar análisis |
| `docs/` | 17 | documentos transversales: metodología, guías, bibliografía, marcos y protocolos |
| `international-education/` | 1 | comparación internacional de sistemas educativos |
| `labs/` | 13 | laboratorios y simuladores de práctica |
| `manifests/` | 35 | fuente única de verdad del currículo: nada se edita a mano en `curriculum/` |
| `notebooks/` | 1 | actividades analíticas reproducibles |
| `papers/` | 1 | plantilla de revisión crítica de artículos |
| `projects/` | 6 | proyectos integradores mayores del programa |
| `rutas/` | 15 | guías de carrera por rol: qué es, día a día, ruta en el programa y credenciales |
| `scripts/` | 7 | generadores y validadores; todo lo publicado se reconstruye con ellos |
| `templates/` | 5 | plantillas de trabajo reutilizables |
| `tests/` | 1 | pruebas estructurales del repositorio |
| `virtual-school-lab/` | 1 | escuela y universidad simuladas para practicar decisiones |

## Currículo

### Parte 00 — Fundamentos de la educación

[README de la parte](curriculum/part-00-fundamentos-de-la-educacion/README.md) · clases 001–012

- `001` [Educación, pedagogía, enseñanza y aprendizaje](curriculum/part-00-fundamentos-de-la-educacion/class-01-educacion-pedagogia-ensenanza-y-aprendizaje/README.md)
- `002` [Historia de la educación](curriculum/part-00-fundamentos-de-la-educacion/class-02-historia-de-la-educacion/README.md)
- `003` [Filosofía de la educación](curriculum/part-00-fundamentos-de-la-educacion/class-03-filosofia-de-la-educacion/README.md)
- `004` [Ética profesional docente](curriculum/part-00-fundamentos-de-la-educacion/class-04-etica-profesional-docente/README.md)
- `005` [Sistemas educativos comparados](curriculum/part-00-fundamentos-de-la-educacion/class-05-sistemas-educativos-comparados/README.md)
- `006` [Educación formal, no formal e informal](curriculum/part-00-fundamentos-de-la-educacion/class-06-educacion-formal-no-formal-e-informal/README.md)
- `007` [Derecho a la educación](curriculum/part-00-fundamentos-de-la-educacion/class-07-derecho-a-la-educacion/README.md)
- `008` [Rol social de la escuela](curriculum/part-00-fundamentos-de-la-educacion/class-08-rol-social-de-la-escuela/README.md)
- `009` [Profesiones y roles educativos](curriculum/part-00-fundamentos-de-la-educacion/class-09-profesiones-y-roles-educativos/README.md)
- `010` [Cultura escolar y comunidad](curriculum/part-00-fundamentos-de-la-educacion/class-10-cultura-escolar-y-comunidad/README.md)
- `011` [Calidad y equidad educativa](curriculum/part-00-fundamentos-de-la-educacion/class-11-calidad-y-equidad-educativa/README.md)
- `012` [Proyecto integrador: mapa del sistema educativo](curriculum/part-00-fundamentos-de-la-educacion/class-12-proyecto-integrador-mapa-del-sistema-educativo/README.md)

### Parte 01 — Ciencias del aprendizaje

[README de la parte](curriculum/part-01-ciencias-del-aprendizaje/README.md) · clases 013–024

- `013` [Conductismo y aprendizaje observable](curriculum/part-01-ciencias-del-aprendizaje/class-01-conductismo-y-aprendizaje-observable/README.md)
- `014` [Cognitivismo y procesamiento de información](curriculum/part-01-ciencias-del-aprendizaje/class-02-cognitivismo-y-procesamiento-de-informacion/README.md)
- `015` [Constructivismo](curriculum/part-01-ciencias-del-aprendizaje/class-03-constructivismo/README.md)
- `016` [Socioconstructivismo y aprendizaje mediado](curriculum/part-01-ciencias-del-aprendizaje/class-04-socioconstructivismo-y-aprendizaje-mediado/README.md)
- `017` [Memoria de trabajo y memoria de largo plazo](curriculum/part-01-ciencias-del-aprendizaje/class-05-memoria-de-trabajo-y-memoria-de-largo-plazo/README.md)
- `018` [Atención y control ejecutivo](curriculum/part-01-ciencias-del-aprendizaje/class-06-atencion-y-control-ejecutivo/README.md)
- `019` [Carga cognitiva](curriculum/part-01-ciencias-del-aprendizaje/class-07-carga-cognitiva/README.md)
- `020` [Práctica de recuperación y espaciado](curriculum/part-01-ciencias-del-aprendizaje/class-08-practica-de-recuperacion-y-espaciado/README.md)
- `021` [Metacognición](curriculum/part-01-ciencias-del-aprendizaje/class-09-metacognicion/README.md)
- `022` [Motivación y autodeterminación](curriculum/part-01-ciencias-del-aprendizaje/class-10-motivacion-y-autodeterminacion/README.md)
- `023` [Transferencia y aprendizaje profundo](curriculum/part-01-ciencias-del-aprendizaje/class-11-transferencia-y-aprendizaje-profundo/README.md)
- `024` [Proyecto integrador: diseño basado en evidencia](curriculum/part-01-ciencias-del-aprendizaje/class-12-proyecto-integrador-diseno-basado-en-evidencia/README.md)

### Parte 02 — Desarrollo humano

[README de la parte](curriculum/part-02-desarrollo-humano/README.md) · clases 025–036

- `025` [Desarrollo prenatal y primera infancia](curriculum/part-02-desarrollo-humano/class-01-desarrollo-prenatal-y-primera-infancia/README.md)
- `026` [Desarrollo motor y sensorial](curriculum/part-02-desarrollo-humano/class-02-desarrollo-motor-y-sensorial/README.md)
- `027` [Desarrollo del lenguaje](curriculum/part-02-desarrollo-humano/class-03-desarrollo-del-lenguaje/README.md)
- `028` [Desarrollo cognitivo](curriculum/part-02-desarrollo-humano/class-04-desarrollo-cognitivo/README.md)
- `029` [Desarrollo socioemocional](curriculum/part-02-desarrollo-humano/class-05-desarrollo-socioemocional/README.md)
- `030` [Apego y vínculos](curriculum/part-02-desarrollo-humano/class-06-apego-y-vinculos/README.md)
- `031` [Niñez media](curriculum/part-02-desarrollo-humano/class-07-ninez-media/README.md)
- `032` [Adolescencia](curriculum/part-02-desarrollo-humano/class-08-adolescencia/README.md)
- `033` [Adultez emergente y adultez](curriculum/part-02-desarrollo-humano/class-09-adultez-emergente-y-adultez/README.md)
- `034` [Envejecimiento y aprendizaje permanente](curriculum/part-02-desarrollo-humano/class-10-envejecimiento-y-aprendizaje-permanente/README.md)
- `035` [Diferencias individuales](curriculum/part-02-desarrollo-humano/class-11-diferencias-individuales/README.md)
- `036` [Proyecto integrador: trayectoria de desarrollo](curriculum/part-02-desarrollo-humano/class-12-proyecto-integrador-trayectoria-de-desarrollo/README.md)

### Parte 03 — Educación parvularia

[README de la parte](curriculum/part-03-educacion-parvularia/README.md) · clases 037–048

- `037` [Principios de educación parvularia](curriculum/part-03-educacion-parvularia/class-01-principios-de-educacion-parvularia/README.md)
- `038` [Juego y aprendizaje](curriculum/part-03-educacion-parvularia/class-02-juego-y-aprendizaje/README.md)
- `039` [Ambientes de aprendizaje](curriculum/part-03-educacion-parvularia/class-03-ambientes-de-aprendizaje/README.md)
- `040` [Lenguaje y alfabetización emergente](curriculum/part-03-educacion-parvularia/class-04-lenguaje-y-alfabetizacion-emergente/README.md)
- `041` [Pensamiento matemático temprano](curriculum/part-03-educacion-parvularia/class-05-pensamiento-matematico-temprano/README.md)
- `042` [Corporalidad y movimiento](curriculum/part-03-educacion-parvularia/class-06-corporalidad-y-movimiento/README.md)
- `043` [Arte, música y creatividad](curriculum/part-03-educacion-parvularia/class-07-arte-musica-y-creatividad/README.md)
- `044` [Exploración del entorno](curriculum/part-03-educacion-parvularia/class-08-exploracion-del-entorno/README.md)
- `045` [Desarrollo socioemocional](curriculum/part-03-educacion-parvularia/class-09-desarrollo-socioemocional/README.md)
- `046` [Observación y documentación pedagógica](curriculum/part-03-educacion-parvularia/class-10-observacion-y-documentacion-pedagogica/README.md)
- `047` [Familia y comunidad](curriculum/part-03-educacion-parvularia/class-11-familia-y-comunidad/README.md)
- `048` [Proyecto integrador: experiencia parvularia](curriculum/part-03-educacion-parvularia/class-12-proyecto-integrador-experiencia-parvularia/README.md)

### Parte 04 — Educación básica

[README de la parte](curriculum/part-04-educacion-basica/README.md) · clases 049–060

- `049` [Didáctica de la lectura](curriculum/part-04-educacion-basica/class-01-didactica-de-la-lectura/README.md)
- `050` [Didáctica de la escritura](curriculum/part-04-educacion-basica/class-02-didactica-de-la-escritura/README.md)
- `051` [Didáctica de la matemática](curriculum/part-04-educacion-basica/class-03-didactica-de-la-matematica/README.md)
- `052` [Didáctica de las ciencias](curriculum/part-04-educacion-basica/class-04-didactica-de-las-ciencias/README.md)
- `053` [Historia, geografía y ciudadanía](curriculum/part-04-educacion-basica/class-05-historia-geografia-y-ciudadania/README.md)
- `054` [Arte y creatividad](curriculum/part-04-educacion-basica/class-06-arte-y-creatividad/README.md)
- `055` [Educación física y bienestar](curriculum/part-04-educacion-basica/class-07-educacion-fisica-y-bienestar/README.md)
- `056` [Tecnología y alfabetización digital](curriculum/part-04-educacion-basica/class-08-tecnologia-y-alfabetizacion-digital/README.md)
- `057` [Planificación de unidades](curriculum/part-04-educacion-basica/class-09-planificacion-de-unidades/README.md)
- `058` [Evaluación formativa en básica](curriculum/part-04-educacion-basica/class-10-evaluacion-formativa-en-basica/README.md)
- `059` [Gestión de aula en niñez media](curriculum/part-04-educacion-basica/class-11-gestion-de-aula-en-ninez-media/README.md)
- `060` [Proyecto integrador: unidad interdisciplinaria](curriculum/part-04-educacion-basica/class-12-proyecto-integrador-unidad-interdisciplinaria/README.md)

### Parte 05 — Educación media y adolescencia

[README de la parte](curriculum/part-05-educacion-media-y-adolescencia/README.md) · clases 061–072

- `061` [Psicología de la adolescencia](curriculum/part-05-educacion-media-y-adolescencia/class-01-psicologia-de-la-adolescencia/README.md)
- `062` [Identidad, pertenencia y motivación](curriculum/part-05-educacion-media-y-adolescencia/class-02-identidad-pertenencia-y-motivacion/README.md)
- `063` [Autoridad pedagógica](curriculum/part-05-educacion-media-y-adolescencia/class-03-autoridad-pedagogica/README.md)
- `064` [Gestión de aula adolescente](curriculum/part-05-educacion-media-y-adolescencia/class-04-gestion-de-aula-adolescente/README.md)
- `065` [Aprendizaje basado en proyectos](curriculum/part-05-educacion-media-y-adolescencia/class-05-aprendizaje-basado-en-proyectos/README.md)
- `066` [Aprendizaje basado en problemas](curriculum/part-05-educacion-media-y-adolescencia/class-06-aprendizaje-basado-en-problemas/README.md)
- `067` [Debate y argumentación](curriculum/part-05-educacion-media-y-adolescencia/class-07-debate-y-argumentacion/README.md)
- `068` [STEM y STEAM](curriculum/part-05-educacion-media-y-adolescencia/class-08-stem-y-steam/README.md)
- `069` [Orientación vocacional](curriculum/part-05-educacion-media-y-adolescencia/class-09-orientacion-vocacional/README.md)
- `070` [Ciudadanía digital](curriculum/part-05-educacion-media-y-adolescencia/class-10-ciudadania-digital/README.md)
- `071` [Evaluación auténtica](curriculum/part-05-educacion-media-y-adolescencia/class-11-evaluacion-autentica/README.md)
- `072` [Proyecto integrador: desafío de educación media](curriculum/part-05-educacion-media-y-adolescencia/class-12-proyecto-integrador-desafio-de-educacion-media/README.md)

### Parte 06 — Educación técnico-profesional

[README de la parte](curriculum/part-06-educacion-tecnico-profesional/README.md) · clases 073–084

- `073` [Formación por competencias](curriculum/part-06-educacion-tecnico-profesional/class-01-formacion-por-competencias/README.md)
- `074` [Aprendizaje situado](curriculum/part-06-educacion-tecnico-profesional/class-02-aprendizaje-situado/README.md)
- `075` [Talleres y laboratorios](curriculum/part-06-educacion-tecnico-profesional/class-03-talleres-y-laboratorios/README.md)
- `076` [Seguridad y cultura preventiva](curriculum/part-06-educacion-tecnico-profesional/class-04-seguridad-y-cultura-preventiva/README.md)
- `077` [Rúbricas de desempeño](curriculum/part-06-educacion-tecnico-profesional/class-05-rubricas-de-desempeno/README.md)
- `078` [Portafolio de evidencias](curriculum/part-06-educacion-tecnico-profesional/class-06-portafolio-de-evidencias/README.md)
- `079` [Aprendizaje dual](curriculum/part-06-educacion-tecnico-profesional/class-07-aprendizaje-dual/README.md)
- `080` [Vínculo educación-empresa](curriculum/part-06-educacion-tecnico-profesional/class-08-vinculo-educacion-empresa/README.md)
- `081` [Práctica profesional](curriculum/part-06-educacion-tecnico-profesional/class-09-practica-profesional/README.md)
- `082` [Competencias transversales](curriculum/part-06-educacion-tecnico-profesional/class-10-competencias-transversales/README.md)
- `083` [Empleabilidad y transición al trabajo](curriculum/part-06-educacion-tecnico-profesional/class-11-empleabilidad-y-transicion-al-trabajo/README.md)
- `084` [Proyecto integrador: módulo TP](curriculum/part-06-educacion-tecnico-profesional/class-12-proyecto-integrador-modulo-tp/README.md)

### Parte 07 — Educación de adultos y andragogía

[README de la parte](curriculum/part-07-educacion-de-adultos-y-andragogia/README.md) · clases 085–096

- `085` [Principios de andragogía](curriculum/part-07-educacion-de-adultos-y-andragogia/class-01-principios-de-andragogia/README.md)
- `086` [Experiencia previa como recurso](curriculum/part-07-educacion-de-adultos-y-andragogia/class-02-experiencia-previa-como-recurso/README.md)
- `087` [Aprendizaje autodirigido](curriculum/part-07-educacion-de-adultos-y-andragogia/class-03-aprendizaje-autodirigido/README.md)
- `088` [Motivación en adultos](curriculum/part-07-educacion-de-adultos-y-andragogia/class-04-motivacion-en-adultos/README.md)
- `089` [Capacitación laboral](curriculum/part-07-educacion-de-adultos-y-andragogia/class-05-capacitacion-laboral/README.md)
- `090` [Reskilling y upskilling](curriculum/part-07-educacion-de-adultos-y-andragogia/class-06-reskilling-y-upskilling/README.md)
- `091` [Microlearning](curriculum/part-07-educacion-de-adultos-y-andragogia/class-07-microlearning/README.md)
- `092` [Mentoría](curriculum/part-07-educacion-de-adultos-y-andragogia/class-08-mentoria/README.md)
- `093` [Coaching educativo](curriculum/part-07-educacion-de-adultos-y-andragogia/class-09-coaching-educativo/README.md)
- `094` [Aprendizaje experiencial](curriculum/part-07-educacion-de-adultos-y-andragogia/class-10-aprendizaje-experiencial/README.md)
- `095` [Evaluación en formación de adultos](curriculum/part-07-educacion-de-adultos-y-andragogia/class-11-evaluacion-en-formacion-de-adultos/README.md)
- `096` [Proyecto integrador: programa de capacitación](curriculum/part-07-educacion-de-adultos-y-andragogia/class-12-proyecto-integrador-programa-de-capacitacion/README.md)

### Parte 08 — Inclusión y educación especial

[README de la parte](curriculum/part-08-inclusion-y-educacion-especial/README.md) · clases 097–108

- `097` [Educación inclusiva](curriculum/part-08-inclusion-y-educacion-especial/class-01-educacion-inclusiva/README.md)
- `098` [Barreras para el aprendizaje y la participación](curriculum/part-08-inclusion-y-educacion-especial/class-02-barreras-para-el-aprendizaje-y-la-participacion/README.md)
- `099` [Diseño Universal para el Aprendizaje](curriculum/part-08-inclusion-y-educacion-especial/class-03-diseno-universal-para-el-aprendizaje/README.md)
- `100` [Diversificación de la enseñanza](curriculum/part-08-inclusion-y-educacion-especial/class-04-diversificacion-de-la-ensenanza/README.md)
- `101` [Necesidades educativas especiales](curriculum/part-08-inclusion-y-educacion-especial/class-05-necesidades-educativas-especiales/README.md)
- `102` [Autismo y apoyos educativos](curriculum/part-08-inclusion-y-educacion-especial/class-06-autismo-y-apoyos-educativos/README.md)
- `103` [TDAH y autorregulación](curriculum/part-08-inclusion-y-educacion-especial/class-07-tdah-y-autorregulacion/README.md)
- `104` [Dificultades específicas del aprendizaje](curriculum/part-08-inclusion-y-educacion-especial/class-08-dificultades-especificas-del-aprendizaje/README.md)
- `105` [Discapacidad sensorial y motora](curriculum/part-08-inclusion-y-educacion-especial/class-09-discapacidad-sensorial-y-motora/README.md)
- `106` [Discapacidad intelectual](curriculum/part-08-inclusion-y-educacion-especial/class-10-discapacidad-intelectual/README.md)
- `107` [Altas capacidades](curriculum/part-08-inclusion-y-educacion-especial/class-11-altas-capacidades/README.md)
- `108` [Proyecto integrador: aula accesible](curriculum/part-08-inclusion-y-educacion-especial/class-12-proyecto-integrador-aula-accesible/README.md)

### Parte 09 — Diseño curricular

[README de la parte](curriculum/part-09-diseno-curricular/README.md) · clases 109–120

- `109` [Concepto y niveles del currículum](curriculum/part-09-diseno-curricular/class-01-concepto-y-niveles-del-curriculum/README.md)
- `110` [Perfil de egreso](curriculum/part-09-diseno-curricular/class-02-perfil-de-egreso/README.md)
- `111` [Competencias](curriculum/part-09-diseno-curricular/class-03-competencias/README.md)
- `112` [Resultados de aprendizaje](curriculum/part-09-diseno-curricular/class-04-resultados-de-aprendizaje/README.md)
- `113` [Objetivos de aprendizaje](curriculum/part-09-diseno-curricular/class-05-objetivos-de-aprendizaje/README.md)
- `114` [Secuenciación curricular](curriculum/part-09-diseno-curricular/class-06-secuenciacion-curricular/README.md)
- `115` [Mapas curriculares](curriculum/part-09-diseno-curricular/class-07-mapas-curriculares/README.md)
- `116` [Backward design](curriculum/part-09-diseno-curricular/class-08-backward-design/README.md)
- `117` [Alineamiento constructivo](curriculum/part-09-diseno-curricular/class-09-alineamiento-constructivo/README.md)
- `118` [Diseño de syllabus](curriculum/part-09-diseno-curricular/class-10-diseno-de-syllabus/README.md)
- `119` [Planificación anual y por unidad](curriculum/part-09-diseno-curricular/class-11-planificacion-anual-y-por-unidad/README.md)
- `120` [Proyecto integrador: currículo completo](curriculum/part-09-diseno-curricular/class-12-proyecto-integrador-curriculo-completo/README.md)

### Parte 10 — Didáctica avanzada

[README de la parte](curriculum/part-10-didactica-avanzada/README.md) · clases 121–132

- `121` [Conocimiento pedagógico del contenido](curriculum/part-10-didactica-avanzada/class-01-conocimiento-pedagogico-del-contenido/README.md)
- `122` [Explicaciones efectivas](curriculum/part-10-didactica-avanzada/class-02-explicaciones-efectivas/README.md)
- `123` [Ejemplos y contraejemplos](curriculum/part-10-didactica-avanzada/class-03-ejemplos-y-contraejemplos/README.md)
- `124` [Preguntas de alto nivel](curriculum/part-10-didactica-avanzada/class-04-preguntas-de-alto-nivel/README.md)
- `125` [Diálogo socrático](curriculum/part-10-didactica-avanzada/class-05-dialogo-socratico/README.md)
- `126` [Modelamiento y think-aloud](curriculum/part-10-didactica-avanzada/class-06-modelamiento-y-think-aloud/README.md)
- `127` [Scaffolding](curriculum/part-10-didactica-avanzada/class-07-scaffolding/README.md)
- `128` [Práctica guiada e independiente](curriculum/part-10-didactica-avanzada/class-08-practica-guiada-e-independiente/README.md)
- `129` [Aprendizaje colaborativo](curriculum/part-10-didactica-avanzada/class-09-aprendizaje-colaborativo/README.md)
- `130` [Flipped classroom](curriculum/part-10-didactica-avanzada/class-10-flipped-classroom/README.md)
- `131` [Mastery learning](curriculum/part-10-didactica-avanzada/class-11-mastery-learning/README.md)
- `132` [Proyecto integrador: secuencia didáctica](curriculum/part-10-didactica-avanzada/class-12-proyecto-integrador-secuencia-didactica/README.md)

### Parte 11 — Evaluación y psicometría

[README de la parte](curriculum/part-11-evaluacion-y-psicometria/README.md) · clases 133–144

- `133` [Evaluación diagnóstica](curriculum/part-11-evaluacion-y-psicometria/class-01-evaluacion-diagnostica/README.md)
- `134` [Evaluación formativa](curriculum/part-11-evaluacion-y-psicometria/class-02-evaluacion-formativa/README.md)
- `135` [Evaluación sumativa](curriculum/part-11-evaluacion-y-psicometria/class-03-evaluacion-sumativa/README.md)
- `136` [Evaluación auténtica](curriculum/part-11-evaluacion-y-psicometria/class-04-evaluacion-autentica/README.md)
- `137` [Construcción de ítems](curriculum/part-11-evaluacion-y-psicometria/class-05-construccion-de-items/README.md)
- `138` [Rúbricas y escalas](curriculum/part-11-evaluacion-y-psicometria/class-06-rubricas-y-escalas/README.md)
- `139` [Retroalimentación efectiva](curriculum/part-11-evaluacion-y-psicometria/class-07-retroalimentacion-efectiva/README.md)
- `140` [Validez](curriculum/part-11-evaluacion-y-psicometria/class-08-validez/README.md)
- `141` [Confiabilidad](curriculum/part-11-evaluacion-y-psicometria/class-09-confiabilidad/README.md)
- `142` [Análisis de dificultad y discriminación](curriculum/part-11-evaluacion-y-psicometria/class-10-analisis-de-dificultad-y-discriminacion/README.md)
- `143` [Introducción a teoría clásica e IRT](curriculum/part-11-evaluacion-y-psicometria/class-11-introduccion-a-teoria-clasica-e-irt/README.md)
- `144` [Proyecto integrador: sistema de evaluación](curriculum/part-11-evaluacion-y-psicometria/class-12-proyecto-integrador-sistema-de-evaluacion/README.md)

### Parte 12 — Gestión del aula y convivencia

[README de la parte](curriculum/part-12-gestion-del-aula-y-convivencia/README.md) · clases 145–156

- `145` [Clima de aula](curriculum/part-12-gestion-del-aula-y-convivencia/class-01-clima-de-aula/README.md)
- `146` [Normas y rutinas](curriculum/part-12-gestion-del-aula-y-convivencia/class-02-normas-y-rutinas/README.md)
- `147` [Prevención de problemas de conducta](curriculum/part-12-gestion-del-aula-y-convivencia/class-03-prevencion-de-problemas-de-conducta/README.md)
- `148` [Refuerzo y consecuencias](curriculum/part-12-gestion-del-aula-y-convivencia/class-04-refuerzo-y-consecuencias/README.md)
- `149` [Comunicación docente](curriculum/part-12-gestion-del-aula-y-convivencia/class-05-comunicacion-docente/README.md)
- `150` [Conflictos entre estudiantes](curriculum/part-12-gestion-del-aula-y-convivencia/class-06-conflictos-entre-estudiantes/README.md)
- `151` [Desmotivación y resistencia](curriculum/part-12-gestion-del-aula-y-convivencia/class-07-desmotivacion-y-resistencia/README.md)
- `152` [Copias, plagio e integridad](curriculum/part-12-gestion-del-aula-y-convivencia/class-08-copias-plagio-e-integridad/README.md)
- `153` [Uso de celulares y distracciones](curriculum/part-12-gestion-del-aula-y-convivencia/class-09-uso-de-celulares-y-distracciones/README.md)
- `154` [Trabajo con apoderados](curriculum/part-12-gestion-del-aula-y-convivencia/class-10-trabajo-con-apoderados/README.md)
- `155` [Crisis y derivación responsable](curriculum/part-12-gestion-del-aula-y-convivencia/class-11-crisis-y-derivacion-responsable/README.md)
- `156` [Proyecto integrador: plan de gestión de aula](curriculum/part-12-gestion-del-aula-y-convivencia/class-12-proyecto-integrador-plan-de-gestion-de-aula/README.md)

### Parte 13 — Tecnología e IA educativa

[README de la parte](curriculum/part-13-tecnologia-e-ia-educativa/README.md) · clases 157–168

- `157` [Competencia digital docente](curriculum/part-13-tecnologia-e-ia-educativa/class-01-competencia-digital-docente/README.md)
- `158` [LMS y aulas virtuales](curriculum/part-13-tecnologia-e-ia-educativa/class-02-lms-y-aulas-virtuales/README.md)
- `159` [Diseño de recursos digitales](curriculum/part-13-tecnologia-e-ia-educativa/class-03-diseno-de-recursos-digitales/README.md)
- `160` [Gamificación](curriculum/part-13-tecnologia-e-ia-educativa/class-04-gamificacion/README.md)
- `161` [Analítica de aprendizaje](curriculum/part-13-tecnologia-e-ia-educativa/class-05-analitica-de-aprendizaje/README.md)
- `162` [Aprendizaje adaptativo](curriculum/part-13-tecnologia-e-ia-educativa/class-06-aprendizaje-adaptativo/README.md)
- `163` [Fundamentos de IA para docentes](curriculum/part-13-tecnologia-e-ia-educativa/class-07-fundamentos-de-ia-para-docentes/README.md)
- `164` [LLM y generación de contenidos](curriculum/part-13-tecnologia-e-ia-educativa/class-08-llm-y-generacion-de-contenidos/README.md)
- `165` [RAG y tutores educativos](curriculum/part-13-tecnologia-e-ia-educativa/class-09-rag-y-tutores-educativos/README.md)
- `166` [Agentes educativos](curriculum/part-13-tecnologia-e-ia-educativa/class-10-agentes-educativos/README.md)
- `167` [Ética, privacidad y sesgos](curriculum/part-13-tecnologia-e-ia-educativa/class-11-etica-privacidad-y-sesgos/README.md)
- `168` [Proyecto integrador: tutor IA responsable](curriculum/part-13-tecnologia-e-ia-educativa/class-12-proyecto-integrador-tutor-ia-responsable/README.md)

### Parte 14 — Docencia universitaria

[README de la parte](curriculum/part-14-docencia-universitaria/README.md) · clases 169–180

- `169` [Aprendizaje en educación superior](curriculum/part-14-docencia-universitaria/class-01-aprendizaje-en-educacion-superior/README.md)
- `170` [Diseño de asignaturas](curriculum/part-14-docencia-universitaria/class-02-diseno-de-asignaturas/README.md)
- `171` [Syllabus universitario](curriculum/part-14-docencia-universitaria/class-03-syllabus-universitario/README.md)
- `172` [Clase magistral efectiva](curriculum/part-14-docencia-universitaria/class-04-clase-magistral-efectiva/README.md)
- `173` [Seminarios](curriculum/part-14-docencia-universitaria/class-05-seminarios/README.md)
- `174` [Laboratorios](curriculum/part-14-docencia-universitaria/class-06-laboratorios/README.md)
- `175` [Tutorías y ayudantías](curriculum/part-14-docencia-universitaria/class-07-tutorias-y-ayudantias/README.md)
- `176` [Evaluación universitaria](curriculum/part-14-docencia-universitaria/class-08-evaluacion-universitaria/README.md)
- `177` [Integridad académica](curriculum/part-14-docencia-universitaria/class-09-integridad-academica/README.md)
- `178` [Proyectos de título](curriculum/part-14-docencia-universitaria/class-10-proyectos-de-titulo/README.md)
- `179` [Supervisión inicial de investigación](curriculum/part-14-docencia-universitaria/class-11-supervision-inicial-de-investigacion/README.md)
- `180` [Proyecto integrador: asignatura universitaria](curriculum/part-14-docencia-universitaria/class-12-proyecto-integrador-asignatura-universitaria/README.md)

### Parte 15 — Gestión y liderazgo educativo

[README de la parte](curriculum/part-15-gestion-y-liderazgo-educativo/README.md) · clases 181–192

- `181` [Liderazgo pedagógico](curriculum/part-15-gestion-y-liderazgo-educativo/class-01-liderazgo-pedagogico/README.md)
- `182` [Cultura organizacional educativa](curriculum/part-15-gestion-y-liderazgo-educativo/class-02-cultura-organizacional-educativa/README.md)
- `183` [Observación de clases](curriculum/part-15-gestion-y-liderazgo-educativo/class-03-observacion-de-clases/README.md)
- `184` [Feedback a docentes](curriculum/part-15-gestion-y-liderazgo-educativo/class-04-feedback-a-docentes/README.md)
- `185` [Comunidades profesionales de aprendizaje](curriculum/part-15-gestion-y-liderazgo-educativo/class-05-comunidades-profesionales-de-aprendizaje/README.md)
- `186` [Planificación estratégica](curriculum/part-15-gestion-y-liderazgo-educativo/class-06-planificacion-estrategica/README.md)
- `187` [Gestión de equipos](curriculum/part-15-gestion-y-liderazgo-educativo/class-07-gestion-de-equipos/README.md)
- `188` [Indicadores educativos](curriculum/part-15-gestion-y-liderazgo-educativo/class-08-indicadores-educativos/README.md)
- `189` [Mejora escolar](curriculum/part-15-gestion-y-liderazgo-educativo/class-09-mejora-escolar/README.md)
- `190` [Innovación educativa](curriculum/part-15-gestion-y-liderazgo-educativo/class-10-innovacion-educativa/README.md)
- `191` [Ética de la dirección](curriculum/part-15-gestion-y-liderazgo-educativo/class-11-etica-de-la-direccion/README.md)
- `192` [Proyecto integrador: plan de mejora institucional](curriculum/part-15-gestion-y-liderazgo-educativo/class-12-proyecto-integrador-plan-de-mejora-institucional/README.md)

### Parte 16 — Investigación educativa

[README de la parte](curriculum/part-16-investigacion-educativa/README.md) · clases 193–204

- `193` [Epistemología de la investigación](curriculum/part-16-investigacion-educativa/class-01-epistemologia-de-la-investigacion/README.md)
- `194` [Pregunta y problema de investigación](curriculum/part-16-investigacion-educativa/class-02-pregunta-y-problema-de-investigacion/README.md)
- `195` [Revisión de literatura](curriculum/part-16-investigacion-educativa/class-03-revision-de-literatura/README.md)
- `196` [Marco teórico](curriculum/part-16-investigacion-educativa/class-04-marco-teorico/README.md)
- `197` [Diseños cuantitativos](curriculum/part-16-investigacion-educativa/class-05-disenos-cuantitativos/README.md)
- `198` [Diseños cualitativos](curriculum/part-16-investigacion-educativa/class-06-disenos-cualitativos/README.md)
- `199` [Métodos mixtos](curriculum/part-16-investigacion-educativa/class-07-metodos-mixtos/README.md)
- `200` [Muestreo](curriculum/part-16-investigacion-educativa/class-08-muestreo/README.md)
- `201` [Estadística descriptiva e inferencial](curriculum/part-16-investigacion-educativa/class-09-estadistica-descriptiva-e-inferencial/README.md)
- `202` [Análisis temático](curriculum/part-16-investigacion-educativa/class-10-analisis-tematico/README.md)
- `203` [Ética y reproducibilidad](curriculum/part-16-investigacion-educativa/class-11-etica-y-reproducibilidad/README.md)
- `204` [Proyecto integrador: investigación de nivel magíster](curriculum/part-16-investigacion-educativa/class-12-proyecto-integrador-investigacion-de-nivel-magister/README.md)

### Parte 17 — Investigación doctoral y formación de formadores

[README de la parte](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/README.md) · clases 205–216

- `205` [Problema doctoral y originalidad](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-01-problema-doctoral-y-originalidad/README.md)
- `206` [Contribución al conocimiento](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-02-contribucion-al-conocimiento/README.md)
- `207` [Diseños avanzados de investigación](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-03-disenos-avanzados-de-investigacion/README.md)
- `208` [Modelos longitudinales y multinivel](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-04-modelos-longitudinales-y-multinivel/README.md)
- `209` [Meta-análisis y revisión sistemática](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-05-meta-analisis-y-revision-sistematica/README.md)
- `210` [Investigación basada en diseño](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-06-investigacion-basada-en-diseno/README.md)
- `211` [Learning analytics avanzado](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-07-learning-analytics-avanzado/README.md)
- `212` [Escritura científica](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-08-escritura-cientifica/README.md)
- `213` [Publicación y peer review](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-09-publicacion-y-peer-review/README.md)
- `214` [Dirección y evaluación de tesis](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-10-direccion-y-evaluacion-de-tesis/README.md)
- `215` [Formación de docentes](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-11-formacion-de-docentes/README.md)
- `216` [Proyecto integrador: propuesta doctoral defendible](curriculum/part-17-investigacion-doctoral-y-formacion-de-formadores/class-12-proyecto-integrador-propuesta-doctoral-defendible/README.md)

### Parte 18 — Alfabetización inicial y ciencia de la lectura

[README de la parte](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/README.md) · clases 217–228

- `217` [Qué resolvió la ciencia de la lectura](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-01-que-resolvio-la-ciencia-de-la-lectura/README.md)
- `218` [Conciencia fonológica y principio alfabético](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-02-conciencia-fonologica-y-principio-alfabetico/README.md)
- `219` [Enseñanza explícita de correspondencias en español](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-03-ensenanza-explicita-de-correspondencias-en-espanol/README.md)
- `220` [Fluidez lectora: medirla y desarrollarla](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-04-fluidez-lectora-medirla-y-desarrollarla/README.md)
- `221` [Vocabulario y conocimiento del mundo](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-05-vocabulario-y-conocimiento-del-mundo/README.md)
- `222` [Comprensión lectora y sus estrategias](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-06-comprension-lectora-y-sus-estrategias/README.md)
- `223` [Enseñanza de la escritura inicial](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-07-ensenanza-de-la-escritura-inicial/README.md)
- `224` [Dislexia y dificultades específicas de lectura](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-08-dislexia-y-dificultades-especificas-de-lectura/README.md)
- `225` [Evaluación de la lectura por componentes](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-09-evaluacion-de-la-lectura-por-componentes/README.md)
- `226` [Intervención por niveles y grupos de refuerzo](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-10-intervencion-por-niveles-y-grupos-de-refuerzo/README.md)
- `227` [Alfabetización disciplinar en las asignaturas](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-11-alfabetizacion-disciplinar-en-las-asignaturas/README.md)
- `228` [Proyecto integrador: plan lector de establecimiento](curriculum/part-18-alfabetizacion-inicial-y-ciencia-de-la-lectura/class-12-proyecto-integrador/README.md)

### Parte 19 — Metodologías y enfoques pedagógicos

[README de la parte](curriculum/part-19-metodologias-y-enfoques-pedagogicos/README.md) · clases 229–240

- `229` [Cómo se compara un enfoque pedagógico](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-01-como-se-compara-un-enfoque-pedagogico/README.md)
- `230` [Instrucción explícita y enseñanza directa](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-02-instruccion-explicita-y-ensenanza-directa/README.md)
- `231` [Indagación y descubrimiento guiado](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-03-indagacion-y-descubrimiento-guiado/README.md)
- `232` [Conductismo, cognitivismo y constructivismo](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-04-conductismo-cognitivismo-y-constructivismo/README.md)
- `233` [Montessori, Waldorf y Reggio Emilia](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-05-montessori-waldorf-y-reggio-emilia/README.md)
- `234` [Freinet, Escuela Nueva y pedagogías activas](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-06-freinet-escuela-nueva-y-pedagogias-activas/README.md)
- `235` [Pedagogía crítica y educación popular](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-07-pedagogia-critica-y-educacion-popular/README.md)
- `236` [Familias del aprendizaje basado en algo](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-08-familias-del-aprendizaje-basado-en-algo/README.md)
- `237` [Aprendizaje-servicio y vínculo comunitario](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-09-aprendizaje-servicio-y-vinculo-comunitario/README.md)
- `238` [Gamificación y juego serio](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-10-gamificacion-y-juego-serio/README.md)
- `239` [Enfoque por competencias y su coherencia](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-11-enfoque-por-competencias-y-su-coherencia/README.md)
- `240` [Proyecto integrador: decisión metodológica fundamentada](curriculum/part-19-metodologias-y-enfoques-pedagogicos/class-12-proyecto-integrador/README.md)

### Parte 20 — Estrategias pedagógicas para necesidades educativas específicas

[README de la parte](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/README.md) · clases 241–252

- `241` [De la categoría diagnóstica a la estrategia de aula](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-01-de-la-categoria-diagnostica-a-la-estrategia-de-aula/README.md)
- `242` [TDAH: atención, autorregulación y organización](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-02-tdah-atencion-autorregulacion-y-organizacion/README.md)
- `243` [Síndrome de Down: aprendizaje, lenguaje y participación](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-03-sindrome-de-down-aprendizaje-lenguaje-y-participacion/README.md)
- `244` [Autismo: estructura, anticipación y comunicación](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-04-autismo-estructura-anticipacion-y-comunicacion/README.md)
- `245` [Discapacidad intelectual y acceso al currículum](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-05-discapacidad-intelectual-y-acceso-al-curriculum/README.md)
- `246` [Dislexia, disgrafía y discalculia en el aula común](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-06-dislexia-disgrafia-y-discalculia-en-el-aula-comun/README.md)
- `247` [Discapacidad visual y auditiva: estrategias de acceso](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-07-discapacidad-visual-y-auditiva-estrategias-de-acceso/README.md)
- `248` [Discapacidad motora y comunicación aumentativa](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-08-discapacidad-motora-y-comunicacion-aumentativa/README.md)
- `249` [Trastornos del lenguaje y de la comunicación](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-09-trastornos-del-lenguaje-y-de-la-comunicacion/README.md)
- `250` [Altas capacidades: enriquecimiento y aceleración](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-10-altas-capacidades-enriquecimiento-y-aceleracion/README.md)
- `251` [Acompañamiento diferenciado y codocencia](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-11-acompanamiento-diferenciado-y-codocencia/README.md)
- `252` [Proyecto integrador: plan de apoyo con estrategias verificables](curriculum/part-20-estrategias-pedagogicas-para-necesidades-educativas-especificas/class-12-proyecto-integrador/README.md)

### Parte 21 — Desafíos actuales del aula

[README de la parte](curriculum/part-21-desafios-actuales-del-aula/README.md) · clases 253–264

- `253` [Desenganche escolar y ausentismo crónico](curriculum/part-21-desafios-actuales-del-aula/class-01-desenganche-escolar-y-ausentismo-cronico/README.md)
- `254` [Falta de sentido: por qué estudiar dejó de ser evidente](curriculum/part-21-desafios-actuales-del-aula/class-02-falta-de-sentido-por-que-estudiar-dejo-de-ser-evidente/README.md)
- `255` [Atención, pantallas y fragmentación cognitiva](curriculum/part-21-desafios-actuales-del-aula/class-03-atencion-pantallas-y-fragmentacion-cognitiva/README.md)
- `256` [Violencia escolar: tipos, factores y respuesta](curriculum/part-21-desafios-actuales-del-aula/class-04-violencia-escolar-tipos-factores-y-respuesta/README.md)
- `257` [Acoso escolar: detección e intervención con evidencia](curriculum/part-21-desafios-actuales-del-aula/class-05-acoso-escolar-deteccion-e-intervencion-con-evidencia/README.md)
- `258` [Ciberacoso y conflictos que entran desde fuera](curriculum/part-21-desafios-actuales-del-aula/class-06-ciberacoso-y-conflictos-que-entran-desde-fuera/README.md)
- `259` [Conductas agresivas y desregulación emocional](curriculum/part-21-desafios-actuales-del-aula/class-07-conductas-agresivas-y-desregulacion-emocional/README.md)
- `260` [Agresiones al docente y protección del equipo](curriculum/part-21-desafios-actuales-del-aula/class-08-agresiones-al-docente-y-proteccion-del-equipo/README.md)
- `261` [Mediación escolar y prácticas restaurativas](curriculum/part-21-desafios-actuales-del-aula/class-09-mediacion-escolar-y-practicas-restaurativas/README.md)
- `262` [Aulas numerosas y heterogéneas con recursos limitados](curriculum/part-21-desafios-actuales-del-aula/class-10-aulas-numerosas-y-heterogeneas-con-recursos-limitados/README.md)
- `263` [Consumo, riesgo psicosocial y derivación](curriculum/part-21-desafios-actuales-del-aula/class-11-consumo-riesgo-psicosocial-y-derivacion/README.md)
- `264` [Proyecto integrador: plan de convivencia con indicadores](curriculum/part-21-desafios-actuales-del-aula/class-12-proyecto-integrador/README.md)

### Parte 22 — Diversidad cultural, lingüística y territorial

[README de la parte](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/README.md) · clases 265–276

- `265` [Lo que la escuela da por supuesto](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-01-lo-que-la-escuela-da-por-supuesto/README.md)
- `266` [Educación intercultural: del folclor al diálogo de saberes](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-02-educacion-intercultural-del-folclor-al-dialogo-de-saberes/README.md)
- `267` [Educación intercultural bilingüe y lenguas originarias](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-03-educacion-intercultural-bilingue-y-lenguas-originarias/README.md)
- `268` [Estudiantes migrantes: acogida, trayectoria y derechos](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-04-estudiantes-migrantes-acogida-trayectoria-y-derechos/README.md)
- `269` [Castellano como segunda lengua](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-05-castellano-como-segunda-lengua/README.md)
- `270` [Enseñanza de lenguas extranjeras](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-06-ensenanza-de-lenguas-extranjeras/README.md)
- `271` [Variedades lingüísticas y prejuicio](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-07-variedades-linguisticas-y-prejuicio/README.md)
- `272` [Educación rural: territorio y pertinencia](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-08-educacion-rural-territorio-y-pertinencia/README.md)
- `273` [Aula multigrado: varios niveles a la vez](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-09-aula-multigrado-varios-niveles-a-la-vez/README.md)
- `274` [Segregación escolar y efecto par](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-10-segregacion-escolar-y-efecto-par/README.md)
- `275` [Financiamiento, recursos y decisiones pedagógicas](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-11-financiamiento-recursos-y-decisiones-pedagogicas/README.md)
- `276` [Proyecto integrador: plan de pertinencia cultural y territorial](curriculum/part-22-diversidad-cultural-linguistica-y-territorial/class-12-proyecto-integrador/README.md)

### Parte 23 — Bienestar, salud mental y sostenibilidad del oficio

[README de la parte](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/README.md) · clases 277–288

- `277` [Salud mental escolar: alcance y límites de la escuela](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-01-salud-mental-escolar-alcance-y-limites-de-la-escuela/README.md)
- `278` [Ansiedad y estrés académico](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-02-ansiedad-y-estres-academico/README.md)
- `279` [Depresión, autolesión y riesgo suicida](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-03-depresion-autolesion-y-riesgo-suicida/README.md)
- `280` [Aprendizaje socioemocional: qué funciona](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-04-aprendizaje-socioemocional-que-funciona/README.md)
- `281` [Adversidad, trauma y prácticas sensibles](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-05-adversidad-trauma-y-practicas-sensibles/README.md)
- `282` [Duelo, crisis y emergencias en la comunidad](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-06-duelo-crisis-y-emergencias-en-la-comunidad/README.md)
- `283` [Afectividad y educación sexual integral](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-07-afectividad-y-educacion-sexual-integral/README.md)
- `284` [Convivencia digital, imagen y exposición](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-08-convivencia-digital-imagen-y-exposicion/README.md)
- `285` [Carga docente, tiempo y sostenibilidad](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-09-carga-docente-tiempo-y-sostenibilidad/README.md)
- `286` [Desgaste profesional y su prevención institucional](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-10-desgaste-profesional-y-su-prevencion-institucional/README.md)
- `287` [Cuidado del equipo y liderazgo del bienestar](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-11-cuidado-del-equipo-y-liderazgo-del-bienestar/README.md)
- `288` [Proyecto integrador: plan de bienestar escolar](curriculum/part-23-bienestar-salud-mental-y-sostenibilidad-del-oficio/class-12-proyecto-integrador/README.md)

### Parte 24 — Modelos educativos internacionales y evidencia comparada

[README de la parte](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/README.md) · clases 289–300

- `289` [Cómo se lee un sistema educativo sin copiarlo](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-01-como-se-lee-un-sistema-educativo-sin-copiarlo/README.md)
- `290` [Pruebas internacionales: qué miden y qué no](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-02-pruebas-internacionales-que-miden-y-que-no/README.md)
- `291` [Finlandia: qué se malinterpretó](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-03-finlandia-que-se-malinterpreto/README.md)
- `292` [Singapur: currículum, formación docente y matemática](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-04-singapur-curriculum-formacion-docente-y-matematica/README.md)
- `293` [Estonia: equidad y digitalización](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-05-estonia-equidad-y-digitalizacion/README.md)
- `294` [Japón y el lesson study](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-06-japon-y-el-lesson-study/README.md)
- `295` [Shanghái: práctica deliberada entre docentes](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-07-shanghai-practica-deliberada-entre-docentes/README.md)
- `296` [Ontario: mejora sistémica sostenida](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-08-ontario-mejora-sistemica-sostenida/README.md)
- `297` [Portugal y Polonia: reformas que movieron resultados](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-09-portugal-y-polonia-reformas-que-movieron-resultados/README.md)
- `298` [Escuela Nueva de Colombia y modelos de bajo costo](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-10-escuela-nueva-de-colombia-y-modelos-de-bajo-costo/README.md)
- `299` [Chile en perspectiva comparada](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-11-chile-en-perspectiva-comparada/README.md)
- `300` [Proyecto integrador: propuesta de adaptación fundamentada](curriculum/part-24-modelos-educativos-internacionales-y-evidencia-comparada/class-12-proyecto-integrador/README.md)

## Documentos transversales

| Documento | Propósito |
|---|---|
| [`docs/ACCESIBILIDAD.md`](docs/ACCESIBILIDAD.md) | Accesibilidad del material |
| [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) | Arquitectura del repositorio |
| [`docs/BIBLIOGRAFIA.md`](docs/BIBLIOGRAFIA.md) | Bibliografía del programa |
| [`docs/ESTANDARES_DE_EVIDENCIA.md`](docs/ESTANDARES_DE_EVIDENCIA.md) | Estándares de evidencia |
| [`docs/ETICA_Y_PRACTICA_RESPONSABLE.md`](docs/ETICA_Y_PRACTICA_RESPONSABLE.md) | Ética y práctica responsable |
| [`docs/FUENTES.md`](docs/FUENTES.md) | Fuentes oficiales y cómo leerlas |
| [`docs/GLOSARIO.md`](docs/GLOSARIO.md) | Glosario del programa |
| [`docs/GUIA_DEL_ESTUDIANTE.md`](docs/GUIA_DEL_ESTUDIANTE.md) | Guía del estudiante |
| [`docs/GUIA_DEL_FORMADOR.md`](docs/GUIA_DEL_FORMADOR.md) | Guía del formador |
| [`docs/IA_EN_EDUCACION.md`](docs/IA_EN_EDUCACION.md) | Inteligencia artificial en educación |
| [`docs/INCLUSION_Y_DUA.md`](docs/INCLUSION_Y_DUA.md) | Inclusión y Diseño Universal para el Aprendizaje |
| [`docs/MARCO_CHILE.md`](docs/MARCO_CHILE.md) | Marco institucional y normativo chileno |
| [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md) | Metodología del programa |
| [`docs/MIGRACION_A_CAPACITACION.md`](docs/MIGRACION_A_CAPACITACION.md) | Migración a capacitación |
| [`docs/PREGUNTAS_FRECUENTES.md`](docs/PREGUNTAS_FRECUENTES.md) | Preguntas frecuentes |
| [`docs/RUTAS_DE_APRENDIZAJE.md`](docs/RUTAS_DE_APRENDIZAJE.md) | Rutas de aprendizaje |
| [`docs/SISTEMA_DE_EVALUACION.md`](docs/SISTEMA_DE_EVALUACION.md) | Sistema de evaluación del programa |
