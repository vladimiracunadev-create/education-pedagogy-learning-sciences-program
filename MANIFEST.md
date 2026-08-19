# Manifiesto del repositorio

> Documento generado por `scripts/generar_indice.py`. **No editar a mano:** los cambios se
> pierden en la siguiente generación. La fuente de verdad está en `manifests/`.

Inventario cuantitativo verificable. Los números se calculan contando archivos reales; no se
declaran a mano. El CI comprueba en cada push que este archivo siga coincidiendo con el
repositorio.

| Elemento | Cantidad |
|---|---:|
| Partes del currículo | 18 |
| Clases | 216 |
| Palabras en las clases | 840.621 |
| Conceptos con definición operacional | 864 |
| Señales observables exigidas | 648 |
| Obras distintas citadas en clase | 353 |
| Citas bibliográficas en clase | 432 |
| Diagramas mermaid | 234 |
| Preguntas de comprobación | 648 |
| Evidencias de aprendizaje | 216 |
| Proyectos integradores de parte | 18 |
| Proyectos integradores mayores | 5 |
| Guías de carrera por rol | 14 |
| Documentos transversales | 17 |
| Casos profesionales | 8 |
| Laboratorios | 10 |
| Plantillas de trabajo | 4 |
| Pruebas estructurales | 33 |

## Estándar de clase

Cada una de las 216 clases cumple el estándar **`clase-profunda`**: 22 secciones
obligatorias, mínimo de 2.500 palabras, un diagrama, cuatro conceptos con definición operacional,
tres señales observables, ejemplo trabajado sobre el caso de su parte, rúbrica ponderada y
fuentes con su uso declarado.

## Verificación

```bash
python scripts/generar_clases.py --check
python scripts/generar_indice.py --check
python scripts/validar_estructura.py --resumen
python scripts/validar_encoding.py
python -m unittest discover -s tests -v
```

---

[⬅ Programa](README.md) · [Estado](STATUS.md) · [Índice de archivos](FILE_INDEX.md)
