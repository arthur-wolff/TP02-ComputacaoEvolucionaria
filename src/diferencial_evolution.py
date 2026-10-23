import numpy as np
import time


import funcoes_teste as ft

# Dominio das funcoes teste
DOMINIO = {
    "esfera": (-5.12, 5.12),
    "ackley": (-32.768, 32.768),
    "rastrigin": (-5.12, 5.12),
}

FUNCOES = {"esfera": ft.esfera, "ackley": ft.ackley, "rastrigin": ft.rastrigin}

TOL = 1e-6


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


# Populacao inicial


def inicializar_populacao(NP, n, lb, ub, rng):

    r = rng.random((NP, n))
    pop = lb + r * (ub - lb)
    return pop


# Fitness


def avaliar(x, funcao: str, rho: float):
    f_pen = valor_penalizado(x, funcao, rho)
    viavel = bool(np.all(restricoes(x, funcao) <= TOL))
    f = FUNCOES[funcao](x) if viavel else np.nan

    return f_pen, f, viavel


# Mutacao


def mutacao(pop, i, F, lb, ub, rng):
    NP = len(pop)
    idx = rng.choice(NP - 1, size=3, replace=False)
    idx[idx >= i] += 1
    r1, r2, r3 = idx
    v = pop[r1] + F * (pop[r2] - pop[r3])
    return np.clip(v, lb, ub)


# Crossover binomial


def crossover_binomial(x_i, v_i, CR, rng):
    n = len(x_i)
    mask = rng.random(n) < CR
    mask[rng.integers(n)] = True
    return np.where(mask, v_i, x_i)


def registrar_his(
    x, f_pen, f, viavel, nfe, melhor_pen, melhor_f_viavel, melhor_x_viavel, hist
):

    if f_pen < melhor_pen:
        melhor_pen = f_pen
    if viavel and f < melhor_f_viavel:
        melhor_f_viavel, melhor_x_viavel = f, x.copy()

    hist[nfe] = melhor_pen  # hist e um array: modificado in-place
    nfe += 1
    return nfe, melhor_pen, melhor_f_viavel, melhor_x_viavel


# Funcao principal do DE


def de_rand_1_bin(funcao, n, NP, F, CR, rho, max_nfe, seed):
    assert NP >= 4
    assert NP <= max_nfe

    lb, ub = DOMINIO[funcao]
    rng = np.random.default_rng(seed)
    t0 = time.perf_counter()

    hist = np.empty(max_nfe)

    nfe = 0
    melhor_pen = np.inf
    melhor_f_viavel = np.inf
    melhor_x_viavel = None

    # População inicial

    pop = inicializar_populacao(NP, n, lb, ub, rng)
    fit = np.empty(NP)
    n_viaveis_ini = 0
    # Fitness
    for i in range(NP):
        fit[i], f, viavel = avaliar(pop[i], funcao, rho)
        n_viaveis_ini += viavel
        nfe, melhor_pen, melhor_f_viavel, melhor_x_viavel = registrar_his(
            pop[i],
            fit[i],
            f,
            viavel,
            nfe,
            melhor_pen,
            melhor_f_viavel,
            melhor_x_viavel,
            hist,
        )

    while nfe < max_nfe:
        nova_pop, nova_fit = pop.copy(), fit.copy()
        for i in range(NP):
            if nfe >= max_nfe:
                break
            # Gera um mutante

            mutante = mutacao(pop, i, F, lb, ub, rng)

            # Gera um trial

            trial = crossover_binomial(pop[i], mutante, CR, rng)

            # avalia o trial
            f_pen, f, viavel = avaliar(trial, funcao, rho)

            nfe, melhor_pen, melhor_f_viavel, melhor_x_viavel = registrar_his(
                trial,
                f_pen,
                f,
                viavel,
                nfe,
                melhor_pen,
                melhor_f_viavel,
                melhor_x_viavel,
                hist,
            )
            if f_pen <= fit[i]:
                nova_pop[i], nova_fit[i] = trial, f_pen

        pop, fit = nova_pop, nova_fit

    return {
        "funcao": funcao,
        "n": n,
        "NP": NP,
        "F": F,
        "CR": CR,
        "rho": rho,
        "seed": seed,
        "nfe": nfe,
        "tempo": time.perf_counter() - t0,
        "achou_viavel": melhor_x_viavel is not None,
        "melhor_f_viavel": melhor_f_viavel if melhor_x_viavel is not None else np.nan,
        "melhor_x_viavel": melhor_x_viavel,
        "melhor_pen_final": melhor_pen,
        "frac_viavel_ini": n_viaveis_ini / NP,
        "hist": hist,
    }
