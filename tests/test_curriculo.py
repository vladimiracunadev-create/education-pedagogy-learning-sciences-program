"""Pruebas estructurales del repositorio.

No prueban el contenido pedagógico —eso lo revisa una persona— sino las garantías que el
repositorio afirma: que el currículo está completo, que lo publicado coincide con la fuente,
que cada clase cumple su contrato y que no hay enlaces rotos.

Ejecutar con:  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "manifests"
CURRICULO = RAIZ / "curriculum"

PARTES = 18
CLASES = 216
CLASES_POR_PARTE = 12


def leer_json(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def cargar_clases() -> dict[int, dict]:
    clases: dict[int, dict] = {}
    for archivo in sorted((MANIFIESTOS / "classes").glob("*.json")):
        for registro in leer_json(archivo):
            clases[registro["n"]] = registro
    return clases


class PruebaManifiestos(unittest.TestCase):
    """La fuente de verdad debe estar completa y bien formada."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.curriculo = leer_json(MANIFIESTOS / "curriculum.json")
        cls.clases = cargar_clases()
        cls.marco = leer_json(MANIFIESTOS / "pedagogia" / "marco.json")

    def test_hay_216_clases_declaradas(self) -> None:
        self.assertEqual(len(self.curriculo), CLASES)

    def test_numeracion_global_correlativa(self) -> None:
        self.assertEqual([c["global_class"] for c in self.curriculo], list(range(1, CLASES + 1)))

    def test_hay_18_partes_con_12_clases(self) -> None:
        partes: dict[int, int] = {}
        for clase in self.curriculo:
            partes[clase["part"]] = partes.get(clase["part"], 0) + 1
        self.assertEqual(len(partes), PARTES)
        self.assertTrue(all(cantidad == CLASES_POR_PARTE for cantidad in partes.values()))

    def test_cada_clase_tiene_contenido(self) -> None:
        faltan = [c["global_class"] for c in self.curriculo if c["global_class"] not in self.clases]
        self.assertEqual(faltan, [], f"clases sin manifiesto de contenido: {faltan[:10]}")

    def test_contrato_de_datos_completo(self) -> None:
        obligatorios = {
            "n", "evidencia", "foco", "proposito", "decision", "entregable", "conceptos",
            "desarrollo", "practica", "limites", "errores", "criterios", "preguntas",
            "lecturas", "inclusion", "reto", "conexion",
        }
        for numero, registro in self.clases.items():
            with self.subTest(clase=numero):
                self.assertTrue(obligatorios <= set(registro))
                self.assertEqual(len(registro["conceptos"]), 4)
                self.assertEqual(len(registro["errores"]), 2)
                self.assertEqual(len(registro["criterios"]), 2)
                self.assertEqual(len(registro["preguntas"]), 3)
                self.assertIn(len(registro["lecturas"]), (2, 3))

    def test_estados_de_evidencia_validos(self) -> None:
        validos = set(self.marco["niveles_evidencia"])
        for numero, registro in self.clases.items():
            with self.subTest(clase=numero):
                self.assertIn(registro["evidencia"], validos)

    def test_titulos_unicos_dentro_de_cada_parte(self) -> None:
        # Entre partes distintas dos títulos se repiten a propósito: el mismo asunto tratado
        # a distinta profundidad. Dentro de una parte, un título repetido sería duplicación.
        for parte in {c["part"] for c in self.curriculo}:
            titulos = [c["title"] for c in self.curriculo if c["part"] == parte]
            with self.subTest(parte=parte):
                self.assertEqual(len(set(titulos)), len(titulos))

    def test_conceptos_con_definicion_no_vacia(self) -> None:
        for numero, registro in self.clases.items():
            for termino, definicion in registro["conceptos"]:
                with self.subTest(clase=numero, termino=termino):
                    self.assertGreater(len(termino.strip()), 2)
                    self.assertGreater(len(definicion.strip()), 20)


