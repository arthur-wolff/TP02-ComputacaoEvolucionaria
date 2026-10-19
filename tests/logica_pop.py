import numpy as np

rng = np.random.default_rng(0)
r = rng.random((1000, 2))
pop = -5.12 + r * (5.12 - (-5.12))
print(pop.shape, pop.min(), pop.max())
