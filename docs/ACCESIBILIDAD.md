# Accesibilidad del material

Un programa que enseña inclusión y publica material inaccesible se contradice a sí mismo. Este
documento declara qué cumple el repositorio, cómo se verifica y qué queda pendiente.

## 1. Qué cumple este repositorio

| Decisión | Por qué |
|---|---|
| Todo el contenido en Markdown plano | legible con lector de pantalla, editable con cualquier herramienta y sin formato propietario |
| Encabezados jerárquicos correctos (`#`, `##`, `###`) | permiten navegar por estructura en lugar de leer linealmente |
| Tablas con encabezado explícito | los lectores de pantalla anuncian la columna al leer cada celda |
| Enlaces con texto descriptivo | nunca «haz clic aquí»: el texto del enlace dice a dónde lleva |
| Sin dependencia del color para transmitir información | los estados de evidencia se nombran en texto, no solo con un color |
| Sitio HTML con contraste alto y tema claro y oscuro | respeta la preferencia del sistema y permite cambiarla |
| Diagramas con alternativa textual | si mermaid no carga, el bloque queda como texto legible que describe el flujo |
| Sin imágenes portadoras de contenido | nada del programa se pierde si las imágenes no cargan |
| Tipografía del sistema y unidades relativas | respeta el tamaño de letra configurado por la persona |

## 2. Cómo verificarlo

```bash
python scripts/validar_encoding.py      # UTF-8 sin BOM ni mojibake
python scripts/validar_estructura.py    # jerarquía de encabezados y enlaces internos
python scripts/generar_sitio.py         # el sitio falla si hay enlaces rotos
```

Verificación manual recomendada antes de una publicación mayor:

1. navegar el sitio solo con teclado;
2. abrir una clase con un lector de pantalla y comprobar que la estructura se anuncia;
3. aumentar el zoom al 200 % y comprobar que no se pierde contenido;
4. cargar una página con los diagramas bloqueados y verificar que sigue siendo comprensible.

## 3. Lo que este repositorio pide a quien produce material con él

Si generas material a partir de este programa —para tu curso, tu institución o tu plataforma—,
mantén estas condiciones mínimas:

- **Estructura antes que estilo.** Usa encabezados reales, no texto en negrita más grande.
- **Texto alternativo en toda imagen** que aporte información; imagen decorativa, alt vacío.
- **Subtítulos en todo video** y transcripción cuando el contenido sea central.
- **Contraste suficiente** entre texto y fondo.
- **No transmitas información solo por color**, por posición o por forma.
- **Documentos que se puedan leer sin conexión** y en dispositivos modestos.
- **Formatos abiertos** cuando sea posible: quien usa tecnología de apoyo suele tener menos
  margen con formatos propietarios.

## 4. Accesibilidad del paquete de capacitación

El paquete que genera `scripts/exportar_capacitacion.py` hereda estas condiciones: HTML
semántico, sin dependencias externas, sin JavaScript necesario para leer el contenido y con
estilos que respetan el zoom. Si tu plataforma reescribe el HTML, verifica que conserve los
encabezados y las tablas con encabezado.

## 5. Limitaciones declaradas

- **Los diagramas mermaid no tienen descripción larga.** Su contenido está también en el texto de
  la clase, pero un diagrama complejo leído por un lector de pantalla no equivale a la versión
  visual. Es una brecha conocida.
- **El sitio depende de un recurso externo para renderizar diagramas.** Sin conexión, quedan como
  texto: la información no se pierde, la representación visual sí.
- **No hay versión en lectura fácil** de las clases. Sería un aporte real y no existe todavía.
- **No hay traducción a otros idiomas ni a lengua de señas.**

Estas limitaciones se declaran porque un documento de accesibilidad que solo enumera logros no
sirve para mejorar.

## 6. Cómo reportar un problema de accesibilidad

Abre un *issue* en el repositorio describiendo: qué página, con qué herramienta, qué esperabas y
qué ocurrió. Los problemas de accesibilidad tienen prioridad sobre las mejoras de contenido en
este proyecto.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [Inclusión y DUA](INCLUSION_Y_DUA.md) | [Programa](../README.md) · [Documentos](../FILE_INDEX.md) | [IA en educación](IA_EN_EDUCACION.md) |
