import numpy as np

# Funcao esferica


def esfera(x):
    return np.sum(x**2)


# Funcao Ackley


def ackley(x):
    n = len(x)
    return (
        -20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / n))
        - np.exp(np.mean(np.cos(2 * np.pi * x)))
        + 20
        + np.e
    )


# Funcao Rastrigin


def rastrigin(x):
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))
