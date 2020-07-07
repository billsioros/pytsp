
from random import random, randrange, shuffle

from pytsp.core import (CompressedAnnealing, GeneticAlgorithm,
                        SimulatedAnnealing, cached, jarvis)


class TravellingSalesman(SimulatedAnnealing, GeneticAlgorithm):
    class Traits(SimulatedAnnealing.Traits, GeneticAlgorithm.Traits):
        class Mutate(GeneticAlgorithm.Traits.Mutate):
            def random_swap(self, elements):
                neighbor = elements[:]

                i, j = randrange(1, len(elements) -
                                 1), randrange(1, len(elements) - 1)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                return neighbor

            def shift_1(self, elements):
                neighbor = elements[:]

                i, j = randrange(1, len(elements) -
                                 1), randrange(1, len(elements) - 1)

                neighbor.insert(j, neighbor.pop(i))

                return neighbor

            def reverse_random_sublist(self, elements):
                neighbor = elements[:]

                i = randrange(1, len(elements) - 1)
                j = randrange(1, len(elements) - 1)

                i, j = min([i, j]), max([i, j])

                neighbor[i:j] = neighbor[i:j][::-1]

                return neighbor

        class Crossover(GeneticAlgorithm.Traits.Crossover):
            def cut_and_stitch(self, individual_a, individual_b):
                individual_a, individual_b

                offspring = individual_a[1:len(individual_a) // 2]
                for b in individual_b[1:-1]:
                    if b not in offspring:
                        offspring.append(b)

                return [individual_a[0]] + offspring + [individual_b[0]]

        class Select(GeneticAlgorithm.Traits.Select):
            def random_top_half(self, population):
                return population[randrange(0, len(population) // 2)]

        class Fitness(GeneticAlgorithm.Traits.Fitness):
            def inverse_cost(self, individual):
                return 1.0 / self.cost(individual)

            def unweighted_mst(self, individual):
                v = len(individual) - 1

                return ((v * v) - v + 1) / self.cost(individual)

            def weighted_mst(self, individual):
                return self.heuristic(individual) / self.cost(individual)

        class Metric:
            def euclidean(self, p1, p2):
                return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

            def manhattan(self, p1, p2):
                return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        class Heuristic:
            @cached
            def kruskal(self, route):
                edges = []
                for u in route[:-1]:
                    for v in route[:-1]:
                        if u != v:
                            edges.append((u, v, self.metric(u, v)))

                edges.sort(key=lambda edge: edge[2])

                cost, components = 0, {v: set([v]) for v in route}

                for u, v, d in edges:
                    if not components[u].intersection(components[v]):
                        cost += d

                        components[u] = components[u].union(components[v])
                        components[v] = components[u]

                        for root, component in components.items():
                            if u in component or v in component:
                                for vertex in component:
                                    components[root] = components[root].union(
                                        components[vertex])

                return cost

        class Criterion:
            def angle(self, c, b, a):
                from math import degrees, atan2

                return degrees(
                    atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0])
                )

            def eccentricity(self, a, b, c):
                d1 = self.metric(a, b)
                d2 = self.metric(b, c)
                d3 = self.metric(a, c)

                return d3 / (d1 + d2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cost(self, route):
        return sum([
            self.metric(route[i], route[i + 1])
            for i in range(len(route) - 1)
        ])

    def nearest_neighbor(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        route, remaining = [depot], cities[:]

        while len(remaining) > 0:
            nearest = (0, self.metric(route[-1], remaining[0]))
            for i in range(1, len(remaining)):
                city = remaining[i]
                distance = self.metric(route[-1], city)
                if distance < nearest[1]:
                    nearest = (i, distance)

            route.append(remaining[nearest[0]])
            del remaining[nearest[0]]

        return route + [depot], self.cost(route + [depot])

    def convex_hull(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        route = jarvis([depot] + cities)
        inner = set([depot] + cities).difference(set(route))
        while inner:
            best, best_i, best_value = None, -1, float("-inf")
            for candidate in inner:
                for i in range(len(route) - 1):
                    value_candidate = self.criterion(
                        route[i], candidate, route[i + 1]
                    )
                    if value_candidate > best_value:
                        best_value = value_candidate
                        best = candidate
                        best_i = i

            inner.remove(best)
            route = route[:best_i + 1] + [best] + route[best_i + 1:]

        while route[0] != depot:
            route.insert(0, route.pop())

        return route + [depot], self.cost(route + [depot])

    def opt_2(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        def reverse_sublist(elements, i, j):
            copy = elements[:]

            copy[i:j] = copy[i:j][::-1]

            return copy

        route = cities[:]
        cost = self.cost([depot] + route + [depot])
        for i in range(0, len(route) - 1):
            for j in range(i + 1, len(route)):
                candidate = reverse_sublist(route, i, j)
                candidate_cost = self.cost([depot] + candidate + [depot])
                if candidate_cost < cost:
                    return self.opt_2(depot, candidate)

        return [depot] + route + [depot], self.cost([depot] + route + [depot])

    def simulated_annealing(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        return SimulatedAnnealing.fit(self, [depot] + cities + [depot])

    def genetic_algorithm(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        fittest = GeneticAlgorithm.fit(self, [depot] + cities + [depot])

        return fittest, self.cost(fittest)


class TravellingSalesmanTimeWindows(TravellingSalesman, CompressedAnnealing):
    class Traits(TravellingSalesman.Traits, CompressedAnnealing.Traits):
        class Fitness(TravellingSalesman.Traits.Fitness):
            def inverse_cost(self, individual):
                c = 0.5 * self.cost(individual) + 0.5 * self.penalty(individual)

                return 1.0 / c

            def unweighted_mst(self, individual):
                v = len(individual) - 1

                c = 0.5 * self.cost(individual) + 0.5 * self.penalty(individual)

                return ((v * v) - v + 1) / c

            def weighted_mst(self, individual):
                c = 0.5 * self.cost(individual) + 0.5 * self.penalty(individual)

                return self.heuristic(individual) / c

        class Service:
            pass

        class Timewindow:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def partial_cost(self, a, b):
        return self.service(a) + self.metric(a, b)

    def cost(self, route):
        return sum([
            self.partial_cost(route[i], route[i + 1])
            for i in range(len(route) - 1)
        ])

    def partial_penalty(self, arrival, a, b):
        arrival += self.partial_cost(a, b)

        beg, end = self.timewindow(b)

        start_of_service = max(arrival, beg)

        penalty = max(0, start_of_service + self.service(b) - end)

        return arrival, penalty

    def penalty(self, route):
        arrival, penalty = 0, 0

        for i in range(len(route) - 1):
            arrival, p = self.partial_penalty(arrival, route[i], route[i + 1])
            penalty += p

        return penalty

    def compressed_annealing(self, *args, **kwargs):
        depot, cities = args[0], args[1]

        fittest = CompressedAnnealing.fit(self, [depot] + cities + [depot])

        return fittest, self.cost(fittest)
