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
        return potential(r, default_potential_name)

    foo = getattr(module, potential_name)
    V = foo(r)
    if V is None and potential_name != default_potential_name:
        return potential(r, default_potential_name)
    elif V is None and potential_name == default_potential_name:
        logger.warning("V is None, even from default!")
        raise ValueError("Potential evaluating to None from potential file '{}.py'.".format(potential_name))

    return V.sum(axis=0)


def potentials_directory_path():
    current_path = __file__
    parent_path = os.path.dirname(current_path)
    potential_directory = "potentials"
    potentials_path = os.path.join(parent_path, potential_directory)
    return potentials_path


def full_potential_path(potential_name: str):
    directory_path = potentials_directory_path()
    path = os.path.join(directory_path, potential_name + ".py")
    return path


def list_potentials():
    potentials_path = potentials_directory_path()

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
