import numpy as np
import time


from src import funcoes_teste as ft

LIMITES = {
    "esfera": (-5.12, 5.12),
    "ackley": (-32.768, 32.768),
    "rastrigin": (-5.12, 5.12),
}


# Restricoes
def restricoes(x, funcao: str):
    g1 = np.sum(x) - 5
    if funcao == "esfera":
        g2 = np.sum(x**2) - 25
    elif funcao == "ackley":
        g2 = np.sum(x**2) - 50
    elif funcao == "rastrigin":
        g2 = np.sum(np.cos(x)) - 1
    else:
        raise ValueError("Função desconhecida")
    return np.array([g1, g2])


# Penalizacoes
def valor_penalizado(x, funcao, rho):
    f = {"esfera": ft.esfera, "ackley": ft.ackley, "rastrigin": ft.rastrigin}[funcao](x)
    g = restricoes(x, funcao)
    return f + rho * np.sum(np.maximum(0, g) ** 2)


def de_rand_1_bin(funcao, n, lb, ub, NP, F, CR, rho, max_nfe, seed):
    rng = np.random.default_rng(seed)
    nfe = 0
    historico = []  # (nfe, melhor valor penalizado)

    # 1. população inicial
    pop = ...  # TODO: shape (NP, n), dentro de [lb, ub]
    fit = ...  # TODO: valor_penalizado de cada indivíduo (conta NFE!)

    while nfe < max_nfe:
        for i in range(NP):
            if nfe >= max_nfe:
                break
            # 2. mutação DE/rand/1
            # 3. tratamento de limites
            # 4. crossover binomial
            # 5. avaliação do trial (nfe += 1) e seleção target x trial
            ...
        # registrar histórico

    # 6. pós-processamento: melhor solução VIÁVEL (usando f original e g)
    return ...
