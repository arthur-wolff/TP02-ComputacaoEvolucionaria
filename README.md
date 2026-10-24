# TP02 — Differential Evolution (DE/rand/1/Bin) com Restrições

Trabalho Prático 2 da disciplina de **Computação Evolucionária** (UFOP).

Implementação, em Python, do algoritmo **Differential Evolution** com estratégia `DE/rand/1/Bin`, escrito do zero (sem usar DE pronto), aplicado a três funções clássicas de otimização contínua **com restrições**, tratadas por **penalização**. O objetivo é entender o funcionamento do algoritmo, a influência de seus parâmetros e o efeito da penalização, e não obter o melhor desempenho possível.

## Problemas

Nas três funções o ótimo global é a origem, com f(x*) = 0, e a origem é viável.

| Função | Domínio de cada variável | g1 | g2 |
|---|---|---|---|
| Esfera | [-5.12, 5.12] | Σx − 5 ≤ 0 | Σx² − 25 ≤ 0 |
| Ackley | [-32.768, 32.768] | Σx − 5 ≤ 0 | Σx² − 50 ≤ 0 |
| Rastrigin | [-5.12, 5.12] | Σx − 5 ≤ 0 | Σx² − 25 ≤ 0 |

Dimensões: **n = 2, 5 e 10**.

> A restrição g2 da Rastrigin segue a tabela de problemas do enunciado (Σx² − 25). O código de exemplo do enunciado usa Σcos(x) − 1, que não corresponde à tabela e não deve ser usado.

## Estrutura do repositório

```
.
├── src/
│   ├── funcoes_teste.py          # esfera, Ackley e Rastrigin
│   ├── diferencial_evolution.py  # restrições, penalização, operadores e laço do DE
│   └── main.py                   # experimentos, estatísticas, CSVs e gráficos
├── tests/                        # scripts de verificação da população e da penalização
├── resultados/                   # gerada ao executar o main.py (não versionada, ver .gitignore)
├── requirements.txt
└── README.md
```

## Como executar

Requisitos: Python 3.9+ (numpy, pandas e matplotlib).

```bash
pip install -r requirements.txt
python src/main.py
```

Execute a partir da **raiz do projeto**: o `main.py` cria a pasta `resultados/` no diretório atual. Essa pasta **não é enviada ao GitHub** (está no `.gitignore`); ela é gerada localmente a cada execução, cuja duração depende da máquina (são 14 configurações × 10 execuções; no ambiente em que os resultados abaixo foram obtidos, de 0,6 a 1,0 s por execução). Ao final são gerados:

- `resultados/resumo.csv`: estatísticas por configuração (inclui o NFE até a primeira solução viável);
- `resultados/execucoes.csv`: resultado de cada execução (inclui a semente, o NFE até a primeira solução viável e o vetor da melhor solução viável);
- `resultados/convergencia_<funcao>.png`, `experimento_parametro_ackley.png` e `estudo_rho.png`.

## Implementação

| Componente | Função | Descrição |
|---|---|---|
| População inicial | `inicializar_populacao` | Amostragem uniforme dentro dos limites da função |
| Avaliação | `avaliar` | Retorna o valor penalizado, o `f(x)` original (somente se viável) e a flag de viabilidade |
| Penalização | `valor_penalizado` | `F_pen(x) = f(x) + ρ · Σⱼ [max(0, gⱼ(x))]²` |
| Mutação | `mutacao` | `DE/rand/1`: `v = x_r1 + F · (x_r2 − x_r3)`, com r1, r2, r3 distintos entre si e diferentes do alvo |
| Crossover | `crossover_binomial` | Binomial, com ao menos uma componente herdada do mutante |
| Laço principal | `de_rand_1_bin` | Seleção target × trial comparando `F_pen`; registra o NFE da primeira solução viável |

### Decisões de implementação

- **Limites de caixa:** tratados por **projeção** (`np.clip`) do mutante ao intervalo da função.
- **Restrições:** as violações são calculadas para qualquer solução, mesmo fora da região viável. O trial substitui o alvo se `F_pen(trial) <= F_pen(alvo)`.
- **Viabilidade:** uma solução é viável se g1 ≤ 1e-6 e g2 ≤ 1e-6 (tolerância `TOL`).
- **Seleção síncrona:** os trials são comparados com a população da geração atual e a nova população só substitui a anterior ao final da geração.
- **Critério de parada:** NFE = 20.000 por execução, contando a inicialização e candidatos viáveis e inviáveis. O laço interrompe assim que o orçamento acaba, inclusive no meio de uma geração.
- **Resultados viáveis:** o `f(x)` original só é guardado para soluções viáveis. Valores penalizados nunca são reportados como valores objetivos. O gráfico de convergência mostra explicitamente o valor **penalizado**.

## Configuração experimental

| Parâmetro | Valor |
|---|---|
| NP | `max(10·n, 20)`: 20 (n=2), 50 (n=5), 100 (n=10) |
| F | 0.5 |
| CR | 0.9 |
| ρ | 100 (fixo em todas as funções) |
| NFE máximo | 20.000 por execução |
| Execuções | 10 independentes por configuração |
| Sementes | 101, 202, 303, 404, 505, 606, 707, 808, 909, 1010 |

### Experimentos adicionais (Ackley, n = 10)

- **Efeito do parâmetro:** apenas **F** varia, de 0.5 para 0.9. As sementes, o NFE, NP, CR e ρ são os mesmos.
- **Estudo de ρ:** ρ ∈ {1, 100, 10⁴}, com os demais parâmetros fixos.

