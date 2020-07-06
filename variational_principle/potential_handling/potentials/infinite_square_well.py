import numpy as np
from variational_principle.potential_handling.potentials.square_well import square_well


def infinite_square_well(r: np.ndarray):
    return square_well(r, np.inf, perturbed=False)
