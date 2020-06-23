import variational_principle as vp
import plot as plt
import json_data

def main():

    data_file = json_data.JsonData()

    # Whether to plot the potential function or not.
    include_potential = data_file.plot_with_potential

    # The size and range of the grid
    start, stop, N = data_file.start, data_file.stop, data_file.num_samples
    # The number of orders of psi to calculate
    num_states = data_file.num_states
    # The number of axes of the system
    D = data_file.num_dimensions
    # Number of times to generate samples in the wavefunction
    num_iterations = 10 ** data_file.num_iterations

    # a factor to scale the psi by when plotting it together with the potential function in the 1D case.
    v_scale = data_file.plot_scale

    r, V, all_psi, all_E = vp.compute(start, stop, N, D, num_states, num_iterations)

    i = 0
    for E in all_E:
        # Display the final energy of the wavefunction to the console.
        print("Final Energy for state", i, "is", E, "eV")
        i += 1

    # plot the generated psis.
    plt.plot_system(r, all_psi, D, include_potential, V, v_scale)


main()