class PruebaCurriculoPublicado(unittest.TestCase):
    """El árbol publicado debe existir y cumplir el contrato pedagógico."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.paginas = sorted(CURRICULO.glob("part-*/class-*/README.md"))
        cls.partes = sorted(p for p in CURRICULO.glob("part-*") if p.is_dir())

    def test_hay_216_paginas_de_clase(self) -> None:
        self.assertEqual(len(self.paginas), CLASES)

    def test_hay_18_readme_de_parte(self) -> None:
        self.assertEqual(len(self.partes), PARTES)
        for parte in self.partes:
            self.assertTrue((parte / "README.md").exists(), f"falta README en {parte.name}")

    def test_secciones_obligatorias(self) -> None:
        secciones = [
            "## 🎯 Propósito", "## 📚 Resultados de aprendizaje", "## 🧭 Agenda sugerida",
            "## 🧩 Conceptos centrales", "## 🧠 Modelo mental", "## 🗺️ Flujo de razonamiento",
            "## 📖 Desarrollo", "## 📚 Lectura comparada", "## 🧮 Ejemplo trabajado",
            "## 🔀 Comparación de caminos y límites", "## 🪜 El mismo tema según el rol",
            "## 🧪 Taller guiado", "## 🏫 Caso profesional", "## 📥 Evidencia de aprendizaje",
            "## 🏆 Reto verificable", "## ✅ Evaluación de la clase", "## ⚠️ Errores frecuentes",
            "## ♿ Diversidad, accesibilidad y ética", "## 🇨🇱 Contexto chileno y cumplimiento",
            "## ❓ Preguntas de comprobación", "## 📗 Fuentes y verificación",
            "## 🔗 Conexión con el resto del programa",
        ]
        for pagina in self.paginas:
            texto = pagina.read_text(encoding="utf-8")
            with self.subTest(clase=pagina.parent.name):
                for seccion in secciones:
                    self.assertIn(seccion, texto)

    def test_cada_clase_tiene_diagrama(self) -> None:
        for pagina in self.paginas:
            with self.subTest(clase=pagina.parent.name):
                self.assertIn("```mermaid", pagina.read_text(encoding="utf-8"))

    def test_profundidad_minima(self) -> None:
        # Estándar `clase-profunda`: por debajo de 2.500 palabras la clase perdió
        # alguna de sus 22 secciones o quedó reducida a un esquema.
        for pagina in self.paginas:
            palabras = len(pagina.read_text(encoding="utf-8").split())
            with self.subTest(clase=pagina.parent.name):
                self.assertGreater(palabras, 2500)

    def test_sin_negrita_anidada(self) -> None:
        # La negrita dentro de negrita no se renderiza y ensucia el texto publicado.
        patron = re.compile(r"\*\*[^*\n]*\*\*[^*\n]*\*\*[^*\n]*\*\*\.\*\*")
        for pagina in self.paginas:
            with self.subTest(clase=pagina.parent.name):
                self.assertIsNone(patron.search(pagina.read_text(encoding="utf-8")))

    def test_caso_de_la_parte_en_cada_clase(self) -> None:
        # El ejemplo trabajado y el caso profesional usan el caso persistente de la parte.
        casos = leer_json(MANIFIESTOS / "pedagogia" / "casos.json")["partes"]
        for pagina in self.paginas:
            parte = str(int(pagina.parent.parent.name.split("-")[1]))
            inicio = casos[parte]["caso"][:60]
            with self.subTest(clase=pagina.parent.name):
                self.assertIn(inicio, pagina.read_text(encoding="utf-8"))

    def test_titulo_con_formato_correcto(self) -> None:
        for pagina in self.paginas:
            texto = pagina.read_text(encoding="utf-8")
            with self.subTest(clase=pagina.parent.name):
                self.assertRegex(texto, re.compile(r"^# Clase \d{3} — .+$", re.M))


class PruebaSincronia(unittest.TestCase):
    """Lo publicado debe coincidir exactamente con lo generado desde la fuente."""

    def ejecutar(self, script: str, *argumentos: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(RAIZ / "scripts" / script), *argumentos],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    def test_curriculo_sincronizado(self) -> None:
        resultado = self.ejecutar("generar_clases.py", "--check")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_documentos_generados_al_dia(self) -> None:
        resultado = self.ejecutar("generar_indice.py", "--check")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_estructura_valida(self) -> None:
        resultado = self.ejecutar("validar_estructura.py")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_codificacion_limpia(self) -> None:
        resultado = self.ejecutar("validar_encoding.py")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_sitio_compila(self) -> None:
        resultado = self.ejecutar("generar_sitio.py", "--check")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_paquete_de_capacitacion_compila(self) -> None:
        resultado = self.ejecutar("exportar_capacitacion.py", "--check")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)


class PruebaRutasPorRol(unittest.TestCase):
    """Las guías de carrera deben estar completas, enlazadas y ser navegables."""

    SECCIONES = [
        "## 🧭 Qué es y por qué importa",
        "## 🗓️ Un día en el puesto",
        "## 🧠 Qué necesitas saber",
        "## 📚 Tu ruta en el programa",
        "## 📈 Progresión",
        "## ⚠️ Mitos y errores comunes",
        "## 🚀 Siguientes pasos",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.carpeta = RAIZ / "rutas"
        cls.guias = sorted(p for p in cls.carpeta.glob("*.md") if p.name != "README.md")
        cls.indice = (cls.carpeta / "README.md").read_text(encoding="utf-8")

    def test_existen_las_guias(self) -> None:
        self.assertGreaterEqual(len(self.guias), 10)

    def test_secciones_obligatorias(self) -> None:
        for guia in self.guias:
            texto = guia.read_text(encoding="utf-8")
            with self.subTest(rol=guia.stem):
                for seccion in self.SECCIONES:
                    self.assertIn(seccion, texto)

    def test_enlazadas_desde_el_indice(self) -> None:
        for guia in self.guias:
            with self.subTest(rol=guia.stem):
                self.assertIn(guia.name, self.indice)

    def test_profundidad_minima(self) -> None:
        for guia in self.guias:
            with self.subTest(rol=guia.stem):
                self.assertGreater(len(guia.read_text(encoding="utf-8").split()), 700)

    def test_navegacion_de_retorno(self) -> None:
        for guia in self.guias:
            texto = guia.read_text(encoding="utf-8")
            with self.subTest(rol=guia.stem):
                self.assertIn("Volver al índice de rutas", texto)

    def test_enlazadas_desde_el_readme_principal(self) -> None:
        readme = (RAIZ / "README.md").read_text(encoding="utf-8")
        for guia in self.guias:
            with self.subTest(rol=guia.stem):
                self.assertIn(f"rutas/{guia.name}", readme)


class PruebaDocumentacion(unittest.TestCase):
    """Los documentos que el programa promete deben existir y estar enlazados."""

    def test_documentos_de_raiz(self) -> None:
        for nombre in ("README.md", "CURRICULUM.md", "SYLLABUS.md", "STATUS.md", "ROADMAP.md",
                       "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
                       "SUPPORT.md", "LICENSE", "LICENSE-CONTENT.md", "FILE_INDEX.md",
                       "VERSION", "catalog.json"):
            with self.subTest(archivo=nombre):
                self.assertTrue((RAIZ / nombre).exists(), f"falta {nombre}")

    def test_documentos_transversales(self) -> None:
        esperados = {
            "METODOLOGIA.md", "ESTANDARES_DE_EVIDENCIA.md", "ETICA_Y_PRACTICA_RESPONSABLE.md",
            "BIBLIOGRAFIA.md", "FUENTES.md", "GLOSARIO.md", "GUIA_DEL_ESTUDIANTE.md",
            "GUIA_DEL_FORMADOR.md", "RUTAS_DE_APRENDIZAJE.md", "SISTEMA_DE_EVALUACION.md",
            "INCLUSION_Y_DUA.md", "ACCESIBILIDAD.md", "IA_EN_EDUCACION.md", "MARCO_CHILE.md",
            "MIGRACION_A_CAPACITACION.md", "ARQUITECTURA.md", "PREGUNTAS_FRECUENTES.md",
        }
        presentes = {p.name for p in (RAIZ / "docs").glob("*.md")}
        self.assertTrue(esperados <= presentes, f"faltan: {sorted(esperados - presentes)}")

    def test_catalogo_coherente_con_el_curriculo(self) -> None:
        catalogo = leer_json(RAIZ / "catalog.json")
        self.assertEqual(catalogo["clases"], CLASES)
        self.assertEqual(catalogo["partes"], PARTES)
        self.assertEqual(len(catalogo["catalogo"]), CLASES)
        for registro in catalogo["catalogo"]:
            with self.subTest(clase=registro["n"]):
                self.assertTrue((RAIZ / registro["ruta"]).exists())

    def test_status_declara_las_cifras_reales(self) -> None:
        status = (RAIZ / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("| Clases | 216 |", status)
        self.assertIn("| Partes | 18 |", status)

    def test_version_semantica(self) -> None:
        version = (RAIZ / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
