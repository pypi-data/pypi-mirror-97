import matplotlib.pyplot as plt


def plot_price_evolution_for_sa_run(sa_log):
    """
    This function plots the evolution of the grid price from a sa_log DataFrame
    obtained running the sa_optimization from the optimization module.

    Parameters
    ----------
        sa_log: :class:`pandas.core.frame.DataFrame`
            DataFrame containing the log of a run from the sa_optimization
            function.
    """

    # Filter data frame to not plot configuration with no hubs
    bounded_sa_log = sa_log[sa_log['price'] != 999999999999999]

    plt.figure(figsize=(10, 5))

    plt.plot(bounded_sa_log['time'], bounded_sa_log['price'], '-',  label='SA')

    plt.legend()

    plt.title('SA run - Grid price evolution')

    plt.xlabel('time [s]')

    plt.ylabel('price [$]')

    plt.show()


def plot_price_evolution_for_nr_run(nr_log):
    """
    This function plots the evolution of the grid price from a nr_log DataFrame.

    Parameters
    ----------
        nr_log: :class:`pandas.core.frame.DataFrame`
            DataFrame containing the log of a run from the nr_optimization
            function.

    """
    plt.figure(figsize=(10, 5))

    plt.plot(nr_log['time'], nr_log['virtual_price'], '.',  label='NR')

    plt.legend()

    plt.grid()

    plt.title('Network Relaxation run - Grid price evolution')

    plt.xlabel('time [s]')

    plt.ylabel('price [$]')

    plt.show()


def plot_price_evolution_for_ga_run(ga_log):
    """
    This function plots the evolution of the grid price from a nr_log DataFrame.

    Parameters
    ----------
        nr_log: :class:`pandas.core.frame.DataFrame`
            DataFrame containing the log of a run from the nr_optimization
            function.

    """
    # Filter data frame to not plot configuration with no hubs
    bounded_ga_log = ga_log[ga_log['price'] < 999999999999998]

    plt.figure(figsize=(6, 3))

    plt.plot(bounded_ga_log['birth_time'],
             bounded_ga_log['price'],
             '.',  label='GA')

    plt.legend()

    plt.grid()

    plt.title('Genetic Algorithm run - Grid price evolution')

    plt.xlabel('time [s]')

    plt.ylabel('price [$]')

    plt.show()

    # Plot curve of price of fittest chromosome in each generation

    plt.figure(figsize=(6, 3))

    ga_log_only_elites = bounded_ga_log[
                            bounded_ga_log['rank_in_generation'] == 1]

    plt.plot(ga_log_only_elites['birth_time'],
             ga_log_only_elites['price'],
             '.-',  label='GA')

    plt.legend()

    plt.grid()

    plt.title('Genetic Algorithm run - Fittest chromosome price evolution')

    plt.xlabel('time [s]')

    plt.ylabel('price [$]')

    plt.show()

    # Plot average chromosome price per generation

    plt.figure(figsize=(6, 3))
    average_price_per_generation = [
        bounded_ga_log[bounded_ga_log['generation'] == generation
                       ].mean(axis=0)['price']
        for generation in bounded_ga_log['generation'].unique()]

    ga_log_only_elites = bounded_ga_log[
                            bounded_ga_log['rank_in_generation'] == 1]
    plt.plot(ga_log_only_elites['birth_time'],
             average_price_per_generation,
             '.-',  label='GA')
    plt.legend()
    plt.grid()
    plt.title('Genetic Algorithm run - Average chromosome price evolution')
    plt.xlabel('time [s]')
    plt.ylabel('price [$]')
    plt.show()