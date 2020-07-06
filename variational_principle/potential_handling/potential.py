import numpy as np
import importlib
import logging
import os


def potential(r: np.ndarray, potential_name="harmonic_oscillator") -> np.ndarray:
    """
    The potential energy function of the system
    :param r: The coordinate grid of the system for each axis.
    :param potential_name: The filename of the potential system to import and use.
    :return: The potential function V as a grid of values for each position.
    """
    logger = logging.getLogger(__name__)

    default_potential_name = "harmonic_oscillator"
    all_potentials = list_potentials()
    if potential_name not in all_potentials:
        potential_name = default_potential_name

    path = "variational_principle.potential_handling.potentials."
    try:
        module = importlib.import_module(path + potential_name)
    except ModuleNotFoundError as e:
        logger.warning("Module '%s' not found, defaulting to '%s'." % (potential_name, default_potential_name))
        logger.warning(e)
        return None
        # module = importlib.import_module(path + default_potential_name)
        # potential_name = default_potential_name

    foo = getattr(module, potential_name)
    V = foo(r)

    return V.sum(axis=0)


def list_potentials():
    current_path = __file__
    parent_path = os.path.dirname(current_path)
    potential_directory = "potentials"
    potentials_path = os.path.join(parent_path, potential_directory)

    files = os.scandir(potentials_path)
    potentials = []
    for f in files:
        name = f.name
        if "__" in name:
            continue
        potentials.append(name[:-3])
    return potentials


if __name__ == "__main__":
    list_potentials()
