# Checklist de validação após implementar o núcleo do algoritmo

Este documento reúne os cuidados que devem ser adicionados ou verificados depois que a primeira versão do algoritmo estiver funcionando. A estratégia atual é implementar primeiro o fluxo principal e, em seguida, acrescentar validações, casos de borda e instrumentação.

## 1. Contrato esperado

- Receber uma lista de números e uma capacidade de bloco `B`, com padrão 100.
- Aceitar inteiros e floats finitos, incluindo valores negativos.
- Tratar valores numericamente iguais, como `2` e `2.0`, como a mesma chave.
- Tratar `0.0` e `-0.0` como o mesmo valor.
- Rejeitar `NaN`, infinito positivo e infinito negativo.
- Retornar uma nova lista em ordem crescente.
- Não modificar a lista recebida.
- Na versão instrumentada, retornar `(lista_ordenada, comparacoes, movimentacoes)`.

## 2. Casos obrigatórios do enunciado

- [ ] Entrada vazia: `[]`.
- [ ] Entrada com um elemento: `[42]`.
- [ ] Entrada já ordenada.
- [ ] Entrada em ordem estritamente reversa.
- [ ] Entrada com elementos repetidos.
- [ ] Entrada com todos os elementos iguais.
- [ ] Entradas aleatórias homogêneas.
- [ ] Tamanhos crescentes, como 10, 100, 1.000 e 10.000, conforme a viabilidade.

Para todos esses casos, verificar:

- [ ] A saída é igual a `sorted(entrada)`.
- [ ] A saída tem o mesmo tamanho da entrada.
- [ ] Todas as multiplicidades foram preservadas.
- [ ] A entrada original permaneceu inalterada.

## 3. Casos específicos da proposta

### Números negativos e limites de bloco

- [ ] Apenas números negativos.
- [ ] Mistura de negativos, zero e positivos.
- [ ] Valores próximos de limites de bloco com `B = 100`: `99`, `100`, `199`, `200`.
- [ ] Limites negativos: `-1`, `-100`, `-101`.
- [ ] Confirmar o uso de `floor`, especialmente em valores como `-1.2`, cujo piso é `-2`.

### Decimais

- [ ] Mistura de inteiros e floats.
- [ ] Vários decimais com o mesmo piso: `50.1`, `50.2`, `50.7` e `50.00001`.
- [ ] Decimais negativos com o mesmo piso: `-1.2` e `-1.8`.
- [ ] Valores equivalentes: `2` e `2.0`.
- [ ] Zeros equivalentes: `0`, `0.0` e `-0.0`.
- [ ] Confirmar que os valores completos são emitidos, sem arredondamento.

### Ocupação dos blocos

- [ ] Um valor por bloco: `0`, `100`, `200`, `300`.
- [ ] Vários valores no mesmo bloco.
- [ ] Grupos densos separados por uma distância grande.
- [ ] Valores muito distantes: `1`, `1_000_000`, `1_000_001`.
- [ ] Buracos internos: `200` e `299`.
- [ ] Bloco com apenas um piso, cujo vetor físico deve ter tamanho 1.
- [ ] Confirmar que blocos intermediários sem valores não são criados.
- [ ] Confirmar que o vetor físico cobre apenas do menor ao maior piso presente no bloco.

### Capacidade B

- [ ] Capacidade padrão `B = 100`.
- [ ] Capacidade `B = 1`.
- [ ] Capacidade pequena, como `B = 10`.
- [ ] Capacidade grande, como `B = 1.000`.
- [ ] Confirmar que capacidades diferentes produzem a mesma lista ordenada.

## 4. Entradas que devem ser rejeitadas

Definir e aplicar exceções consistentes:

- `TypeError` para elementos que não pertencem ao domínio numérico aceito.
- `ValueError` para números não finitos e capacidades inválidas.

Verificar:

- [ ] `NaN`.
- [ ] Infinito positivo.
- [ ] Infinito negativo.
- [ ] Texto dentro da lista.
- [ ] `None` dentro da lista.
- [ ] Lista ou outro objeto dentro da entrada.
- [ ] `B = 0`.
- [ ] `B` negativo.
- [ ] `B` float.
- [ ] `B` textual.

### Decisão pendente sobre booleanos

Em Python, `bool` é subtipo de `int`: `True == 1` e `False == 0`. Antes de finalizar a validação, decidir e documentar se booleanos serão aceitos como números ou rejeitados explicitamente. A recomendação atual é rejeitá-los para evitar ambiguidade.

## 5. Casos de robustez adicionais

- [ ] Muitos elementos iguais.
- [ ] Muitos valores distintos no mesmo piso, exercitando o Merge Sort local.
- [ ] Muitos blocos, exercitando o Merge Sort dos IDs.
- [ ] Inteiros muito grandes positivos e negativos.
- [ ] Lista grande com poucos valores distintos.
- [ ] Lista grande com todos os valores distintos.
- [ ] Executar a função mais de uma vez para confirmar que não mantém estado entre chamadas.

## 6. Merge Sort auxiliar

- [ ] Ordenar lista vazia.
- [ ] Ordenar lista unitária.
- [ ] Ordenar IDs negativos e positivos.
- [ ] Ordenar pares pelo valor completo, não pela frequência.
- [ ] Preservar todos os pares durante a intercalação.
- [ ] Somar corretamente as comparações e movimentações feitas em todas as chamadas.

## 7. Instrumentação

Depois que a ordenação estiver correta, definir e aplicar uma regra única para as métricas:

- [ ] Definir o que conta como comparação.
- [ ] Definir o que conta como movimentação.
- [ ] Contabilizar as operações dos Merge Sorts auxiliares.
- [ ] Contabilizar a escrita dos elementos na saída conforme a regra escolhida.
- [ ] Decidir como tratar cópias e criação de listas.
- [ ] Explicar que as operações internas de hashing não são comparações instrumentadas, caso fiquem fora da métrica.
- [ ] Conferir que os contadores nunca sejam negativos e sejam inteiros.

## 8. Integração e reprodução

- [ ] Manter a assinatura compatível com os testes: `my_authorial_sort(arr, block_size=100)` ou equivalente com valor padrão.
- [ ] Integrar a função à suíte principal em `codigo/python/test_suite.py`.
- [ ] Integrar a função ao benchmark em `codigo/python/benchmark.py`.
- [ ] Executar os testes do próprio template.
- [ ] Executar a suíte principal completa.
- [ ] Registrar dependências e instruções de execução.
- [ ] Confirmar que o código funciona a partir de uma cópia limpa do repositório.

## 9. Ordem recomendada para realizar as verificações

1. Fazer o núcleo produzir a saída correta para entradas simples.
2. Verificar vazio, unitário, repetidos, negativos e decimais.
3. Verificar limites e ocupação dos blocos.
4. Acrescentar validação de tipos, números finitos e `B`.
5. Confirmar que a entrada não é modificada.
6. Instrumentar comparações e movimentações.
7. Integrar à suíte e ao benchmark.
8. Executar testes maiores e analisar os resultados.

Não adicionar otimizações antes de a versão básica passar nos testes de corretude. Cada otimização posterior deve repetir esta validação.
