import numpy as np
from variational_principle.potential_handling.potentials.square_well import square_well

display_name = "Perturbed Finite Square Well"


def perturbed_finite_square_well(r: np.ndarray):
    return square_well(r, 10, perturbed=True, perturbation=0.5)
