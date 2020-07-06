import numpy as np

display_name = "Delta Barrier Potential"


def delta_barrier(r: np.ndarray):
    V = np.zeros(r.shape)
    sub_V = V
    while True:
        sub_sub_V = sub_V[0]
        if not type(sub_sub_V) is np.ndarray:
            L = len(sub_V)
            sub_V[L // 2] = -np.inf
            break
        else:
            sub_V = sub_sub_V

    return V
