"""Pruebas del registro de fuentes.

No comprueban que la obra diga lo que la clase afirma —eso lo comprueba quien la
lee— sino la garantía que el registro promete: que toda obra citada está en él y
que ningún localizador publicado es inventado.

Ejecutar con:  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))

import fuentes as F  # noqa: E402

ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PruebaEsquemaDelRegistro(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registro = F.cargar_registro()
        cls.entradas = cls.registro["entries"]

    def test_el_registro_declara_su_esquema_y_su_politica(self) -> None:
        self.assertEqual(self.registro["schema_version"], F.ESQUEMA)
        self.assertRegex(self.registro["verified_on"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertTrue(self.registro["policy"].strip())

    def test_los_identificadores_son_unicos_y_kebab_case(self) -> None:
        ids = [e["id"] for e in self.entradas]
        self.assertEqual(len(ids), len(set(ids)))
        for ident in ids:
            self.assertRegex(ident, ID)

    def test_cada_entrada_declara_tipo_y_estado_conocidos(self) -> None:
        for entrada in self.entradas:
            self.assertIn(entrada["type"], F.TIPOS, entrada["id"])
            self.assertIn(entrada["status"], F.ESTADOS, entrada["id"])
            self.assertTrue(entrada["title"].strip(), entrada["id"])


class PruebaLocalizadores(unittest.TestCase):
    """Un localizador publicado tiene que ser comprobable; si no, es pendiente."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.entradas = F.cargar_registro()["entries"]

    def test_los_libros_verificados_llevan_isbn13_con_digito_valido(self) -> None:
        for entrada in self.entradas:
            if entrada["status"] == "verificada" and entrada["type"] == "book":
                self.assertTrue(F.isbn13_valido(entrada.get("isbn13", "")), entrada["id"])

    def test_los_articulos_verificados_llevan_doi(self) -> None:
        for entrada in self.entradas:
            if entrada["status"] == "verificada" and entrada["type"] == "paper":
                self.assertTrue(F.doi_valido(entrada.get("doi", "")), entrada["id"])

    def test_el_locator_es_la_forma_canonica_de_su_tipo(self) -> None:
        for entrada in self.entradas:
            canonico = F.locator_canonico(entrada)
            if canonico:
                self.assertEqual(entrada.get("locator"), canonico, entrada["id"])
            elif entrada["status"] == "verificada":
                self.assertRegex(entrada.get("locator", ""), F.URL_RE, entrada["id"])
                self.assertRegex(entrada.get("accessed", ""), F.FECHA_RE, entrada["id"])

    def test_lo_pendiente_no_trae_localizador_a_medias(self) -> None:
        for entrada in self.entradas:
            if entrada["status"] != "pendiente":
                continue
            for campo in ("isbn13", "doi", "locator"):
                self.assertFalse(str(entrada.get(campo, "")).strip(), entrada["id"])
            self.assertTrue(entrada.get("nota", "").strip(), entrada["id"])

    def test_el_digito_de_control_del_isbn_se_calcula_de_verdad(self) -> None:
        self.assertTrue(F.isbn13_valido("9780262035613"))
        self.assertFalse(F.isbn13_valido("9780262035614"))
        self.assertFalse(F.isbn13_valido("978026203561"))
        self.assertTrue(F.doi_valido("10.3102/003465430298487"))
        self.assertFalse(F.doi_valido("doi:10.3102/003465430298487"))


class PruebaCobertura(unittest.TestCase):
    """El registro y los manifiestos describen el mismo conjunto de obras."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.entradas = F.cargar_registro()["entries"]
        cls.usos = F.usos_por_cita()

    def test_toda_obra_citada_esta_en_el_registro(self) -> None:
        citas = {e["cita"] for e in self.entradas}
        faltan = [c for c in self.usos if c not in citas]
        self.assertEqual(faltan, [], f"{len(faltan)} obras citadas fuera del registro")

    def test_ninguna_entrada_sobra(self) -> None:
        for entrada in self.entradas:
            self.assertIn(entrada["cita"], self.usos, entrada["id"])
            self.assertEqual(entrada["used_in"], self.usos[entrada["cita"]], entrada["id"])

    def test_los_usos_apuntan_a_paginas_existentes(self) -> None:
        for entrada in self.entradas:
            self.assertTrue(entrada["used_in"], entrada["id"])
            for ruta in entrada["used_in"]:
                self.assertTrue((RAIZ / ruta).exists(), f"{entrada['id']} → {ruta}")


class PruebaCandidatos(unittest.TestCase):
    """Las URLs propuestas son propuestas: ninguna entra al registro sin comprobarse."""

    def test_los_candidatos_apuntan_a_entradas_reales(self) -> None:
        ruta = RAIZ / "sources" / "candidatos-normativos.json"
        if not ruta.exists():
            self.skipTest("no hay candidatos declarados")
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        ids = {e["id"] for e in F.cargar_registro()["entries"]}
        for ident, candidato in datos["candidatos"].items():
            self.assertIn(ident, ids, f"candidato sin entrada: {ident}")
            urls = candidato.get("urls") or [candidato.get("url", "")]
            for url in urls:
                self.assertRegex(url, F.URL_RE, ident)


if __name__ == "__main__":
    unittest.main()
