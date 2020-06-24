import variational_principle.variational_principle as vp
import variational_principle.plot as plt
import variational_principle.json_data as json_data

import logging
import logging.config
import json

def main():

    logging.config.dictConfig(json.load(open("logging.json")))
    logger = logging.getLogger(__name__)

    logger.info("Beginning simulation:")

    logger.info("Loading system info from 'data.json':")
    data_file = json_data.JsonData()
    logger.info("DONE reading json file.")

    logger.info("Assigning variables from 'data.json'")
    # Whether to plot the potential function or not.
    include_potential = data_file.plot_with_potential
    logger.info("Set `include_potential` to %s", include_potential)

    # The size and range of the grid
    start, stop, N = data_file.start, data_file.stop, data_file.num_samples
    logger.info("Set `start` to %f", start)
    logger.info("Set `stop` to %f", stop)
    logger.info("Set `N` to %d", N)

    # The number of orders of psi to calculate
    num_states = data_file.num_states
    logger.info("Set `num_states` to %d", num_states)
    # The number of axes of the system
    D = data_file.num_dimensions
    logger.info("Set `D` to %d", D)
    # Number of times to generate samples in the wavefunction
    num_iterations = 10 ** data_file.num_iterations
    logger.info("Set `num_iterations` to %d", num_iterations)

    # a factor to scale the psi by when plotting it together with the potential function in the 1D case.
    v_scale = data_file.plot_scale
    logger.info("Set `v_scale` to %f", v_scale)

    logger.info("Computing the energy eigenstates")
    r, V, all_psi, all_E = vp.compute(start, stop, N, D, num_states, num_iterations)
    logger.info("DONE computing energy eigenstates")

    i = 0
    for E in all_E:
        # Display the final energy of the wavefunction to the console.
        print("Final Energy for state", i, "is", E, "eV")
        logger.info("Final Energy for state %d is %feV", i, E)
        i += 1

    logger.info("Beginning plotting:")
    # plot the generated psis.
    plt.plot_system(r, all_psi, D, include_potential, V, v_scale)
    logger.info("DONE plotting")

    logger.info("--END--")


if __name__ == "__main__":
    main()
