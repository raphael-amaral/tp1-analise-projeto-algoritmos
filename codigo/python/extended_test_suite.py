"""Testes complementares específicos para o algoritmo autoral de blocos."""

import random
import unittest

from student_template import my_authorial_sort


class TestCasosEspecificosDosBlocos(unittest.TestCase):
    def verificar(self, entrada, tamanho_bloco=100):
        original = list(entrada)
        resultado, comparacoes, movimentacoes = my_authorial_sort(
            entrada, tamanho_bloco
        )

        self.assertEqual(resultado, sorted(original))
        self.assertEqual(entrada, original, "A entrada original foi modificada")
        self.assertIsInstance(comparacoes, int)
        self.assertIsInstance(movimentacoes, int)
        self.assertGreaterEqual(comparacoes, 0)
        self.assertGreaterEqual(movimentacoes, 0)

    def test_decimais_com_o_mesmo_piso(self):
        self.verificar([50.7, 50.2, 50.00001, 50.1, 50.99])

    def test_decimais_negativos_com_o_mesmo_piso(self):
        self.verificar([-1.2, -1.8, -1.01, -1.999, -1.5])

    def test_fronteiras_positivas_e_negativas(self):
        self.verificar([99, 100, 199, 200, -1, -100, -101])

    def test_valores_muito_distantes(self):
        self.verificar([1, 1_000_000, 1_000_001, -1_000_000])

    def test_buracos_dentro_do_bloco(self):
        self.verificar([200, 299, 205, 290])

    def test_inteiros_e_decimais_misturados(self):
        self.verificar([2, 2.0, 2.5, -3, -3.75, 0, -0.0, 10.1])

    def test_varios_tamanhos_de_bloco(self):
        entrada = [250, 50.7, -1.2, 50.2, 250, -1.8, 50.7]
        for tamanho in (1, 10, 100, 1000):
            with self.subTest(tamanho=tamanho):
                self.verificar(entrada, tamanho)

    def test_muitos_decimais_no_mesmo_piso(self):
        random.seed(2026)
        entrada = [50 + random.random() for _ in range(1000)]
        self.verificar(entrada)

    def test_muitos_blocos_esparsos(self):
        entrada = list(range(-500_000, 500_001, 1000))
        random.Random(2026).shuffle(entrada)
        self.verificar(entrada)

    def test_escala_com_dez_mil_elementos(self):
        random.seed(2026)
        entrada = [random.randint(-100_000, 100_000) for _ in range(10_000)]
        self.verificar(entrada)


if __name__ == "__main__":
    unittest.main(verbosity=2)
