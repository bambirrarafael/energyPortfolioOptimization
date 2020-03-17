import numpy as np


def normalize_solution(solutions):
    aux = np.zeros([len(solutions), 4])
    normalized_solutions = np.zeros([len(solutions), 4])
    k = 0
    for i in solutions:
        for j in range(4):
            aux[k, j] = solutions[i][j]
        k += 1
    for i in range(len(solutions)):
        for j in range(4):
            normalized_solutions[i, j] = (aux.max(axis=0)[j] - aux[i, j]) / (aux.max(axis=0)[j] - aux.min(axis=0)[j])
    return normalized_solutions
