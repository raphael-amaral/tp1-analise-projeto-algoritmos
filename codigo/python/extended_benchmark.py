"""Benchmark complementar para cenários específicos do algoritmo de blocos."""

import argparse
import csv
import gc
import random
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from authorial import dpes_sort
from classical import merge_sort, quick_sort
from student_template import my_authorial_sort


ALGORITMOS = {
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Authorial (DPES)": dpes_sort,
    "Autoral (Blocos)": my_authorial_sort,
}


def gerar_entrada(n, distribuicao, repeticao):
    gerador = random.Random(2026 + repeticao)

    if distribuicao == "decimais_mesmo_piso":
        return [50 + gerador.random() for _ in range(n)]

    if distribuicao == "decimais_espalhados":
        return [gerador.uniform(-10 * n, 10 * n) for _ in range(n)]

    if distribuicao == "blocos_esparsos":
        entrada = [i * 10_000 for i in range(n)]
        gerador.shuffle(entrada)
        return entrada

    if distribuicao == "buracos_internos":
        entrada = []
        for i in range(n):
            bloco = i // 2
            entrada.append(bloco * 100 + (0 if i % 2 == 0 else 99))
        gerador.shuffle(entrada)
        return entrada

    raise ValueError(f"Distribuição desconhecida: {distribuicao}")


def executar(tamanhos, distribuicoes, repeticoes):
    resultados = {distribuicao: {} for distribuicao in distribuicoes}

    for distribuicao in distribuicoes:
        print(f"\nBenchmark complementar: [{distribuicao}]")
        for nome, algoritmo in ALGORITMOS.items():
            resultados[distribuicao][nome] = {}

        for n in tamanhos:
            entradas = [
                gerar_entrada(n, distribuicao, repeticao)
                for repeticao in range(repeticoes)
            ]

            for nome, algoritmo in ALGORITMOS.items():
                tempos = []
                comparacoes = []
                movimentacoes = []

                for entrada in entradas:
                    gc_ativo = gc.isenabled()
                    gc.disable()
                    try:
                        inicio = time.perf_counter()
                        resultado, comps, moves = algoritmo(list(entrada))
                        tempo = (time.perf_counter() - inicio) * 1000
                    finally:
                        if gc_ativo:
                            gc.enable()
                    tempos.append(tempo)
                    comparacoes.append(comps)
                    movimentacoes.append(moves)
                    assert resultado == sorted(entrada), f"Falha em {nome}"

                resultados[distribuicao][nome][n] = {
                    "tempo": sum(tempos) / repeticoes,
                    "comparacoes": sum(comparacoes) / repeticoes,
                    "movimentacoes": sum(movimentacoes) / repeticoes,
                }
            print(f"  N={n} concluído")

    return resultados


def gerar_grafico(resultados, caminho):
    distribuicoes = list(resultados)
    fig, eixos = plt.subplots(
        len(distribuicoes), 3, figsize=(20, 4 * len(distribuicoes))
    )

    for linha, distribuicao in enumerate(distribuicoes):
        for nome, tamanhos in resultados[distribuicao].items():
            ns = sorted(tamanhos)
            eixos[linha][0].plot(
                ns, [tamanhos[n]["tempo"] for n in ns], marker="o", label=nome
            )
            eixos[linha][1].plot(
                ns,
                [tamanhos[n]["comparacoes"] for n in ns],
                marker="s",
                label=nome,
            )
            eixos[linha][2].plot(
                ns,
                [tamanhos[n]["movimentacoes"] for n in ns],
                marker="^",
                label=nome,
            )

        titulo = distribuicao.replace("_", " ").title()
        nomes = ("Tempo Médio (ms)", "Comparações", "Movimentações")
        for coluna, nome_eixo in enumerate(nomes):
            eixo = eixos[linha][coluna]
            eixo.set_title(f"{nome_eixo} — [{titulo}]")
            eixo.set_xlabel("Tamanho da Entrada (N)")
            eixo.set_ylabel(nome_eixo)
            eixo.set_xscale("log")
            eixo.set_xticks(ns)
            eixo.xaxis.set_major_formatter(ScalarFormatter())
            eixo.grid(True, linestyle="--", alpha=0.6)
            eixo.legend()

    plt.tight_layout()
    plt.savefig(caminho, dpi=150)
    print(f"\nGráfico salvo em: {caminho}")


def imprimir_resumo(resultados):
    for distribuicao, algoritmos in resultados.items():
        print(f"\n### {distribuicao.replace('_', ' ').title()} — tempo em ms")
        for nome, tamanhos in algoritmos.items():
            valores = ", ".join(
                f"N={n}: {metricas['tempo']:.3f}"
                for n, metricas in sorted(tamanhos.items())
            )
            print(f"{nome}: {valores}")


def salvar_csv(resultados, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([
            "distribuicao", "algoritmo", "n", "tempo_medio_ms",
            "comparacoes_medias", "movimentacoes_medias"
        ])
        for distribuicao, algoritmos in resultados.items():
            for algoritmo, tamanhos in algoritmos.items():
                for n, metricas in sorted(tamanhos.items()):
                    writer.writerow([
                        distribuicao,
                        algoritmo,
                        n,
                        f"{metricas['tempo']:.6f}",
                        f"{metricas['comparacoes']:.2f}",
                        f"{metricas['movimentacoes']:.2f}",
                    ])
    print(f"Dados salvos em: {caminho}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark complementar do TP1")
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--plot", default="extended_benchmark_results.png")
    parser.add_argument("--csv", default="extended_benchmark_results.csv")
    args = parser.parse_args()

    tamanhos = [10, 50, 100, 250, 500, 1000, 10000]
    distribuicoes = [
        "decimais_mesmo_piso",
        "decimais_espalhados",
        "blocos_esparsos",
        "buracos_internos",
    ]
    resultados = executar(tamanhos, distribuicoes, args.trials)
    imprimir_resumo(resultados)
    salvar_csv(resultados, args.csv)
    gerar_grafico(resultados, args.plot)


if __name__ == "__main__":
    main()
