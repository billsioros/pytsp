
import logging
from random import choice, random, randrange, shuffle

from pytsp import SimulatedAnnealing


class Sort(SimulatedAnnealing):
    class Traits:
        class Mutate:
            def shift_1(self, elements):
                neighbor = elements[:]

                i = randrange(0, len(elements))
                j = randrange(0, len(elements))

                neighbor.insert(j, neighbor.pop(i))

                return neighbor

        class Cost:
            def ordered(self, individual):
                mispositioned = 0
                for i in range(0, len(individual) - 1):
                    for j in range(i + 1, len(individual)):
                        mispositioned += individual[i] > individual[j]

                return mispositioned


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    sorter = Sort(mutate='shift_1', cost='ordered')

    individual = list(range(10))

    shuffle(individual)

    best, cost = sorter.fit(individual)

    logging.getLogger('GuessString').info(
        'Best: %s, Cost: %5.3f' % (best, cost)
    )
