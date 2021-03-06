import random

import numpy as np
import scipy.linalg as la

import variational_principle.quantum_operators as qo
import variational_principle.calculus.laplacian as lap
import variational_principle.potential_handling.potential as pot
import variational_principle.data_handling.computation_data as ci

import logging
import time


def nth_state(r: np.ndarray, v: np.ndarray, dr: float, D: int, N: int, num_iterations: int,
              prev_psi_linear: np.ndarray, n: int) -> (np.ndarray, float):
    """
    Calculates the nth psi energy eigenstate wavefunction of a given potential system.
    :param r: The grid coordinates.
    :param dr: The grid spacing.
    :param D: The number of axes in the system.
    :param N: The size of each axis.
    :param num_iterations: The number of iterations to calculate over.
    :param prev_psi_linear: The previous calculated psi states for the potential system.
    :param n: The order of the state.
    :return: The energy eigenstate wavefunction psi of order n for the potential system.
    """

    logger = logging.getLogger(__name__)
    logger.debug("Beginning computation of energy eigenstate.")

    logger.debug("Calculating the orthonormal basis.")
    # Get the orthonormal basis for this state, by finding the null space if the previous lower order psi
    orthonormal_basis = la.null_space(prev_psi_linear).T

    logger.debug("Calculating the potential")
    # turn the potential grid into a linear column vector for linear algebra purposes.
    V = v.reshape(N ** D)

    logger.debug("Setup default wavefunction.")
    # generate an initial psi, I've found that a quadratic function works nicely (no discontinuities.)
    psi = (0.5 * r ** 2).sum(axis=0)
    # psi = np.ones(r.shape).sum(axis=0)

    # linearise psi from a grid to a column vector
    psi = psi.reshape(N ** D)

    logger.debug("Filtering infinite values from the wavefunction, potential and orthonormal basis.")
    # Account for infinite values in the potential:
    len_V = len(V)
    # Keep track of all the indices that have an inf value for the V.
    nan_indices = [False] * len_V
    for j in range(len_V):
        # # Tag the bordering points as well.
        # a, b = j - 1, j + 1
        # if a < 0:
        #     a = 0
        # if b >= len_V:
        #     b = len_V - 1
        #
        # if not np.isfinite(V[j]) and (not np.isfinite(V[a]) and not np.isfinite(V[b])):
        #     # nan_indices[a] = nan_indices[j] = nan_indices[b] = True
        #     nan_indices[j] = True
        if not np.isfinite(V[j]):
            nan_indices[j] = True

    # filter the corresponding psi values to be = 0
    psi = np.where(nan_indices, 0, psi)

    # filter the values in the orthonormal basis to be 0
    for j in range(n - 1):
        nan_indices[j] = False
    orthonormal_basis = np.where(nan_indices, 0, orthonormal_basis)

    logger.debug("Calculating previous energy.")
    # get a default initial energy to compare against.
    prev_E = qo.energy(psi, V, dr)

    # Keep track of the number of orthonormal bases that there are.
    num_bases = len(orthonormal_basis)

    logger.debug("Iterating over %d simulation(s)", num_iterations)
    t1 = time.time()
    logger.debug("Simulation began at [%s]", time.asctime())

    # loop for the desired number of iterations
    for i in range(num_iterations):

        # generate a random orthonormal basis to sample.
        rand_index = random.randrange(num_bases)

        # generate a random value to change by that converges to 0 as we sample more.
        rand_change = random.random() * 0.1 * (num_iterations - i) / num_iterations

        # 50% of the time, add, the other 50% take away
        if random.random() > 0.5:
            rand_change *= -1

        # get the orthonormal basis that we are sampling with
        basis_vector = orthonormal_basis[rand_index]

        # tweak the psi wavefunction by the generated change, with the given basis.
        psi += basis_vector * rand_change
        # re normalise the changed psi
        psi = qo.normalise(psi, dr)

        # get the corresponding new energy for the changed psi
        new_E = qo.energy(psi, V, dr)

        # if the new energy is lower than the current energy, keep the change.
        if new_E < prev_E:
            prev_E = new_E
        # otherwise set psi back to the way it was before the change.
        else:
            psi -= basis_vector * rand_change
            psi = qo.normalise(psi, dr)

    t2 = time.time()
    logger.debug("Simulation done at  [%s]", time.asctime())
    logger.debug("Took %f second(s)", t2 - t1)

    logger.debug("Calculating final energy of the eigenstate.")
    # compute the energy of the resulted wavefunction
    final_energy = qo.energy(psi, V, dr)

    # turn psi back from a column vector to a grid.
    psi = psi.reshape([N] * D)

    logger.debug("Correcting the arbitrary phase of the computed eigenstate.")
    # Correction of phase, to bring it to the positive for nicer plotting.
    phase = np.sum(psi) * dr
    if phase < 0:
        psi *= -1

    logger.debug("DONE oomputing energy eigenstate and eigenvalue")
    # return the generated psi as a grid.
    return psi, final_energy


