from typing import Dict, List, Callable, Literal, Tuple
import random
import pandas as pd
import matplotlib.pyplot as plt


def generate_random_solution(num_items: int, num_bins: int) -> List[int]:
    """Generate a random bin packing solution.

    Args:
        num_items (int): The number of items to be packed.
        num_bins (int): The number of bins available.

    Returns:
        List[int]: A list where each element `i` represents the bin index assigned to item `i`.
    """
    return [random.randint(1, num_bins) for _ in range(num_items)]


def fitness(solution: List[int], weight_function: Callable[[int], int]) -> int:
    """Calculate the fitness of a bin packing solution.

    Args:
        solution (List[int]): A list where each element `i` represents the bin index assigned to item `i`.
        weight_function (Callable[[int], int]): A function that takes an item index and returns its weight.

    Returns:
        int: The fitness score of the solution, higher is better.
    """
    # Initialise bin weights
    bin_weights = [0] * (max(solution) + 1)

    # Sum weights for each bin
    for item_index, bin_index in enumerate(solution):
        bin_weights[bin_index] += weight_function(item_index + 1)

    heaviest = max(bin_weights)
    lightest = min(bin_weights)
    diff = heaviest - lightest

    return 100 / (1 + diff)


def tournament_select(
    population: List[List[int]], fitness_scores: List[int], tournament_size: int
) -> List[int]:
    """Select a parent solution using tournament selection.

    Args:
        population (List[List[int]]): The current population of solutions.
        fitness_scores (List[int]): The fitness scores corresponding to each solution in the population.
        tournament_size (int): The number of individuals to compete in the tournament.

    Returns:
        List[int]: The selected parent solution.
    """

    # Randomly select 'tournament_size' individuals from the population
    selected_indices = random.sample(range(len(population)), tournament_size)

    # Find the index of the individual with the best fitness
    best_index = max(selected_indices, key=lambda i: fitness_scores[i])

    return population[best_index]


def uniform_crossover(
    parent_1: List[int], parent_2: List[int], crossover_rate: float = 0.8
) -> Tuple[List[int], List[int]]:
    """Perform uniform crossover between two parent solutions to produce two offspring.

    Args:
        parent_1 (List[int]): The first parent solution.
        parent_2 (List[int]): The second parent solution.
        crossover_rate (float, optional): The probability of performing crossover.

    Returns:
        Tuple[List[int], List[int]]: Two offspring solutions resulting from crossover.
    """

    offspring_1 = []
    offspring_2 = []

    if random.random() > crossover_rate:
        # No crossover, return parents as offspring
        return parent_1[:], parent_2[:]

    for gene_1, gene_2 in zip(parent_1, parent_2):
        if random.random() < 0.5:
            offspring_1.append(gene_1)
            offspring_2.append(gene_2)
        else:
            offspring_1.append(gene_2)
            offspring_2.append(gene_1)

    return offspring_1, offspring_2


def mutate(solution: List[int], mutation_rate: float, num_bins: int) -> List[int]:
    """Mutate a solution by randomly changing the bin assignment of items.

    Args:
        solution (List[int]): The original solution.
        mutation_rate (float): The probability of mutating each gene.
        num_bins (int): The number of bins available.

    Returns:
        List[int]: The mutated solution.
    """
    mutated_solution = []

    for gene in solution:
        if random.random() < mutation_rate:
            # Assign to a new random bin
            mutated_solution.append(random.randint(1, num_bins))
        else:
            mutated_solution.append(gene)

    return mutated_solution


def run_genetic_algorithm(
    population_size: int,
    tournament_size: int,
    mutation_rate: float,
    num_bins: int,
    weight_function: Callable[[int], int],
    fitness_calcs: int,
) -> Dict[str, List[float]]:
    """Run the genetic algorithm for bin packing problem.

    Args:
        population_size (int): The size of the population.
        tournament_size (int): The size of the tournament for selection.
        mutation_rate (float): The mutation rate.
        num_bins (int): The number of bins available.
        weight_function (Callable[[int], int]): A function that takes an item index and returns its weight.
        fitness_calcs (int, optional): The total number of fitness calculations to perform.
        outputs (bool, optional): Whether to print progress outputs.

    Returns:
        Dict[str, List[float]]: A dictionary containing fitness statistics over iterations.
    """
    fitness_history = {"best": [], "worst": [], "average": [], "std_dev": []}

    # Initialise a population of random solutions
    population = [
        generate_random_solution(500, num_bins) for _ in range(population_size)
    ]

    for iter in range(int(fitness_calcs / population_size)):
        # Evaluate fitness of each solution using the fitness function
        fitness_scores = [fitness(solution, weight_function) for solution in population]

        # Elitism: Find the best solution
        best_index = fitness_scores.index(max(fitness_scores))
        best_solution = population[best_index]

        # Replace old population with new offspring
        new_population = [best_solution]

        while len(new_population) < population_size:
            # Select two parents
            parent_1 = tournament_select(population, fitness_scores, tournament_size)
            parent_2 = tournament_select(population, fitness_scores, tournament_size)

            # Create offspring
            offspring_1, offspring_2 = uniform_crossover(parent_1, parent_2)
            offspring_1 = mutate(offspring_1, mutation_rate, num_bins)
            offspring_2 = mutate(offspring_2, mutation_rate, num_bins)

            new_population.append(offspring_1)
            new_population.append(offspring_2)

        # Ensure population size remains constant
        population = new_population[:population_size]

        # Calculate and record fitness statistics
        best_fitness = max(fitness_scores)
        worst_fitness = min(fitness_scores)
        average_fitness = sum(fitness_scores) / len(fitness_scores)
        std_dev_fitness = pd.Series(fitness_scores).std()

        fitness_history["best"].append(best_fitness)
        fitness_history["worst"].append(worst_fitness)
        fitness_history["average"].append(average_fitness)
        fitness_history["std_dev"].append(std_dev_fitness)

    return fitness_history