## Resultados

Todas as configurações encontraram solução viável nas 10 execuções (**taxa de sucesso = 100%**). A média e o desvio padrão (ddof = 1) usam as 10 execuções viáveis. "Viáveis ini." é a fração média de indivíduos viáveis na população inicial e "NFE 1ª viável" é a mediana do NFE até a primeira solução viável (inclui a inicialização).

| Função | n | NP | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) | Viáveis ini. | NFE 1ª viável |
|---|---|---|---|---|---|---|---|---|
| Esfera | 2 | 20 | 1.772e-225 | 7.003e-217 ± 2.214e-216* | 10/10 | 0.73 | 69.0% | 1 |
| Esfera | 5 | 50 | 5.155e-37 | 9.391e-35 ± 1.500e-34 | 10/10 | 0.68 | 13.6% | 3.5 |
| Esfera | 10 | 100 | 1.162e-07 | 5.440e-07 ± 6.213e-07 | 10/10 | 0.74 | 0.1% | 343 |
| Ackley | 2 | 20 | 4.441e-16 | 4.441e-16 ± 0 | 10/10 | 1.01 | 2.0% | 26.5 |
| Ackley | 5 | 50 | 4.441e-16 | 1.155e-15 ± 1.498e-15 | 10/10 | 0.89 | 0.0% | 565 |
| Ackley | 10 | 100 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.91 | 0.0% | 3605 |
| Rastrigin | 2 | 20 | 0 | 0 ± 0 | 10/10 | 0.78 | 69.0% | 1 |
| Rastrigin | 5 | 50 | 4.476e-13 | 0.1073 ± 0.3252 | 10/10 | 0.82 | 13.6% | 3.5 |
| Rastrigin | 10 | 100 | 23.1684 | 30.5114 ± 4.2642 | 10/10 | 0.74 | 0.1% | 343 |

\* O desvio da Esfera n = 2 foi calculado em precisão estendida: em `float64` ele sofre *underflow* e sai 0 (valores da ordem de 1e-217 elevados ao quadrado ficam abaixo do menor número positivo do tipo). O desvio é maior que a média porque uma única execução (semente 606, 7.0e-216) domina.

O NFE médio é 20.000 em todas as configurações. Os tempos são específicos da máquina e da carga em que os experimentos foram executados; o NFE, por outro lado, não depende da máquina. Na Rastrigin n = 2, o valor 0 é numérico: soluções com |xᵢ| ~ 1e-9 têm f real da ordem de 1e-16, mas cos(2πxᵢ) arredonda para 1 em ponto flutuante. Os vetores das melhores soluções viáveis ficam em `resultados/resumo.csv`.

### Efeito de F (Ackley, n = 10)

| F | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) | NFE 1ª viável |
|---|---|---|---|---|---|
| 0.5 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.91 | 3605 |
| 0.9 | 5.1689 | 7.0712 ± 1.0095 | 10/10 | 0.75 | 16561 |

Com F = 0.9 a primeira solução viável só aparece entre ~13.900 e ~19.400 NFE (contra ~3.400 a ~4.000 com F = 0.5), sobrando poucas gerações para refinar f. A causa do atraso (passos maiores) é uma hipótese, pois a diversidade da população não foi medida.

### Efeito de ρ (Ackley, n = 10)

| ρ | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) | NFE 1ª viável |
|---|---|---|---|---|---|
| 1 | 4.400e-03 | 6.073e-03 ± 1.518e-03 | 10/10 | 0.88 | 3605 |
| 100 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.85 | 3605 |
| 10⁴ | 3.958e-03 | 6.022e-03 ± 1.150e-03 | 10/10 | 0.85 | 3605 |

### Gráficos de convergência

Os gráficos de convergência do melhor valor **penalizado** versus NFE (escala logarítmica; linhas finas = execuções, linha grossa = mediana; valores abaixo de 1e-12 são limitados a 1e-12 apenas no gráfico) são gerados em `resultados/` ao rodar o programa: `convergencia_esfera.png`, `convergencia_ackley.png`, `convergencia_rastrigin.png`, `experimento_parametro_ackley.png` e `estudo_rho.png`. As sementes fixas tornam os resultados reproduzíveis.

## Observações

- Nas três funções a origem é o ótimo global e é viável, então as restrições não são ativas no ótimo: elas apenas delimitam a região viável, e o desafio está em chegar a ela.
- A fração de viáveis na população inicial cai com a dimensão (Esfera e Rastrigin: 69,0%, 13,6% e 0,1%, idênticas porque usam a mesma bola de raio 5, o mesmo cubo e as mesmas sementes) ou já parte de quase zero (Ackley), mas o DE encontrou soluções viáveis em todas as execuções. Na Ackley n = 10 a primeira solução viável surge em ~3.600 NFE (cerca de 18% do orçamento).
- O DE só compara alvo e trial, então ρ altera a escala dos valores penalizados, mas pouco a ordem enquanto a violação domina: o NFE até a primeira viável tem a mesma distribuição para ρ = 1, 100 e 10⁴.
- Na Rastrigin n = 10 a curva estagna em ~30 (mínimos locais); em n = 5 duas execuções (sementes 303 e 404) terminam bem acima das demais.
- Em Ackley n = 10, o aumento de F de 0.5 para 0.9 piorou muito o resultado final no orçamento de 20.000 NFE. A discussão completa está no relatório.
