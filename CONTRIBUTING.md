# Cómo contribuir

Gracias por el interés. Este repositorio tiene reglas estrictas porque su valor depende de que
cada afirmación se pueda verificar.

## Regla número uno

> **No edites `curriculum/`.** Es contenido generado. Edita el manifiesto correspondiente en
> `manifests/` y ejecuta `python scripts/generar_clases.py`.

Si editas una clase publicada, el CI fallará: comprueba que lo publicado coincida exactamente con
la fuente.

## Qué se acepta

| Tipo de contribución | Cómo se evalúa |
|---|---|
| **Corrección de un error factual** | se acepta con la fuente que lo demuestra; es la contribución más valiosa |
| **Actualización normativa** | se acepta citando la norma vigente con su fecha |
| **Mejora de una explicación** | se evalúa por claridad y precisión, no por extensión |
| **Nueva lectura de referencia** | debe aportar algo que las existentes no aportan |
| **Mejora de accesibilidad** | tiene prioridad sobre las mejoras de contenido |
| **Mejora de los generadores** | debe mantener cero dependencias externas |
| **Nueva clase o parte** | solo si cumple los cinco criterios del [ROADMAP](ROADMAP.md) |

## Qué no se acepta

- Afirmaciones sin fuente identificable.
- Métodos presentados como más respaldados de lo que están.
- Contenido que reproduzca neuromitos ya refutados
  (ver [docs/ESTANDARES_DE_EVIDENCIA.md](docs/ESTANDARES_DE_EVIDENCIA.md)).
- Material con derechos de autor de terceros sin permiso.
- Datos reales de estudiantes, familias o colegas, aunque estén parcialmente anonimizados.
- Contenido promocional de productos, plataformas o servicios.
- Cambios que rompan el contrato pedagógico de una clase.

## Exigencias de toda contribución de contenido

1. **Separa evidencia de opinión.** Si es tu experiencia profesional, dilo; es legítimo y se marca
   como `PRACTICA-PROFESIONAL`.
2. **Declara el estado de evidencia** con el criterio del documento de estándares.
3. **Declara los límites.** Toda clase tiene una sección para lo que la evidencia **no** sostiene:
   completarla no es opcional.
4. **Cita con precisión:** autor, año, obra. Y verifica que la obra existe y dice lo que afirmas.
5. **Considera diversidad y accesibilidad** en el campo `inclusion`.
6. **Escribe en español claro.** Frases cortas, sin jerga innecesaria, con ejemplos concretos.

## Flujo de trabajo

```bash
# 1. Bifurca el repositorio y crea una rama
git checkout -b correccion/clase-042-fuente

# 2. Edita el manifiesto correspondiente
#    manifests/classes/part-NN.json  ·  manifests/parts/parts-NN-NN.json

# 3. Regenera y valida
python scripts/generar_clases.py
python scripts/generar_indice.py
python scripts/validar_estructura.py
python scripts/validar_encoding.py
python -m unittest discover -s tests -v

# 4. Confirma y abre un pull request
```

El pull request debe indicar: qué cambia, por qué, y qué fuente lo respalda.

## Estilo

- **Markdown:** se valida con markdownlint-cli2; la configuración está en el repositorio.
- **Python:** biblioteca estándar únicamente, líneas de hasta 100 caracteres, nombres en español
  coherentes con los existentes.
- **JSON:** una clase por objeto, campos en el orden del contrato, sin comentarios.
- **Codificación:** UTF-8 sin BOM. `validar_encoding.py` lo comprueba.

## Reportar un problema

Abre un *issue* indicando:

- **Error factual:** qué clase, qué afirma, qué es correcto y con qué fuente.
- **Enlace roto o error de formato:** qué archivo y qué esperabas.
- **Problema de accesibilidad:** qué página, con qué herramienta, qué ocurrió.
- **Desacuerdo de fondo:** cuál es la posición alternativa y qué evidencia la sostiene. Los
  desacuerdos fundados son bienvenidos: varias clases están marcadas `EN-DEBATE` precisamente
  porque el campo no tiene consenso.

## Licencia de las contribuciones

Al contribuir aceptas que tu aporte se publique bajo las licencias del proyecto:
[CC BY-NC-SA 4.0](LICENSE-CONTENT.md) para el contenido educativo y [MIT](LICENSE) para el código.