def standard_experiments():
    # Produces four graphs for each problem with different parameter settings

    problem: Literal["BPP1", "BPP2"] = "BPP2"

    # Trial parameters
    # (p, pm, t)
    trial_params = [
        (100, 0.01, 3),
        (100, 0.05, 3),
        (100, 0.01, 7),
        (100, 0.05, 7),
    ]

    if problem == "BPP1":
        num_bins = 10

        def weight_function(i):
            return i

    else:
        num_bins = 50

        def weight_function(i):
            return (i * i) / 2

    print(f"Running trials for problem: {problem}")

    plots_to_render = []

    for p, pm, t in trial_params:
        # Print problem details
        print(f"\nPopulation size: {p}, Mutation rate: {pm}, Tournament size: {t}")

        trial_data = []

        for _ in range(5):
            # Run the genetic algorithm
            fitness_history = run_genetic_algorithm(
                p, t, pm, num_bins, weight_function, fitness_calcs=10_000
            )

            trial_data.append(fitness_history)

            print(
                f"Trial completed. Best fitness: {fitness_history['best'][-1]:.7f}, "
                f"Worst fitness: {fitness_history['worst'][-1]:.7f}, "
                f"Average fitness: {fitness_history['average'][-1]:.7f}, "
                f"Std Dev: {fitness_history['std_dev'][-1]:.8f}"
            )

        # Graph of average fitness against iteration for each trial
        fig, ax = plt.subplots()
        for i, data in enumerate(trial_data):
            ax.plot(data["average"], label=f"Trial {i + 1}")

        ax.set_title(
            f"Average Fitness over Iterations for {problem} (p={p}, pm={pm}, t={t})"
        )
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Average Fitness")
        ax.legend()

        fig.tight_layout(pad=2.0)

        # Uncomment to save figures
        # fig.savefig(f"bpp_ga_results_{problem}_p{p}_pm{pm}_t{t}.png")

        plots_to_render.append(fig)

    # Show all plots
    plt.show()


def population_size_experiment():
    # Experiment varying population size

    # Setup as BPP2 with the best parameters found
    pm, t = (0.01, 7)
    bins = 10

    def weight_function(i):
        return (i * i) / 2

    # Graph fitness against iteration for different population sizes
    # Run each configuration 5 times and show all trials in the same colour per population size
    population_sizes = [10, 50, 100, 400, 800]
    all_trials = {}

    for p in population_sizes:
        trial_data = []

        for _ in range(3):
            # Run the genetic algorithm
            fitness_history = run_genetic_algorithm(
                p, t, pm, bins, weight_function, fitness_calcs=75 * p
            )

            trial_data.append(fitness_history)

            print(f"Trial completed for population size {p}.")

        all_trials[p] = trial_data

    # Choose one colour per population size
    colors = [plt.cm.tab10(i) for i in range(len(population_sizes))]

    # Single figure with lines for each trial, same colour per population size
    fig, ax = plt.subplots()
    for idx, p in enumerate(population_sizes):
        trials = all_trials[p]
        for j, trial in enumerate(trials):
            label = f"Population Size {p}" if j == 0 else "_nolegend_"
            ax.plot(
                range(len(trial["average"])),
                trial["average"],
                color=colors[idx],
                alpha=0.7,
                label=label,
            )

    ax.set_title(f"Average Fitness over Iterations for BPP2 (pm={pm}, t={t})")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Average Fitness")
    ax.legend()

    fig.tight_layout(pad=2.0)
    # fig.savefig("bpp_ga_population_size_experiment.png")

    plt.show()


def mutation_rate_experiment():
    # Additional experiment varying mutation rate

    # Setup as BPP2 with the best parameters found
    p, t = (100, 7)
    bins = 10

    def weight_function(i):
        return (i * i) / 2

    # Graph fitness against iteration for different mutation rates
    # Run each configuration 5 times and show all trials in the same colour per mutation rate
    mutation_rates = [0.0001, 0.001, 0.01, 0.1, 1.0]
    all_trials = {}

    for pm in mutation_rates:
        trial_data = []

        for _ in range(3):
            # Run the genetic algorithm
            fitness_history = run_genetic_algorithm(
                p, t, pm, bins, weight_function, fitness_calcs=10_000
            )

            trial_data.append(fitness_history)

            print(f"Trial completed for mutation rate {pm}.")

        all_trials[pm] = trial_data

    # Choose one colour per mutation rate
    colors = [plt.cm.tab10(i) for i in range(len(mutation_rates))]


    # Single figure with lines for each trial, same colour per mutation rate
    fig, ax = plt.subplots()
    for idx, pm in enumerate(mutation_rates):
        trials = all_trials[pm]
        for j, trial in enumerate(trials):
            label = f"Mutation Rate {pm}" if j == 0 else "_nolegend_"
            ax.plot(
                range(len(trial["average"])),
                trial["average"],
                color=colors[idx],
                alpha=0.7,
                label=label,
            )

    ax.set_title(f"Average Fitness over Iterations for BPP2 (p=100, t={t})")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Average Fitness")
    # ax.set_yscale("log")

    ax.legend()

    fig.tight_layout(pad=2.0)
    fig.savefig("bpp_ga_mutation_rate_experiment.png")

    plt.show()


if __name__ == "__main__":
    # standard_experiments()
    # population_size_experiment()
    mutation_rate_experiment()
