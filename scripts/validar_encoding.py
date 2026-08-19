#!/usr/bin/env python3
"""Comprueba que todo el texto del repositorio sea UTF-8 limpio.

Detecta tres problemas que arruinan un repositorio en español y que pasan
inadvertidos hasta que alguien abre el archivo en otro sistema:

1. BOM al inicio del archivo (rompe el primer encabezado y algunos parsers).
2. Bytes que no son UTF-8 válido.
3. Mojibake: texto UTF-8 que fue leído como Latin-1 y vuelto a guardar, de modo
   que una vocal acentuada aparece como dos caracteres extraños en su lugar.

Uso:
  python scripts/validar_encoding.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

EXTENSIONES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".html", ".css", ".js", ".csv", ".toml"}
IGNORADOS = {".git", "node_modules", ".venv", "venv", "__pycache__", "site", "capacitacion",
             ".ruff_cache", ".pytest_cache", ".cache", "output"}

# Secuencias que solo aparecen cuando UTF-8 se interpretó como Latin-1 o cp1252.
# Se construyen en tiempo de ejecución y no como literales: escribirlas a mano haría
# que este mismo archivo fuera detectado como corrupto por su propia comprobación.
def _corromper(texto: str) -> str:
    return texto.encode("utf-8").decode("latin-1")


MOJIBAKE = tuple(_corromper(caracter) for caracter in "áéíóúñÑ¿¡—“”…🎓")


def archivos() -> list[Path]:
    encontrados = []
    for ruta in RAIZ.rglob("*"):
        if not ruta.is_file() or ruta.suffix.lower() not in EXTENSIONES:
            continue
        if any(parte in IGNORADOS for parte in ruta.relative_to(RAIZ).parts):
            continue
        encontrados.append(ruta)
    return sorted(encontrados)


def main() -> int:
    fallos: list[str] = []
    revisados = 0

    for ruta in archivos():
        revisados += 1
        relativo = ruta.relative_to(RAIZ).as_posix()
        bruto = ruta.read_bytes()

        if bruto.startswith(b"\xef\xbb\xbf"):
            fallos.append(f"{relativo}: tiene BOM UTF-8 al inicio")
            continue
        try:
            texto = bruto.decode("utf-8")
        except UnicodeDecodeError as fallo:
            fallos.append(f"{relativo}: no es UTF-8 válido ({fallo.reason} en el byte {fallo.start})")
            continue

        for secuencia in MOJIBAKE:
            if secuencia in texto:
                linea = next((i for i, l in enumerate(texto.splitlines(), 1) if secuencia in l), 0)
                fallos.append(f"{relativo}:{linea}: mojibake detectado («{secuencia}»)")
                break

    if fallos:
        print(f"FALLÓ: {len(fallos)} archivo(s) con problemas de codificación.")
        for fallo in fallos[:30]:
            print(f"  - {fallo}")
        return 1

    print(f"OK: {revisados} archivos en UTF-8 sin BOM ni mojibake.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
