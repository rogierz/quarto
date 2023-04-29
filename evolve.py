import os
import pickle
import random
from players import EvolutionaryPlayer
from players.evolutionary import PlayerParams, FILE_PATH
from tqdm import trange, tqdm
from contextlib import redirect_stdout
POPULATION_SIZE = 100
OFFSPRING_SIZE = 100
GENERATIONS = 50
MUTATION_RATE = 0.1


def tournament(population, tournament_size):
    return max(
        random.choices(
            population,
            k=tournament_size),
        key=lambda i: i.fitness)


def evolve():
    population = [PlayerParams([0.5, 0.5, 0.5])
                  for _ in range(POPULATION_SIZE)]
    for _ in trange((GENERATIONS), desc="Iteration", position=0):
        offspring = []
        for _ in trange(
                OFFSPRING_SIZE,
                desc="Offspring",
                position=1,
                leave=False):
            with redirect_stdout(None):
                p1 = ~tournament(population, 2)
                p2 = ~tournament(population, 2)
            o = p1 ^ p2
            offspring.append(o)
        population += offspring
        with redirect_stdout(None):
            population = sorted(
                population,
                key=lambda i: i.fitness,
                reverse=True)[
                :POPULATION_SIZE]
    return population[0]


if __name__ == "__main__":
    if os.path.isfile(FILE_PATH):
        choice = input("Do you really want to delete the existing agent? ")
        if choice == "N" or choice == "n":
            print("Nice, bye then.")
            exit(0)

    best_agent = evolve()
    with open(FILE_PATH, "wb+") as fs:
        pickle.dump(best_agent, fs)
