import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt

from advanced import dpll, to_cnf
from sat import parse_expression
from simple import solve as ssolve


def generate_expression(max_depth: int, density: float = 0.7, num_vars: int = 5):
    """Generates a random expression, provided some paramters.

    Args:
        max_depth (int): The maximum depth that the expression can reach. Setting to 0 always gives a single literal.
        density (float): A value in [0, 1] that represents the probability that a generated term is an operator (as opposed to a literal). Increasing creates a deeper-nested expression.
        num_vars (int): The maximum number of variables that the expression can contain.

    Returns:
        An expression represented as tuples following the format given in the specification.
    """
    vars = [f"x{i + 1}" for i in range(num_vars)]

    def _gen(depth):
        if depth == 0 or random.random() > density:
            var = random.choice(vars)

            if random.choice([True, False]):
                return var
            else:
                return ("~", var)
        else:
            op = random.choice(["+", "-"])
            return (op, _gen(depth - 1), _gen(depth - 1))

    return _gen(max_depth)


def test_once(expr):
    """Measures the execution time to solve the given expression. Prints an error message if the two solvers disagree.

    Returns:
        A tuple `(simple_time, advanced_time, cnf_time)`, where `cnf_time` is the time taken to convert the expression to CNF for the advanced solver."""
    s_start = timer()
    s = ssolve(expr)
    s_time = timer() - s_start

    cnf_start = timer()
    cnf = to_cnf(parse_expression(expr))
    cnf_time = timer() - cnf_start

    a_start = timer()
    a = dpll(cnf)
    a_time = timer() - a_start

    if s != a:
        print("\n--- Solver mismatch ---")
        print(f" {parse_expression(expr)}")
        print(f"Simple: {s}, Advanced: {a}")

    return s_time, a_time, cnf_time


def average_times(n, max_depth, density, num_vars):
    """Measures the average execution times of `n` expressions, generated using `generate_expression` with the provided parameters.

    Returns:
        A tuple `(simple_time, advanced_time, cnf_time)` of average times, where `cnf_time` is the time taken to convert the expression to CNF for the advanced solver.
    """
    s_total = a_total = cnf_total = 0.0

    for _ in range(n):
        expr = generate_expression(max_depth, density, num_vars)
        s_time, a_time, cnf_time = test_once(expr)
        s_total += s_time
        a_total += a_time
        cnf_total += cnf_time

    return (
        s_total / n,
        a_total / n,
        cnf_total / n,
    )


def test_many(n: int, max_depth: int = 5, density: float = 0.7, num_vars: int = 5):
    """Measures the average execution times of `n` expressions, generated using `generate_expression` with the provided parameters. Prints the results."""
    s_total, a_total, cnf_total = average_times(n, max_depth, density, num_vars)

    print(f"\n--- Results from {n:,} tests ---")
    print(f"Simple avg:   {s_total * 1e6 / n:.1f}μs")
    print(f"Advanced avg: {a_total * 1e6 / n:.1f}μs")
    print(f"CNF Conversion avg: {cnf_total * 1e6 / n:.1f}μs")

    print(f"\nTook ~{s_total + a_total:.0f}s")
    print(f"Max Depth: {max_depth}, Density: {density}, Num Vars: {num_vars}")
    print(f"e.g. {generate_expression(max_depth, density, num_vars)}")


def produce_graphs(n=20):
    # The points to measure
    depths = range(1, 8)
    densities = [x / 10 for x in range(1, 10)]
    num_vars_list = range(3, 10)

    results_depth, results_density, results_vars = [], [], []

    # Vary depth
    for d in depths:
        t = average_times(n, d, 0.7, 5)
        results_depth.append(t)
        print(f"Depth {d}: s={t[0]:.6f}s, a={t[1]:.6f}s, cnf={t[2]:.6f}s")

    # Vary density
    for dens in densities:
        t = average_times(n, 5, dens, 5)
        results_density.append(t)
        print(f"Density {dens}: s={t[0]:.6f}s, a={t[1]:.6f}s, cnf={t[2]:.6f}s")

    # Vary num_vars
    for nv in num_vars_list:
        t = average_times(n, 5, 0.7, nv)
        results_vars.append(t)
        print(f"Vars {nv}: s={t[0]:.6f}s, a={t[1]:.6f}s, cnf={t[2]:.6f}s")

    # Plot
    def plot_results(xs, results, xlabel, title):
        s_times = [r[0] * 1e6 for r in results]
        a_times = [r[1] * 1e6 for r in results]
        # cnf_times = [r[2] * 1e6 for r in results]

        plt.figure(figsize=(7, 4))
        plt.plot(xs, s_times, "o-", label="Simple Solver (μs)")
        plt.plot(xs, a_times, "o-", label="DPLL Solver (μs)")
        # plt.plot(xs, cnf_times, "o-", label="CNF Conversion (μs)")
        plt.xlabel(xlabel)
        plt.ylabel("Average Time (μs)")
        plt.title(title)
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

    plot_results(depths, results_depth, "Expression Depth", "Performance vs Depth")
    plot_results(densities, results_density, "Expression Density", "Performance vs Density")
    plot_results(num_vars_list, results_vars, "Number of Variables", "Performance vs Number of Variables")

    plt.show()


if __name__ == "__main__":
    test_many(5_000)
    produce_graphs(n=100)
