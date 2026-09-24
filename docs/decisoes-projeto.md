# Decisões e proposta conceitual do TP1

Registro consolidado em 24/09/2026. Este documento reúne as decisões da conversa e a análise preliminar. Não substitui o relatório final nem comprova originalidade ou desempenho experimental.

Referências locais: [enunciado](enunciado.md), [pseudocódigo atual](../pseudocodigo.txt) e [raciocínio inicial escrito pelo aluno](raciocinio-projetual.txt). O texto pessoal do aluno foi preservado.

## 1. Objetivo e estado atual

A proposta busca ordenar números usando seus valores para determinar posições em vetores, evitando comparar todos os valores entre si. Combina contagem prévia de frequências, blocos criados sob demanda, indexação por piso e ordenação local quando necessária.

A base que o aluno deseja preservar é a ordenação por índices. Comparações continuam necessárias para ordenar os identificadores dos blocos e os valores distintos que compartilham um piso.

O fluxo conceitual e o pseudocódigo estão definidos. A implementação própria, sua instrumentação e os experimentos ainda não foram realizados. O template Python contém o Insertion Sort de exemplo; o DPES é a referência fornecida no pacote. Testes anteriores do material de apoio não validam a nova proposta.

## 2. Decisões adotadas

| Aspecto | Decisão |
|---|---|
| Linguagem | Python |
| Entrada | Inteiros e floats finitos, incluindo negativos |
| Valores equivalentes | `2` e `2.0` compartilham contagem; `-0.0` e `0.0` também |
| Identidade das ocorrências | Não preservar diferenças de tipo entre valores equivalentes nem o sinal do zero |
| Valores especiais | Rejeitar NaN e infinitos |
| Capacidade lógica | Parâmetro inteiro positivo `B`, padrão 100 |
| Seleção automática de B | Não será adotada nesta versão |
| Tamanho físico dos vetores | Ajustado ao menor e maior piso de cada bloco |
| Ordenações auxiliares | Merge Sort instrumentado para IDs e pares de cada posição |
| Memória | Manter dicionário de frequências e blocos em memória, priorizando simplicidade |
| Saída | Nova lista em ordem crescente; entrada não modificada |
| Interface com o pacote | Na implementação instrumentada, retornar lista, comparações e movimentações, conforme o template |

O pseudocódigo mostra apenas a saída numérica para facilitar a compreensão. Os contadores serão incorporados posteriormente. Detalhes de validação de tipos, como aceitar ou rejeitar `bool` (subtipo de inteiro em Python), ainda precisam ser explicitados antes da implementação.

## 3. Estruturas de dados

- `frequencias`: dicionário de valor completo para quantidade de ocorrências.
- `blocos`: dicionário de identificador para um registro com `menorPiso`, `maiorPiso` e `vetor`.
- Cada posição do vetor começa vazia. Quando ocupada, guarda uma lista de pares `(valorCompleto, quantidade)`.
- `saida`: lista final, com as repetições expandidas.

Não é necessário manter um segundo dicionário de frequências dentro de cada posição: o dicionário global já agregou os valores iguais.

## 4. Mapeamento e limites

Para cada valor `x`:

```text
k = piso(x)
idBloco = k // B
```

`piso` arredonda para baixo. A divisão inteira também segue o arredondamento para baixo, como em Python. Por exemplo, `piso(-1.2) = -2` e `-2 // 100 = -1`.

O bloco de ID `q` representa a faixa lógica `[q × B, (q + 1) × B)`. Esses limites são fixos para um B escolhido e não se sobrepõem.

Depois de descobrir os pisos presentes em cada bloco:

```text
tamanhoDoVetor = maiorPiso - menorPiso + 1
indice = piso(x) - menorPiso
```

O índice final usa o deslocamento pelo menor piso, não mais `k % B`. O vetor representa apenas a parte utilizada da faixa lógica.

Exemplo: com B = 100, os valores 240, 245 e 250 pertencem ao bloco 2. Seu vetor tem 11 posições, com índices 0, 5 e 10. Com apenas 250, o vetor tem uma posição.

## 5. Fluxo completo

1. Validar B como inteiro positivo.
2. Percorrer a entrada, validar os números e construir o dicionário de frequências.
3. Percorrer as chaves distintas para descobrir os blocos ocupados e seus menores e maiores pisos. Ainda não criar os vetores.
4. Criar o vetor de cada bloco com `maiorPiso - menorPiso + 1` posições vazias.
5. Percorrer novamente os pares do dicionário e distribuí-los usando o índice relativo ao menor piso do bloco.
6. Ordenar os IDs dos blocos com Merge Sort.
7. Percorrer os blocos nessa ordem e suas posições em ordem crescente de índice.
8. Ignorar posições vazias. Nas posições com mais de um par, ordenar os pares pelo valor completo usando Merge Sort.
9. Emitir cada valor tantas vezes quanto sua frequência indicar.
10. Retornar a nova lista e, na implementação instrumentada, as métricas.

