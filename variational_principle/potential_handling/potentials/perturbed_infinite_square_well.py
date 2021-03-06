import numpy as np
from variational_principle.potential_handling.potentials.square_well import square_well

display_name = "Perturbed Infinite Square Well"


def perturbed_infinite_square_well(r: np.ndarray):
    return square_well(r, np.inf, perturbed=True, perturbation=0.5)
