import numpy as np
import calculus.laplacian as lap

# global constants:
hbar = 6.5821189 * 10 ** -16  # 6.582119569x10^-16 eV (from wikipedia)
# electron
m = 9.1093819 * 10 ** -31  # 9.1093837015(28)x10^-31
# factor used in calculation of energy
factor = -(hbar ** 2) / (2 * m)


def normalise(psi: np.ndarray, dr: float) -> np.ndarray:
    """
    The function takes in a non-normalised psi wavefunction, and returns the normalised version of it.
    :param psi: The wavefunction to normalise.
    :param dr: The grid spacing of the wavefunction.
    :return: The normalised wavefunction
    """
    # integrate using the rectangular rule
    norm = (psi * psi).sum() * dr
    # Since psi is displayed as |psi|^2, take the sqrt of the norm
    norm_psi = psi / np.sqrt(norm)
    return norm_psi


def energy(psi: np.ndarray, V: np.ndarray, dr: float) -> float:
    """
    Calculates the energy eigenvalue of a given wavefunction psi in a given potential system V.
    :param psi: The wavefunction in the system.
    :param V: The potential function of the system.
    :param dr: The grid spacing in the system.
    :return: The energy eigenvalue E.
    """
    # The laplacian derivative matrix
    DEV2 = lap.get_laplacian()

    # when V is inf, wil get an invalid value error at runtime, not an issue, is sorted in filtering below:
    Vp = V * psi
    # filter out nan values in Vp
    Vp = np.where(np.isfinite(Vp), Vp, 0)

    # Calculate the kinetic energy of the system
    # DEV2 is the laplacian 2nd derivative matrix.
    Tp = factor * (DEV2 @ psi)

    # Return the integral of the KE and PE applied to psi, which is the energy.
    return (psi * (Tp + Vp)).sum() * dr

