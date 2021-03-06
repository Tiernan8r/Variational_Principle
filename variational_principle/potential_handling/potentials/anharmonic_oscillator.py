import numpy as np

display_name = "Anharmonic Oscillator"


def anharmonic_oscillator(r: np.ndarray):
    V = r + 0.5 * r ** 2 + 0.25 * r ** 4
    return V
