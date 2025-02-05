from itertools import permutations
import random

class Boat:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def boat_brute_force(self):
        states = list(permutations([self.a, self.b, self.c]))
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
        states = list(permutations([self.a, self.b, self.c]))
        sampled_states = random.sample(states, min(guesses, len(states)))  # Náhodně vybereme "guesses" permutací
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
        numbers = sorted([self.a, self.b, self.c])  # Seřadíme čísla
        best_permutation = (numbers[1], numbers[2], numbers[0])

        # Opačné pořadí, pokud ještě není v seznamu
        reversed_permutation = best_permutation[::-1]

        return [best_permutation, reversed_permutation]




b1 = Boat(73, 85, 81)
print(Boat.boat_brute_force(b1))
print(Boat.boat_monte_carlo(b1,4))
print(Boat.boat_heuristic(b1))