Para entrada vazia, o resultado é vazio. A ordenação de listas vazias ou unitárias deve ser tratada normalmente pelo Merge Sort.

## 6. Exemplo de execução

Entrada: `[250, 50.7, -1.2, 50.2, 250, -1.8, 50.7]`, com B = 100.

Após a contagem:

```text
250: 2
50.7: 2
-1.2: 1
50.2: 1
-1.8: 1
```

| Bloco | Menor piso | Maior piso | Tamanho físico | Conteúdo da posição 0 |
|---|---:|---:|---:|---|
| 2 | 250 | 250 | 1 | `(250, 2)` |
| 0 | 50 | 50 | 1 | `(50.7, 2), (50.2, 1)` |
| -1 | -2 | -2 | 1 | `(-1.2, 1), (-1.8, 1)` |

Os IDs ordenados são `[-1, 0, 2]`. Os valores de cada posição são ordenados localmente quando necessário. O bloco 1 não é criado.

Saída: `[-1.8, -1.2, 50.2, 50.7, 50.7, 250, 250]`.

## 7. Tratamento dos decimais

O piso serve somente para localizar uma faixa. Guardamos e emitimos os valores completos, sem arredondá-los e sem reconstruí-los a partir dos índices.

Valores como 50.2, 50.7 e 50.00001 compartilham a posição associada ao piso 50, mas permanecem em pares distintos. A ordenação local determina sua ordem.

A preservação é dos valores numéricos recebidos. Não se promete recuperar a representação decimal textual original de um float. Valores numericamente equivalentes podem compartilhar o representante guardado no dicionário.

Se todos os valores distintos estiverem entre 50 e 51, a ordenação local concentrará todo o trabalho de comparação entre esses valores.

## 8. Escolha de B e limitações aceitas

B permanece configurável e igual a 100 por padrão. Não há afirmação de que 100 seja ótimo. B controla o agrupamento lógico; não obriga a alocar B posições em todos os blocos.

O ajuste por mínimo e máximo elimina espaços vazios nas extremidades e o desperdício de B posições quando há um único piso no bloco. Ele não elimina buracos internos.

| Pisos no bloco, B = 100 | Posições alocadas | Posições ocupadas |
|---|---:|---:|
| 250 | 1 | 1 |
| 240, 245, 250 | 11 | 3 |
| 200, 299 | 100 | 2 |

Com valores 0, 100, 200 e 300, criam-se quatro blocos de uma posição cada. Continua sendo necessário ordenar seus quatro IDs.

B maior pode diminuir a quantidade de blocos, mas juntar pisos distantes e aumentar buracos internos. B menor pode produzir mais IDs para ordenar. Uma posição ocupada pode conter muitos decimais distintos; isso não aumenta o comprimento do vetor, mas aumenta a lista local.

## 9. Fundamentação preliminar de corretude

### Invariantes

1. Contagem: após ler um prefixo da entrada, as frequências representam exatamente suas ocorrências.
2. Descoberta dos limites: cada registro contém os extremos dos pisos já examinados que pertencem ao seu bloco.
3. Distribuição: cada chave já processada está em uma única posição, acompanhada de sua frequência original. Seu índice está entre zero e o tamanho do vetor menos um.
4. Reconstrução: após concluir cada posição, a saída está ordenada e contém exatamente as ocorrências das posições já visitadas.

### Por que a saída fica ordenada

IDs crescentes representam faixas numéricas crescentes e disjuntas. Dentro de um bloco, índices crescentes representam pisos crescentes. Se `piso(x) < piso(y)`, então `x < y`. Quando os pisos coincidem, o Merge Sort estabelece a ordem pelos valores completos. A emissão pelas frequências preserva as multiplicidades.

Os percursos são finitos e o Merge Sort termina por reduzir os subproblemas. O relatório final deve desenvolver a inicialização, manutenção e término dos invariantes, além das propriedades do método auxiliar.

## 10. Análise preliminar de tempo e espaço

### Parâmetros

| Símbolo | Significado |
|---|---|
| n | Total de ocorrências da entrada |
| d | Quantidade de valores distintos |
| b | Quantidade de blocos ocupados; não confundir com B |
| B | Capacidade lógica configurada |
| L_j | Comprimento físico do vetor do bloco j |
| S | Soma dos comprimentos físicos: `S = soma L_j` |
| d_i | Quantidade de valores distintos com o mesmo piso i |

Para blocos ocupados, `1 <= L_j <= B`, portanto `S <= bB`. Também `d <= n`, `b <= d` e `soma d_i = d`. Não se deve presumir `d <= S`: vários decimais distintos podem ocupar uma única posição.

