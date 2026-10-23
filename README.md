# TP02 — Differential Evolution (DE/rand/1/Bin) com Restrições

Trabalho Prático 2 da disciplina de **Computação Evolucionária** (UFOP).

Implementação, em Python, do algoritmo **Differential Evolution** com estratégia `DE/rand/1/Bin`, escrito do zero (sem usar DE pronto), aplicado a três funções clássicas de otimização contínua **com restrições**, tratadas por **penalização**. O objetivo é entender o funcionamento do algoritmo, a influência de seus parâmetros e o efeito da penalização, e não obter o melhor desempenho possível.

## Problemas

| Função | Domínio de cada variável | g1 | g2 |
|---|---|---|---|
| Esfera | [-5.12, 5.12] | Σx − 5 ≤ 0 | Σx² − 25 ≤ 0 |
| Ackley | [-32.768, 32.768] | Σx − 5 ≤ 0 | Σx² − 50 ≤ 0 |
| Rastrigin | [-5.12, 5.12] | Σx − 5 ≤ 0 | Σcos(x) − 1 ≤ 0 |

Dimensões: **n = 2, 5 e 10**.

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

Execute a partir da **raiz do projeto**: o `main.py` cria a pasta `resultados/` no diretório atual. Essa pasta **não é enviada ao GitHub** (está no `.gitignore`); ela é gerada localmente a cada execução, cuja duração depende da máquina (são 14 configurações × 10 execuções; no ambiente em que os resultados abaixo foram obtidos, cerca de 0,8 s por execução). Ao final são gerados:

- `resultados/resumo.csv`: estatísticas por configuração;
- `resultados/execucoes.csv`: resultado de cada execução (inclui a semente e o vetor da melhor solução viável);
- `resultados/convergencia_<funcao>.png`, `experimento_parametro_ackley.png` e `estudo_rho.png`.

## Implementação

| Componente | Função | Descrição |
|---|---|---|
| População inicial | `inicializar_populacao` | Amostragem uniforme dentro dos limites da função |
| Avaliação | `avaliar` | Retorna o valor penalizado, o `f(x)` original (somente se viável) e a flag de viabilidade |
| Penalização | `valor_penalizado` | `F_pen(x) = f(x) + ρ · Σⱼ [max(0, gⱼ(x))]²` |
| Mutação | `mutacao` | `DE/rand/1`: `v = x_r1 + F · (x_r2 − x_r3)`, com r1, r2, r3 distintos entre si e diferentes do alvo |
| Crossover | `crossover_binomial` | Binomial, com ao menos uma componente herdada do mutante |
| Laço principal | `de_rand_1_bin` | Seleção target × trial comparando `F_pen` |

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

Todas as configurações encontraram solução viável nas 10 execuções (**taxa de sucesso = 100%**). A média e o desvio padrão (ddof = 1) usam as 10 execuções viáveis. A última coluna é a fração média de indivíduos viáveis na população inicial.

| Função | n | NP | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) | Viáveis na pop. inicial |
|---|---|---|---|---|---|---|---|
| Esfera | 2 | 20 | 1.772e-225 | 7.003e-217 ± 0 | 10/10 | 0.68 | 69.0% |
| Esfera | 5 | 50 | 5.155e-37 | 9.391e-35 ± 1.500e-34 | 10/10 | 0.66 | 13.6% |
| Esfera | 10 | 100 | 1.162e-07 | 5.440e-07 ± 6.213e-07 | 10/10 | 0.63 | 0.1% |
| Ackley | 2 | 20 | 4.441e-16 | 4.441e-16 ± 0 | 10/10 | 0.82 | 2.0% |
| Ackley | 5 | 50 | 4.441e-16 | 1.155e-15 ± 1.498e-15 | 10/10 | 0.85 | 0.0% |
| Ackley | 10 | 100 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.81 | 0.0% |
| Rastrigin | 2 | 20 | 3.0997 | 3.3039 ± 0.2078 | 10/10 | 0.76 | 78.0% |
| Rastrigin | 5 | 50 | 10.9447 | 12.8677 ± 1.2322 | 10/10 | 0.75 | 67.0% |
| Rastrigin | 10 | 100 | 44.0735 | 56.9453 ± 7.8705 | 10/10 | 0.74 | 63.3% |

O NFE médio é 20.000 em todas as configurações. Os tempos são específicos da máquina em que os experimentos foram executados e variam conforme o hardware e as versões das bibliotecas; o NFE, por outro lado, não depende da máquina. Os vetores das melhores soluções viáveis ficam em `resultados/resumo.csv`, gerado na execução.

### Efeito de F (Ackley, n = 10)

| F | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) |
|---|---|---|---|---|
| 0.5 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.81 |
| 0.9 | 5.1689 | 7.0712 ± 1.0095 | 10/10 | 0.74 |

### Efeito de ρ (Ackley, n = 10)

| ρ | Melhor f(x) viável | Média ± desvio | Exec. viáveis | Tempo médio (s) |
|---|---|---|---|---|
| 1 | 4.400e-03 | 6.073e-03 ± 1.518e-03 | 10/10 | 0.85 |
| 100 | 3.868e-03 | 5.646e-03 ± 1.334e-03 | 10/10 | 0.84 |
| 10⁴ | 3.958e-03 | 6.022e-03 ± 1.150e-03 | 10/10 | 0.85 |

### Gráficos de convergência

Os gráficos de convergência do melhor valor **penalizado** versus NFE (escala logarítmica; linhas finas = execuções, linha grossa = mediana) são gerados em `resultados/` ao rodar o programa: `convergencia_esfera.png`, `convergencia_ackley.png`, `convergencia_rastrigin.png`, `experimento_parametro_ackley.png` e `estudo_rho.png`. As sementes fixas tornam os resultados reproduzíveis.

## Observações

- Na Esfera e na Ackley o ótimo irrestrito (origem) é viável, então as restrições pouco atrapalham a convergência. Na Rastrigin, g2 = Σcos(x) − 1 ≤ 0 deixa a origem inviável (g2 = n − 1 > 0 para n ≥ 2), o que explica os valores finais bem maiores.
- A fração de viáveis na população inicial cai com a dimensão (Esfera) ou já parte de quase zero (Ackley), mas o DE encontrou soluções viáveis em todas as execuções.
- Em Ackley n = 10, o aumento de F de 0.5 para 0.9 piorou muito o resultado final no orçamento de 20.000 NFE. A discussão completa está no relatório.
