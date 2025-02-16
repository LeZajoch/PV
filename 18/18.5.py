import json
import os
import random
import time
from datetime import datetime
from itertools import permutations
import matplotlib.pyplot as plt


class Boat:
    def __init__(self, count):
        """
        Instead of passing a list of numbers, 'count' represents the number
        of random numbers to be generated for the boat.
        """
        self.numbers = [random.randint(1, 1000) for _ in range(count)]
        print("Generated numbers:", self.numbers)

    def boat_brute_force(self):
        """
        Evaluates every possible ordering of the boat's numbers.
        The rating for an ordering is defined as the absolute difference
        between the first and the last element.

        Time Complexity: O(n!) and Memory Complexity: O(n!)
        (n is the number of boat elements.)
        """
        states = list(permutations(self.numbers))
        min_difference = float('inf')
        best_permutations = []

        # Determine the minimum endpoint difference.
        for perm in states:
            difference = abs(perm[0] - perm[-1])
            if difference < min_difference:
                min_difference = difference

        # Collect all orderings achieving this minimum difference.
        for perm in states:
            if abs(perm[0] - perm[-1]) == min_difference:
                best_permutations.append(perm)

        return best_permutations

    def boat_monte_carlo(self, guesses):
        """
        Randomly samples a specified number of orderings (guesses) and returns
        all unique orderings (with their reversals) that achieve the best
        endpoint difference.

        Time Complexity: O(n!) because it generates all permutations
        before sampling.
        Memory Complexity: O(n!)
        """
        states = list(permutations(self.numbers))
        sampled_states = random.sample(states, min(guesses, len(states)))
        min_difference = float('inf')
        best_permutations = []

        for perm in sampled_states:
            difference = abs(perm[0] - perm[-1])
            if difference < min_difference:
                min_difference = difference

        for perm in sampled_states:
            if abs(perm[0] - perm[-1]) == min_difference:
                if perm not in best_permutations:
                    best_permutations.append(perm)
                reversed_perm = perm[::-1]
                if reversed_perm not in best_permutations:
                    best_permutations.append(reversed_perm)

        return best_permutations

    def boat_heuristic(self):
        """
        For a boat of any size this heuristic:
          1. Sorts the list of numbers.
          2. Finds the pair of adjacent numbers with the smallest difference
             to be used as endpoints.
          3. Places the remaining numbers (in sorted order) in the middle.
          4. Returns both the computed ordering and its reversal.

        Time Complexity: O(n log n)
        Memory Complexity: O(n)
        """
        if len(self.numbers) < 2:
            return [tuple(self.numbers)]

        sorted_numbers = sorted(self.numbers)
        best_diff = float('inf')
        best_index = 0

        # Find the adjacent pair with the smallest difference.
        for i in range(len(sorted_numbers) - 1):
            diff = abs(sorted_numbers[i + 1] - sorted_numbers[i])
            if diff < best_diff:
                best_diff = diff
                best_index = i

        endpoint1 = sorted_numbers[best_index]
        endpoint2 = sorted_numbers[best_index + 1]

        # Get the middle values.
        remaining = sorted_numbers.copy()
        remaining.remove(endpoint1)
        remaining.remove(endpoint2)

        best_permutation = (endpoint1,) + tuple(remaining) + (endpoint2,)
        reversed_permutation = best_permutation[::-1]

        return [best_permutation, reversed_permutation]