### Hipóteses

A análise abaixo assume hashing com custo esperado constante, aritmética e comparações de custo constante e Merge Sort com limite O(k log k). Inteiros Python de tamanho arbitrário exigem considerar o custo em bits se quisermos uma análise além desse modelo simplificado. As garantias esperadas do hashing não são garantias determinísticas de pior caso.

| Etapa | Custo sob essas hipóteses |
|---|---|
| Validar e contar entrada | O(n) esperado |
| Descobrir limites e distribuir pares | O(d) esperado |
| Inicializar e percorrer vetores | O(S) |
| Ordenar IDs | O(b log b) |
| Ordenar pares por posição | O(soma d_i log d_i) |
| Construir saída | Theta(n) |

Limite total:

```text
O(n + S + b log b + soma(d_i log d_i))
```

Consideramos os termos de ordenação nulos para listas vazias ou unitárias. O termo d é absorvido por n. O ajuste de extremos substitui o antigo custo de varredura e alocação bB por S, que pode ser muito menor.

Memória auxiliar, excluindo a saída: `O(d + S)`, admitindo buffers de Merge Sort até lineares. A nova saída acrescenta `Theta(n)`. A proposta não é in-place.

### Casos relevantes

- Todos iguais: um par, um bloco e uma posição; tempo Theta(n) no modelo de hashing adotado.
- Todos distintos em uma única faixa inteira: ordenação local O(d log d), além da leitura e emissão.
- Um valor por bloco: S = b = d; a ordenação dos IDs continua O(d log d), mas não há vetores inteiros de B posições desperdiçados.
- Apenas inteiros: no máximo um valor distinto por piso, eliminando a ordenação local dos pares.
- B constante: o limite geral sob hashing esperado é O(n + d log d); não há melhoria geral de classe assintótica em relação a contar e ordenar todas as chaves.
- B variável: manter S explícito, pois buracos internos podem dominar tempo e memória.
- Colisões desfavoráveis de hashing podem produzir custo quadrático. O uso de Merge Sort evita quadrático nas ordenações auxiliares, não em toda operação possível do algoritmo.

Ainda é necessário formalizar melhor, médio e pior caso para a implementação escolhida. Caso médio exige hipóteses sobre as entradas; entrada ordenada ou reversa não identifica automaticamente melhor ou pior caso desta proposta.

## 11. Vantagens esperadas e limites

As vantagens são hipóteses fundamentadas pelo mecanismo, ainda sem medição:

- Repetições são agregadas antes da distribuição; esta trabalha com d pares, não n ocorrências.
- Não se alocam blocos intermediários sem valores.
- Vetores ajustados não alocam posições anteriores ao menor piso nem posteriores ao maior piso de cada bloco.
- Os índices estabelecem a ordem entre pisos, restringindo comparações aos IDs e às listas locais.

Muitas repetições também favorecem a alternativa simples de dicionário seguido de ordenação de chaves. O benefício específico dos blocos precisa ser medido contra essa alternativa.

Permanecem os custos de hashing, alocação, listas locais, buracos internos, ordenação de IDs e ordenação de muitos decimais com o mesmo piso. A proposta não explora automaticamente uma entrada já ordenada.

Quanto à estabilidade, a contagem não preserva a identidade ou a ordem original de registros com chaves equivalentes. A versão atual ordena valores numéricos; não deve ser apresentada como uma ordenação estável de registros só porque utiliza Merge Sort.

## 12. Autoria, antecedentes e contribuição candidata

Descrição de trabalho, ainda sem nome definitivo:

> Adaptação de ordenação por distribuição que agrega frequências e organiza valores distintos em blocos esparsos de posições indexadas, com vetores limitados pelos extremos locais e ordenação por comparação apenas nos IDs e nas listas que compartilham um piso.

O dicionário muda a representação do trabalho posterior; os blocos sob demanda evitam faixas globais vazias; os extremos reduzem a alocação dentro dos blocos; a indexação ordena pisos; a ordenação local suporta decimais sem escala global. Essas são mudanças concretas que devem ser avaliadas em conjunto.

Bucket Sort, Counting Sort, histogramas esparsos e combinações de distribuição e contagem são antecedentes. As buscas da conversa não confirmaram uma implementação exatamente equivalente a todo o fluxo atual, mas também não demonstraram ineditismo. A adequação ao requisito de adaptação estrutural profunda permanece uma avaliação a fundamentar.

O DPES fornecido também combina mecanismos: extremos, pivôs interpolados, particionamento triplo, recursão e Insertion Sort em segmentos pequenos. Isso mostra que combinar técnicas é compatível com a proposta didática; não comprova automaticamente a originalidade de qualquer combinação.

Referências identificadas para comparação, sem afirmar equivalência integral:

- [Bucket Sort — NIST](https://xlinux.nist.gov/dads/HTML/bucketsort.html): distribuição, ordenação dos grupos e concatenação.
- [Counting Sort e Radix Sort — Open Data Structures](https://www.opendatastructures.org/ods-python/11_2_Counting_Sort_Radix_So.html): mecanismos de contagem e indexação.
- [Counter — documentação Python](https://docs.python.org/3/library/collections.html#collections.Counter): representação de frequências em dicionário.
- [Histogram construction with counting sort — BitMagic](https://bitmagic.io/hist-sort): uso de representação esparsa/comprimida para contagem, diferente dos vetores locais aqui propostos.
- [Recombinant Sort](https://arxiv.org/abs/2107.01391): combinação de distribuição, contagem e indexação multidimensional, incluindo limites de percurso. Seu mecanismo não é o mesmo fluxo descrito aqui; suas alegações de desempenho não foram adotadas como prova para nossa proposta.

## 13. Alternativas discutidas e não adotadas

- Vetor único indexado pelo valor: problema de faixas muito grandes e vazias.
- Blocos centrados no primeiro valor: exigiriam resolver sobreposições e regras dependentes da ordem de chegada.
- Escala decimal fixa ou adaptativa: restringe a precisão ou pode separar demais os valores após a escala.
- Transformação ordenável dos bits do float: mais complexa e altera o significado da proximidade usada nos blocos.
- Substituir blocos esparsos por ordenação direta de pares: não foi adotado como estratégia interna, para preservar a indexação como base.
- Desvio-padrão para escolher B: dispersão global não descreve adequadamente grupos locais distantes.
- Escolha automática entre capacidades candidatas: discutida e adiada; B permanece parâmetro manual.

## 14. Validação planejada e pendências do enunciado

Antes de implementar:

- Revisar o pseudocódigo e este registro com o aluno.
- Definir precisamente as regras de contagem de comparações e movimentações. Hashing interno não instrumentado não deve ser apresentado como comparação medida.
- Desenvolver a prova de corretude e explicitar as hipóteses da análise.

Na implementação e nos testes:

- Implementar a solução e o Merge Sort instrumentado para IDs e pares.
- Integrar o algoritmo à suíte principal e ao benchmark; o template isolado não faz essa integração automaticamente.
- Validar vazio, unitário, aleatórios, ordenados, reversos e repetidos.
- Incluir negativos, misturas de inteiros e floats, valores equivalentes, rejeição de NaN/infinito e B inválido.
- Incluir limites de blocos, um piso por bloco, buracos internos, grupos distantes, muitos decimais no mesmo piso e capacidades diferentes.
- Verificar ordem, multiplicidades e preservação da entrada.
- Explorar tamanhos crescentes, incluindo 10, 100, 1.000 e 10.000, conforme viabilidade.
- Comparar com pelo menos dois clássicos exigidos, ainda a escolher, e também com dicionário seguido de ordenação das chaves para isolar o efeito dos blocos.
- Comparar a alocação ajustada com a versão de vetores completos para avaliar a mudança de extremos.
- Usar as mesmas entradas entre métodos, repetições estatísticas e registrar ambiente, capacidade, tempo e operações. Medir posições alocadas ajuda a avaliar a motivação, embora não substitua as métricas exigidas.

Na entrega:

- Escolher relatório Markdown/PDF ou slides; acompanhar com código e testes executáveis.
- Incluir concepção, exemplo, pseudocódigo, invariantes, análise temporal e espacial, estabilidade, in-place, tabelas/gráficos, comparação com a literatura e limitações.
- Preparar a declaração detalhada de autoria e IA.
- Saber explicar cada decisão. O enunciado exige apresentação oral de pelo menos um dos três TPs do semestre; isso não significa que necessariamente será este TP.

## 15. Registro provisório de uso de IA

O aluno apresentou e desenvolveu a ideia inicial de indexação, contagem, blocos e tratamento local dos decimais, discutindo e escolhendo alternativas durante a conversa. Houve assistência de IA nesta interface para revisão do enunciado e dos arquivos, pesquisa de antecedentes, análise preliminar, revisão e redação do pseudocódigo e consolidação deste documento. Também foram sugeridas alternativas, incluindo o ajuste dos vetores pelos extremos locais, posteriormente aceito pelo aluno.

Esta redação e a substituição do pseudocódigo foram feitas com assistência de IA e precisam constar na declaração final. Até este registro, não houve implementação nem validação experimental do novo algoritmo. A validação conceitual consistiu em revisão do fluxo, exemplos e argumentos preliminares; isso não substitui testes ou prova formal completa.

A declaração final deve informar a ferramenta utilizada, por que e como foi usada, o que o aluno modificou e como validou os resultados, sem inventar atividades ainda não realizadas.
