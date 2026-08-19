.PHONY: help generar indice actividades validar test sitio capacitacion lint todo limpiar

PYTHON ?= python

help:  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

generar:  ## Regenera curriculum/ desde los manifiestos
	$(PYTHON) scripts/generar_clases.py

indice:  ## Regenera STATUS, SYLLABUS, FILE_INDEX, GLOSARIO y catalog.json
	$(PYTHON) scripts/generar_indice.py

actividades:  ## Regenera el banco de actividades prácticas
	$(PYTHON) scripts/generar_actividades.py

validar:  ## Validación estricta: la misma que corre en CI
	$(PYTHON) scripts/generar_clases.py --check
	$(PYTHON) scripts/generar_indice.py --check
	$(PYTHON) scripts/generar_actividades.py --check
	$(PYTHON) scripts/validar_estructura.py --resumen
	$(PYTHON) scripts/validar_encoding.py

test:  ## Ejecuta las pruebas estructurales
	$(PYTHON) -m unittest discover -s tests -v

sitio:  ## Genera el sitio estático en site/
	$(PYTHON) scripts/generar_sitio.py

capacitacion:  ## Genera el paquete para LMS en capacitacion/
	$(PYTHON) scripts/exportar_capacitacion.py

lint:  ## Comprueba el Markdown con markdownlint-cli2
	npx --yes markdownlint-cli2@0.18.1 "**/*.md"

todo: generar indice actividades validar test sitio capacitacion  ## Todo lo que exige CI

limpiar:  ## Borra artefactos generados y cachés
	rm -rf site capacitacion .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
