from scipy.sparse import diags
import numpy as np

import logging


def _partial_derivative_matrix(D: int, N: int, axis_number: int, dr: float) -> np.ndarray:
    """
    Generates the sparse second derivative central difference derivative matrix along given axis, for a grid of dimensions N^D.
    :param D: The number of dimensions of the system, e.g.: 3D...
    :param N: The dimensions of the symmetric grid.
    :param axis_number: The axis to derive along, starting at 0.
    :param dr: The grid spacing in the system.
    :return: The second order central difference derivative sparse matrix along the given axis.
    """

    logger = logging.getLogger(__name__)
    logger.info("Generating a second derivative matrix for %d dimensions of size %d, along axis %d", D, N, axis_number)

    logger.info("Constraining axis number to total number of dimensions")
    # cap axis_number in range to prevent errors.
    axis_number %= D

    # Determine the number of the cell grids that need to be repeated along to populate the matrix
    num_cells = D - (axis_number + 1)

    logger.info("Generating second derivative stencil")
    # The general pattern for a derivative matrix along the axis: axis_number, for a num_axes number of
    # dimensions, each of length N
    diagonals = [[-2] * N ** D,
                 (([1] * N ** axis_number) * (N - 1) + [0] * N ** axis_number) * N ** num_cells,
                 (([1] * N ** axis_number) * (N - 1) + [0] * N ** axis_number) * N ** num_cells]

    logger.info("Generating second derivative diagonal matrix")
    # Create a sparse matrix for the given diagonals, of the desired size.
    D_n = diags(diagonals, [0, -N ** axis_number, N ** axis_number], shape=(N ** D, N ** D))

    logger.info("Scaling by grid spacing")
    # return the matrix, factored by the grid spacing as required by the central difference formula
    return D_n * (dr ** -2)


def generate_laplacian(D: int, N: int, dr: float):
    """
    Generates the Lagrangian second derivative matrix for the number of axes D.
    :param D: The number of dimensions/axes in the system.
    :param N: The size of each dimension.
    :param dr: The grid spacing in the system.
    """

    logger = logging.getLogger(__name__)
    logger.info("Generating Laplacian matrix operator for system of %d dimensions, sized %d", D, N)

    # Initially set DEV2 to be undefined.
    laplacian = None

    # iterate over each dimension in the system.
    for ax in range(D):
        # generate the second order central difference matrix for this axis
        D_n = _partial_derivative_matrix(D, N, ax, dr)
        # if it's the first matrix generated, set DEV2 equal to it.
        if laplacian is None:
            laplacian = D_n
        # otherwise add it, as matrix multiplication is distributive (ie differentiation is distributive)
        else:
            laplacian += D_n

    logger.info("DONE generating Laplacian.")
    logger.info("Setting global variable.")

    global DEV2
    DEV2 = laplacian


def get_laplacian():
    global DEV2
    return DEV2
