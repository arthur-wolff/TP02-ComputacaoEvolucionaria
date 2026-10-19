import numpy as np
from src import funcoes_teste as ft
from src.diferencial_evolution import valor_penalizado, restricoes

NP, n, rho = 10, 2, 1000
lb, ub = -5.12, 5.12
rng = np.random.default_rng(0)
nfe = 0

pop = lb + rng.random((NP, n)) * (ub - lb)
fit = np.zeros(NP)


for i in range(len(pop)):
    fit[i] = valor_penalizado(pop[i], "esfera", rho)
    nfe += 1

print(fit.shape, nfe)  # esperado: (10,) 10
print(fit[0], valor_penalizado(pop[0], "esfera", rho))  # devem ser iguais
