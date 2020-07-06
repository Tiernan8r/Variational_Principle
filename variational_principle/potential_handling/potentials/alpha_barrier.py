import numpy as np


def alpha_barrier(r: np.ndarray, Z=48):
    e = 1.6021753 * 10 ** -19
    e_0 = 8.854187817 * 10 ** -12
    pi = np.pi

    V = r.copy()
    for i in range(len(r)):
        length = len(r[i])
        third = length // 3

        # # Rc = 1.2 A^1.3 fm
        # Rc = r[i][third]
        # A = (Rc / 1.2) ** (1/1.3) * 10**-15

        # U = -np.array([2.4 * (Z - 2) * A **-(1/3)] * third)
        U = -np.array([0.05] * third)
        U[0] = np.inf

        # inv_r = ((Z - 2) * 2 * e**2) / (4 * pi * e_0 * r[i][third:])
        inv_r = 1 / r[i][third:]

        V[i] = np.concatenate((U, inv_r))

    return V