def append_performance_data(data, filename="performance_data.json"):
    """
    Appends the provided data to a JSON file. If the file does not exist or is
    empty/invalid, a new JSON array is created.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)
    print(f"\nPerformance data appended to {filename}")


def plot_execution_time_graph(perf_algorithms,
                              title="Execution Times by Algorithm"):
    """
    Generates a bar chart for the provided execution times.

    Parameters:
        perf_algorithms (dict): Dictionary where keys are algorithm names and
                                values are dicts containing 'execution_time_in_seconds'.
        title (str): Title of the graph.

    The graph is saved to a uniquely named PNG file in the 'diagrams/last' folder
    and is displayed.
    """
    algorithms = list(perf_algorithms.keys())
    execution_times = [
        perf_algorithms[algo]["execution_time_in_seconds"]
        for algo in algorithms
    ]

    plt.figure(figsize=(8, 6))
    # Use a classic color scheme.
    colors = ['blue', 'green', 'orange']
    plt.bar(algorithms, execution_times, color=colors[: len(algorithms)])
    plt.xlabel("Algorithms")
    plt.ylabel("Execution Time (seconds)")
    plt.title(title)

    # Annotate bars with execution times.
    for idx, exec_time in enumerate(execution_times):
        plt.text(idx, exec_time, f"{exec_time:.6f}", ha="center", va="bottom")

    plt.tight_layout()

    # Ensure the diagrams/last folder exists.
    os.makedirs("diagrams/last", exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    exec_filename = f"diagrams/last/execution_time_graph_{timestamp_str}.png"
    plt.savefig(exec_filename)
    plt.show()
    print(f"\nExecution time graph saved as {exec_filename}")


def plot_average_execution_time_graph(
        performance_json="performance_data.json",
        title="Average Execution Times over Last 100 Attempts"
):
    """
    Loads performance data from the provided JSON file, calculates the average execution
    time for each algorithm over the last 100 attempts (or fewer if less than 100 available),
    and plots a bar chart using a pastel color scheme. The graph is saved in the 'diagrams/average'
    folder with a unique filename and displayed.
    """
    try:
        with open(performance_json, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("No performance data found.")
        return

    if not data:
        print("No performance data available to plot.")
        return

    # Use only the last 100 runs (or all if fewer).
    last_attempts = data[-100:] if len(data) >= 100 else data

    # Aggregate the execution times.
    avg_times = {}
    counts = {}
    for record in last_attempts:
        algos = record.get("algorithms", {})
        for algo_name, algo_data in algos.items():
            exec_time = algo_data.get("execution_time_in_seconds")
            if exec_time is not None:
                avg_times[algo_name] = avg_times.get(algo_name, 0.0) + exec_time
                counts[algo_name] = counts.get(algo_name, 0) + 1

    for algo in avg_times:
        avg_times[algo] /= counts[algo]

    algorithms = list(avg_times.keys())
    execution_times = [avg_times[algo] for algo in algorithms]

    plt.figure(figsize=(8, 6))
    # Use a pastel color palette.
    pastel_colors = ['lightblue', 'lightgreen', 'lightcoral', 'plum']
    plt.bar(algorithms, execution_times, color=pastel_colors[: len(algorithms)])
    plt.xlabel("Algorithms")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title(title)

    for idx, exec_time in enumerate(execution_times):
        plt.text(idx, exec_time, f"{exec_time:.6f}", ha="center", va="bottom")

    plt.tight_layout()
    os.makedirs("diagrams/average", exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    avg_filename = f"diagrams/average/average_execution_time_graph_{timestamp_str}.png"
    plt.savefig(avg_filename)
    plt.show()
    print(f"\nAverage execution time graph saved as {avg_filename}")


if __name__ == "__main__":
    # Instantiate Boat with count of random numbers (e.g., 6)
    b1 = Boat(10)

    # Time the brute force approach.
    start_time = time.time()
    brute_force_result = b1.boat_brute_force()
    brute_force_time = time.time() - start_time

    # Time the Monte Carlo approach (using 4 random samples).
    start_time = time.time()
    monte_carlo_result = b1.boat_monte_carlo(4)
    monte_carlo_time = time.time() - start_time

    # Time the heuristic approach.
    start_time = time.time()
    heuristic_result = b1.boat_heuristic()
    heuristic_time = time.time() - start_time

    # Display run results.
    print("\nBrute Force Best Permutations:")
    print(brute_force_result)
    print(f"Execution Time: {brute_force_time:.6f} seconds")

    print("\nMonte Carlo Best Permutations (using 4 random samples):")
    print(monte_carlo_result)
    print(f"Execution Time: {monte_carlo_time:.6f} seconds")

    print("\nHeuristic Boat Orderings:")
    print(heuristic_result)
    print(f"Execution Time: {heuristic_time:.6f} seconds")

    # Prepare performance data for logging.
    run_data = {
        "timestamp": datetime.now().isoformat(),
        "generated_numbers": b1.numbers,
        "algorithms": {
            "boat_brute_force": {
                "execution_time_in_seconds": brute_force_time,
                "time_complexity": "O(n!)",
                "memory_complexity": "O(n!)",
                "output_items": len(brute_force_result),
            },
            "boat_monte_carlo": {
                "execution_time_in_seconds": monte_carlo_time,
                "time_complexity": "O(n!) (due to full permutation generation)",
                "memory_complexity": "O(n!)",
                "output_items": len(monte_carlo_result),
            },
            "boat_heuristic": {
                "execution_time_in_seconds": heuristic_time,
                "time_complexity": "O(n log n)",
                "memory_complexity": "O(n)",
                "output_items": len(heuristic_result),
            },
        },
    }

    # Append performance data to JSON file.
    append_performance_data(run_data)

    # Plot the current execution times into diagrams/last.
    plot_execution_time_graph(run_data["algorithms"])

    # Plot average execution times for the last 100 runs into diagrams/average.
    plot_average_execution_time_graph()
