
import logging
from random import choice, random, randrange
from string import printable

from pytsp import GeneticAlgorithm


class GuessString(GeneticAlgorithm):
    class Traits:
        class Mutate:
            def randomize(self, individual):
                return ''.join([
                    choice(printable)
                    if random() < self.per_character_mutation_probability
                    else individual[i]
                    for i in range(len(individual))
                ])

        class Crossover:
            def cut_and_stitch(self, individual_a, individual_b):
                left = individual_a[:len(individual_a) // 2]
                right = individual_b[len(individual_b) // 2:]

                return left + right

        class Select:
            def random_top_half(self, population):
                return population[randrange(0, len(population) // 2)]

        class Fitness:
            def least_squares(self, individual):
                squared_sum = 0
                for i in range(len(self.target)):
                    squared_sum += (ord(individual[i]) - ord(self.target[i])) ** 2

                return 1 / (squared_sum + 1)

    def __init__(self, target, *args, per_character_mutation_probability=0.1, **kwargs):
        super().__init__(*args, **kwargs)

        self.target = target
        self.per_character_mutation_probability = per_character_mutation_probability


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    target = 'Hello World!'

    string_guesser = GuessString(
        target,
        mutate='randomize',
        crossover='cut_and_stitch',
        select='random_top_half',
        fitness='least_squares',
        max_iterations=10000
    )

    individual = ''.join([choice(printable) for _ in range(len(target))])

    fittest = string_guesser.fit(individual)

    logging.getLogger('GuessString').info(
        'Fitest: %s, Fitness: %5.3f' % (
            fittest, string_guesser.fitness(fittest))
    )
