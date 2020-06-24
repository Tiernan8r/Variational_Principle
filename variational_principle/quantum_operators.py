import numpy as np
import calculus.laplacian as lap
import scipy.integrate as intg

import logging

##TODO change these global variables implementation
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

    logger = logging.getLogger(__name__)
    logger.info("Normalising energy eigenstate")

    # integrate using the rectangular rule
    psi_sq = psi * psi
    # norm = psi_sq.sum() * dr

    logger.debug("Performing integration")
    norm = intg.trapz(psi_sq, dx=dr)
    # norm = intg.simps(psi_sq, dx=dr)
    # Since psi is displayed as |psi|^2, take the sqrt of the norm
    norm_psi = psi / np.sqrt(norm)
    logger.debug("Energy eigenstate normalised.")
    return norm_psi


def energy(psi: np.ndarray, V: np.ndarray, dr: float) -> float:
    """
    Calculates the energy eigenvalue of a given wavefunction psi in a given potential system V.
    :param psi: The wavefunction in the system.
    :param V: The potential function of the system.
    :param dr: The grid spacing in the system.
    :return: The energy eigenvalue E.
    """

    logger = logging.getLogger(__name__)
    logger.info("Calculating energy eigenvalue for energy eigenstate.")

    # The laplacian derivative matrix
    DEV2 = lap.get_laplacian()
    logger.debug("Retrieved Laplacian operator.")

    # when V is inf, wil get an invalid value error at runtime, not an issue, is sorted in filtering below:
    Vp = V * psi
    # filter out nan values in Vp
    Vp = np.where(np.isfinite(Vp), Vp, 0)
    logger.debug("Performed potential operation and filtered out Nan values.")

    # Calculate the kinetic energy of the system
    # DEV2 is the laplacian 2nd derivative matrix.
    Tp = factor * (DEV2 @ psi)
    logger.debug("Performed kinetic operation.")

    # Return the integral of the KE and PE applied to psi, which is the energy.
    H = psi * (Tp + Vp)
    # return H.sum() * dr
    I = intg.trapz(H, dx=dr)
    logger.debug("Completed integration of Hamiltonian.")
    return I
    # return intg.simps(H, dx=dr)

