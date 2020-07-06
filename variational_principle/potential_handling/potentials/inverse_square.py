import numpy as np
from variational_principle.potential_handling.potentials.inverse import inverse

display_name = "Squared Inverse Potential"


def inverse_square(r: np.ndarray):
    return inverse(r) ** 2
