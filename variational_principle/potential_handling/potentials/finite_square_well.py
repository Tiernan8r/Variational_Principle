import numpy as np
from variational_principle.potential_handling.potentials.square_well import square_well

display_name = "Finite Square Well"


def finite_square_well(r: np.ndarray):
    return square_well(r, 10, perturbed=False)
