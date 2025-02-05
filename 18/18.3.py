from itertools import permutations
import random

class Boat:
    def __init__(self, numbers):
        self.numbers = numbers

    def boat_brute_force(self):
        states = list(permutations(self.numbers, 3))
        min_difference = float('inf')
        best_permutations = []

        for perm in states:
            difference = abs(perm[0] - perm[2])
            if difference < min_difference:
                min_difference = difference

        for perm in states:
            if abs(perm[0] - perm[2]) == min_difference:
                best_permutations.append(perm)

        return best_permutations

    def boat_monte_carlo(self, guesses):
        states = list(permutations(self.numbers, 3))
        sampled_states = random.sample(states, min(guesses, len(states)))
        min_difference = float('inf')
        best_permutations = []

        for perm in sampled_states:
            difference = abs(perm[0] - perm[2])
            if difference < min_difference:
                min_difference = difference

        for perm in sampled_states:
            if abs(perm[0] - perm[2]) == min_difference:
                if perm not in best_permutations:
                    best_permutations.append(perm)
                reversed_perm = perm[::-1]
                if reversed_perm not in best_permutations:
                    best_permutations.append(reversed_perm)

        return best_permutations

    def boat_heuristic(self):
        numbers = sorted(self.numbers)
        best_permutation = (numbers[1], numbers[2], numbers[0])
        reversed_permutation = best_permutation[::-1]
        return [best_permutation, reversed_permutation]


# Testování
b1 = Boat([73, 85, 81, 94, 103, 345])
print(b1.boat_brute_force())
print(b1.boat_monte_carlo(4))
print(b1.boat_heuristic())




#monte carlo nesmi pouzivat permutations bo pak to je stejne narocne jako bruteforce neboli N!