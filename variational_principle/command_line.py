from variational_principle import variation_method as vp
from variational_principle import plot as plt
from variational_principle.data_handling import computation_data

import logging
import logging.config
import json


def run_computation():

    logging.config.dictConfig(json.load(open("data/logging.json", "r")))
    logger = logging.getLogger(__name__)

    logger.debug("Beginning simulation:")

    logger.debug("Loading system info from 'data.json':")
    data = computation_data.ComputationData()
    logger.debug("DONE reading json file.")

    logger.debug("Assigning variables from 'data.json'")
    # Whether to plot the potential function or not.
    include_potential = data.plot_with_potential
    logger.debug("Set `include_potential` to %s", include_potential)

    # The size and range of the grid
    start, stop, N = data.start, data.stop, data.num_samples
    logger.debug("Set `start` to %f", start)
    logger.debug("Set `stop` to %f", stop)
    logger.debug("Set `N` to %d", N)

    # The number of orders of psi to calculate
    num_states = data.num_states
    logger.debug("Set `num_states` to %d", num_states)
    # The number of axes of the system
    D = data.num_dimensions
    logger.debug("Set `D` to %d", D)
    # Number of times to generate samples in the wavefunction
    num_iterations = 10 ** data.num_iterations
    logger.debug("Set `num_iterations` to %d", num_iterations)

    # a factor to scale the psi by when plotting it together with the potential function in the 1D case.
    v_scale = data.plot_scale
    logger.debug("Set `v_scale` to %f", v_scale)

    logger.debug("Computing the energy eigenstates")

    data = vp.compute(data)
    r = data.r
    V = data.V
    all_psi = data.all_psi
    all_E = data.all_energy
    logger.debug("DONE computing energy eigenstates")

    i = 0
    for E in all_E:
        # Display the final energy of the wavefunction to the console.
        # print("Final Energy for state", i, "is", E, "eV")
        logger.info("Final Energy for state %d is %seV" % (i, E))
        logger.debug("Final Energy for state %d is %feV", i, E)
        i += 1

    logger.debug("Beginning plotting:")
    # plot the generated psis.
    plt.plot_system(r, all_psi, D, include_potential, V, v_scale)
    logger.debug("DONE plotting")

    logger.debug("--END--")
