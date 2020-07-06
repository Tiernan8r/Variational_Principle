import numpy as np


def square_well(r: np.ndarray, V_0=10, well_fraction=3, perturbed=False, perturbation=0.5):
    N = r.shape[1]
    D = r.shape[0]

    third = N // well_fraction

    addition = int(abs((third - (N / well_fraction))) * well_fraction)

    mid, bef = np.zeros(third + addition), np.linspace(V_0, V_0, third)
    aft = bef.copy()
    x_well = np.concatenate((bef, mid, aft))
    wells = [x_well] * D
    V = np.array(np.meshgrid(*wells, indexing="ij"))

    # Correction of Corners:
    V = V.reshape(N ** D)

    if perturbed:
        # Perturbation
        R = r.reshape(N ** D)
    for i in range(len(V)):
        if V[i] > 0:
            V[i] = V_0
        if perturbed:
            # Perturbation
            if V[i] == 0:
                V[i] += perturbation * R[i]

    shape = [D] + [N] * D
    V = V.reshape(shape)

    return V
