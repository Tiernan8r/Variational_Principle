import numpy as np

display_name = "Central Potential"


def central_potential(r: np.ndarray, A=-10, B=1.5, C=8):
    V_c = A * C * r ** -1
    V_f = B * C ** 2 * r ** -2

    V = V_c + V_f
    # V = np.sum(V, axis=0)

    return V
