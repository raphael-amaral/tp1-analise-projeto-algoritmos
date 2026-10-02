# Código e benchmarks — TP1

Este diretório contém a implementação do algoritmo autoral de blocos, os
algoritmos fornecidos para comparação, a suíte obrigatória, testes
complementares e os benchmarks usados no relatório.

## Requisitos

- Python 3.12 ou compatível;
- Matplotlib 3.11.2 para gerar os gráficos.

Instale a dependência dentro da pasta `codigo`:

```bash
python -m pip install -r requirements.txt
```

## Testes

```bash
python python/student_template.py
python python/test_suite.py
python python/extended_test_suite.py
```

O primeiro comando executa a validação direta do algoritmo. O segundo executa
a suíte fornecida pelo professor, incluindo o caso autoral com 10.000
elementos. O terceiro cobre fronteiras de blocos, decimais, valores distantes e
diferentes tamanhos de bloco.

## Benchmarks

```bash
python python/benchmark.py --trials 10 --plot benchmark_results.png --csv benchmark_results.csv
python python/extended_benchmark.py --trials 10 --plot extended_benchmark_results.png --csv extended_benchmark_results.csv
```

Cada medição é repetida dez vezes. Bubble Sort, Selection Sort e Insertion Sort
são limitados a 1.000 elementos devido ao custo quadrático; os demais chegam a
10.000. Antes de registrar uma medição, a saída é comparada com `sorted`.

## Arquivos da implementação

- `python/student_template.py`: algoritmo autoral e contadores;
- `python/extended_test_suite.py`: testes complementares;
- `python/extended_benchmark.py`: benchmark dos casos-limite;
- `benchmark_results.csv` e `benchmark_results.png`: resultados principais;
- `extended_benchmark_results.csv` e `extended_benchmark_results.png`:
  resultados complementares.

Os arquivos `classical.py`, `authorial.py` e `test_suite.py` preservam a base
fornecida pelo professor, com a integração necessária para executar e comparar
o algoritmo autoral.
