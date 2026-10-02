"""
TEMPLATE PARA O ALUNO — TRABALHO PRÁTICO 1 (TP1)
Disciplina: Análise e Projetos de Algoritmos (APA)

Instruções:
1. Implemente seu método de ordenação autoral na função `my_authorial_sort`.
2. O retorno deve ser obrigatoriamente a tupla: (lista_ordenada, total_comparacoes, total_movimentacoes).
3. Execute este arquivo diretamente para rodar a suíte de testes de corretude e o benchmark rápido.
"""

from typing import Any, List, Tuple
import unittest

import math

def my_authorial_sort(arr: List[Any], tamanho_bloco: int = 100) -> Tuple[List[Any], int, int]:
    """
    IMPLEMENTE AQUI SEU ALGORITMO AUTORAL.

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
    """
    a = list(arr)
    n = len(a)
    comps = 0
    moves = 0

    # Estruturas principais do algoritmo autoral.

    frequencias: dict[int | float, int] = {}
    """
    frequencias = {
        numero: vezes que o numero aparece
        2: 5
        3: 7
        7.7: 1
    }
    """

    blocos: dict[int, dict] = {}
    """
    blocos = {
        id_bloco: bloco
        # [0, 100)
        0: {
            vetor = [
                [(2, 5)],
                [(3, 7)],
                vazio,
                vazio,
                vazio,
                [(7.7, 1)]
            ]
            menor_piso = 2
            maior_piso = 7
        }
    }
    """

    # Usado somente para ordenar os IDs e os decimais de uma mesma posição.
    def merge_sort(lista, chave):
        nonlocal comps, moves
        if len(lista) <= 1:
            return list(lista)

        meio = len(lista) // 2
        esquerda = merge_sort(lista[:meio], chave)
        direita = merge_sort(lista[meio:], chave)
        resultado = []
        i = j = 0

        while i < len(esquerda) and j < len(direita):
            comps += 1
            if chave(esquerda[i]) <= chave(direita[j]):
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
            moves += 1

        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        moves += len(esquerda) - i + len(direita) - j
        return resultado

    if n <= 1:
        return a, comps, moves
    else:
        for numero in a:
            if numero in frequencias:
                frequencias[numero] = frequencias[numero] + 1
            else:
                frequencias[numero] = 1
        for numero in frequencias:
            parte_inteira = math.floor(numero)
            id_bloco = parte_inteira // tamanho_bloco

            if id_bloco in blocos:
                bloco = blocos[id_bloco]
                comps += 1
                if parte_inteira < bloco["menor_piso"]:
                    bloco["menor_piso"] = parte_inteira

                comps += 1
                if parte_inteira > bloco["maior_piso"]:
                    bloco["maior_piso"] = parte_inteira
            else:
                blocos[id_bloco] = {
                    "vetor": None,
                    "menor_piso": parte_inteira,
                    "maior_piso": parte_inteira
                }

        for bloco in blocos.values():
            tamanho = bloco["maior_piso"] - bloco["menor_piso"] + 1
            bloco["vetor"] = [None] * tamanho

        for numero, quantidade in frequencias.items():
            parte_inteira = math.floor(numero)
            id_bloco = parte_inteira // tamanho_bloco
            bloco = blocos[id_bloco]

            indice = parte_inteira - bloco["menor_piso"]

            if bloco["vetor"][indice] is None:
                bloco["vetor"][indice] = []

            bloco["vetor"][indice].append((numero, quantidade))
            moves += 1

        ids_ordenados = merge_sort(list(blocos.keys()), lambda id_bloco: id_bloco)
        saida = []

        for id_bloco in ids_ordenados:
            bloco = blocos[id_bloco]
            for pares in bloco["vetor"]:
                if pares is not None:
                    pares = merge_sort(pares, lambda par: par[0])
                    for numero, quantidade in pares:
                        for _ in range(quantidade):
                            saida.append(numero)
                            moves += 1

        return saida, comps, moves


# =============================================================================
# SUÍTE DE TESTES AUTOMÁTICA DE VALIDAÇÃO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista não foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("Executando testes unitários no seu algoritmo autoral...")
    unittest.main(verbosity=2)
