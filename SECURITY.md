# Política de seguridad y de datos

Este repositorio no ejecuta servicios ni procesa datos de usuarios: es contenido educativo y un
conjunto de generadores en Python que usan solo la biblioteca estándar. Aun así, hay tres
superficies que importan.

## 1. Datos personales

**Este repositorio no debe contener nunca datos reales de estudiantes, familias o docentes.**

- Todos los ejemplos son ficticios o sintéticos.
- Los datos de `datasets/` son generados y no corresponden a personas reales.
- `.gitignore` excluye `privado/`, `datos-reales/` y archivos de planilla, precisamente para
  reducir el riesgo de un envío accidental.

Si detectas datos personales en el repositorio o en su historial, **repórtalo de inmediato** por
canal privado y no abras un *issue* público describiendo el contenido.

## 2. Superficie técnica

| Elemento | Riesgo | Mitigación |
|---|---|---|
| Generadores en Python | ejecución local de código del repositorio | solo biblioteca estándar; sin red, sin descargas, sin ejecución de código externo |
| Sitio estático | inyección vía contenido | el conversor escapa el HTML del Markdown; el único recurso externo es la biblioteca de diagramas, con versión fijada |
| GitHub Actions | dependencia de acciones de terceros | acciones fijadas por SHA y permisos mínimos por workflow |
| Paquete de capacitación | contenido cargado a plataformas de terceros | HTML sin scripts; la plataforma receptora aplica su propia política |

## 3. Cómo reportar una vulnerabilidad

1. **No abras un *issue* público** si el reporte expone datos personales o un vector explotable.
2. Escribe al responsable del repositorio a través del perfil de GitHub del autor.
3. Incluye: qué encontraste, cómo reproducirlo y qué impacto tendría.
4. Recibirás respuesta en un plazo razonable; es un proyecto mantenido por una persona.

Si el hallazgo es un enlace roto, un error de formato o un problema de contenido, ese sí va como
*issue* público normal.

## 4. Buenas prácticas para quien use este material

- No subas trabajos con datos reales de estudiantes a repositorios públicos.
- No ingreses información identificable de estudiantes en herramientas de IA
  (ver [docs/IA_EN_EDUCACION.md](docs/IA_EN_EDUCACION.md)).
- Antes de adoptar una plataforma educativa, verifica qué datos trata, dónde se almacenan, quién
  accede y por cuánto tiempo se conservan.
- Al publicar evidencia de tu portafolio, anonimiza: nombres, cursos, establecimientos y
  cualquier dato que permita identificar a una persona.

## 5. Alcance de esta política

Cubre el contenido de este repositorio y sus generadores. No cubre las plataformas de terceros
donde se cargue el paquete de capacitación, ni las herramientas que cada institución use para
procesar datos de sus estudiantes.
