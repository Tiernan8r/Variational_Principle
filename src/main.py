import variational_principle as vp
import plot as plt


def main():

    # Whether to plot the potential function or not.
    include_potential = False

    # The size and range of the grid
    start, stop, N = -10, 10, 100
    # The number of orders of psi to calculate
    num_states = 1
    # The number of axes of the system
    D = 1
    # Number of times to generate samples in the wavefunction
    num_iterations = 10 ** 5

    # a factor to scale the psi by when plotting it together with the potential function in the 1D case.
    v_scale = 10

    r, V, all_psi, all_E = vp.compute(start, stop, N, D, num_states, num_iterations)

    i = 0
    for E in all_E:
        # Display the final energy of the wavefunction to the console.
        print("Final Energy for state", i, "is", E, "eV")
        i += 1

    # plot the generated psis.
    plt.plot_system(r, all_psi, D, include_potential, V, v_scale)


main()