def calculate_r(computed_data):

    start = computed_data.start
    stop = computed_data.stop
    N = computed_data.num_samples
    D = computed_data.num_dimensions

    x = np.linspace(start, stop, N)
    # The axes along each dimension
    axes = [x]
    for i in range(D - 1):
        axes.append(x)
    # populate the grid using the axes.
    r = np.array(np.meshgrid(*axes, indexing="ij"))
    return r


def compute(computed_data: ci.ComputationData, write_pipe=None) -> (
        np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    """
    The method to set up the variables and system, and aggregate the computed wavefunctions.
    :param computed_data: a ComputedData object containing info required to set up calculation.
    :param write_pipe: A Connection object for a pipe to write computed data to if implementing multiprocessing.
    :return: r, V, all_psi: the grid, potential function and the list of all the wavefunctions.
    """

    start = computed_data.start
    stop = computed_data.stop
    N = computed_data.num_samples
    D = computed_data.num_dimensions
    num_states = computed_data.num_states
    num_iterations = 10 ** computed_data.num_iterations

    logger = logging.getLogger(__name__)
    logger.debug("Beginning computation of %d energy eigenstate(s).", num_states)

    # Set a seed for repeatable results.
    random.seed("THE-VARIATIONAL-PRINCIPLE")

    # Keep the number of states in bounds, so that the orthonormal basis generator doesn't return an error.
    if num_states >= N:
        logger.debug("Total number of states to calculate constrained from %d to %d, due to computational limitation.",
                     num_states, N - 2)
        num_states = N - 2

    logger.debug("Generating spatial grid")
    r = calculate_r(computed_data)
    computed_data.r = r

    logger.debug("Generating potential.")
    # generate the potential for the system
    potential_name = computed_data.potential_name
    V = pot.potential(r, potential_name)
    computed_data.V = V
    if write_pipe is not None:
        write_pipe.send((computed_data.r_key, r))
        logger.debug("Sent position array through pipe.")
        write_pipe.send((computed_data.v_key, V))
        logger.debug("Sent potential array through pipe.")

    # Calculate the grid spacing for the symmetric grid.
    dr = (stop - start) / N
    logger.debug("The grid spacing of the system is: dr=%f", dr)

    logger.debug("Generating the Laplacian operator for the system.")
    # Generate the 2nd order finite difference derivative matrix.
    lap.generate_laplacian(D, N, dr)

    # Keep track whether we are on the first iteration or not.
    first_iteration = True
    # Set up two arrays to store the generated psi:
    # Stores the psi as linear column vectors, used for calculating the next psi in the series.
    all_psi_linear = np.zeros((1, N ** D))
    # stores in their proper shape as grids, used for plotting.
    all_psi = []
    all_E = []

    logger.debug("Beginning computation of %d states", num_states)
    # iterate over the number of states we want to generate psi for.
    for i in range(num_states):

        logger.debug("Calculating the energy eigenstate and eigenvalue for state %d", i)
        logger.debug("=" * 10)
        # Generate the psi for this order number
        psi, E = nth_state(r, V, dr, D, N, num_iterations, all_psi_linear, i + 1)

        computed_data.add_psi(psi)
        computed_data.add_energy(E)

        if write_pipe is not None:
            key = "state_{}".format(i)
            write_pipe.send((key, psi))
            write_pipe.send(E)

        logger.debug("=" * 10)
        logger.debug("DONE generating energy eigenstate and eigenvalue")

        logger.debug("Saving computed values to data sets")
        # Store the generated psi in both ways in their corresponding arrays.
        all_psi.append(psi)
        all_E.append(E)

        psi_linear = psi.reshape(N ** D)
        if first_iteration:
            all_psi_linear = np.array([psi_linear])
            first_iteration = False
        else:
            all_psi_linear = np.vstack((all_psi_linear, [psi_linear]))

    logger.debug("DONE simulation of %d energy eigenstate(s)", num_states)
    computed_data.r = r
    computed_data.V = V
    # computation_data.all_psi = all_psi
    # computation_data.all_energy = all_E

    return computed_data
