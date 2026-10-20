import numpy as np
import time


from src import funcoes_teste as ft

# Dominio das funcoes teste
DOMINIO = {
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
    f = {"esfera": ft.esfera, "ackley": ft.ackley,
         "rastrigin": ft.rastrigin}[funcao](x)
    g = restricoes(x, funcao)
    return f + rho * np.sum(np.maximum(0, g) ** 2)

# Populacao inicial


def inicializar_populacao(NP, n, lb, ub, rng):

    r = rng.random((NP, n))
    pop = lb + r * (ub - lb)
    return pop

# Fitness


def fitness(pop, funcao, rho, nfe):
    fit = np.zeros(len(pop))
    for i in range(len(pop)):
        fit[i] = valor_penalizado(pop[i], funcao, rho)
        nfe += 1
    return fit, nfe

# Mutacao


def mutacao(pop, i, F, lb, ub, rng):
    NP = len(pop)
    indices = list(range(NP))
    indices.remove(i)
    r1, r2, r3 = rng.choice(indices, size=3, replace=False)
    x_r1, x_r2, x_r3 = pop[r1], pop[r2], pop[r3]
    v_i = x_r1 + F * (x_r2 - x_r3)
    v_i = np.clip(v_i, lb, ub)  # tratamento de limites
    return v_i

# Crossover binomial


def crossover_binomial(x_i, v_i, CR, rng):
    n = len(x_i)
    j_rand = rng.integers(0, n)
    u_i = np.empty(n)
    for j in range(n):
        if rng.random() < CR or j == j_rand:
            u_i[j] = v_i[j]
        else:
            u_i[j] = x_i[j]
    return u_i


# Funcao principal do DE


def de_rand_1_bin(funcao, n, lb, ub, NP, F, CR, rho, max_nfe, seed):
    rng = np.random.default_rng(seed)
    nfe = 0
    historico = []  # (nfe, melhor valor penalizado)

    # População inicial

    pop = inicializar_populacao(NP, n, lb, ub, rng)

    # Fitness

    fit, nfe = fitness(pop, funcao, rho, nfe)

    while nfe < max_nfe:
        for i in range(NP):
            if nfe >= max_nfe:
                break
            # Gera um mutante

            mutante = mutacao(pop, i, F, lb, ub, rng)

            # Gera um trial

            trial = crossover_binomial(pop[i], mutante, CR, rng)

            # avalia o trial

            fit_trial = valor_penalizado(trial, funcao, rho)

            # substitui o individuo se o trial for melhor

            if fit_trial < fit[i]:
                pop[i] = trial
                fit[i] = fit_trial
            else:
                pop[i] = pop[i]
                fit[i] = fit[i]
            nfe += 1

        # registrar histórico
        historico.append((nfe, np.min(fit)))
    return
