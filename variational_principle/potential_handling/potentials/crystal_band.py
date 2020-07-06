import numpy as np


def crystal_band(r: np.ndarray):
    N = r.shape[1]
    D = r.shape[0]

    num_bands = 5
    band_spacing = N // (2 * num_bands)
    V_0 = 10

    x_band = np.linspace(V_0, V_0, N)
    # for i in range(1, 2 * num_bands, 2):
    i = 0
    j = -1
    for k in range(N):
        i %= band_spacing
        j %= 2
        if j == 0:
            x_band[k] = 0
        if i == 0:
            j += 1
        i += 1

    # for i in range(num_bands + 2):
    #     start_index = band_spacing * i * 2
    #     for j in range(band_spacing):
    #         x_band[start_index + j] = 0

    wells = [x_band] * D
    V = np.array(np.meshgrid(*wells, indexing="ij"))

    # Correction of Corners:
    V = np.sum(V, axis=0)
    V = V.reshape(N ** D)
    for i in range(len(V)):
        if V[i] > 0:
            V[i] = V_0
    V = V.reshape([N] * D)

    return V
