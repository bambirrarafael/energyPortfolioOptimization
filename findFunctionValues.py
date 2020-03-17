import numpy as np


def find_function_values(solutions):
    aux = np.zeros([len(solutions), 4])
    k = 0
    for i in solutions:
        for j in range(4):
            aux[k, j] = solutions[i][j]
        k += 1
    fmax = aux.max(axis=0)
    fmin = aux.min(axis=0)
    return [fmax, fmin]
