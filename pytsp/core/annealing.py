
from logging import getLogger
from math import exp, log
from random import random

from pytsp.core.util import Model


class AnnealingMixin(Model):
    class Traits(Model.Traits):
        class Mutate:
            pass

        class Cost:
            pass

    def acceptance_probability(self, current_cost, candidate_cost, temperature):
        if candidate_cost < current_cost:
            return 1
        else:
            return exp((current_cost - candidate_cost) / temperature)


class SimulatedAnnealing(AnnealingMixin):
    class Traits(AnnealingMixin.Traits):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.MAX_TEMPERATURE = kwargs.get('max_temperature', 100000)
        self.COOLING_RATE = kwargs.get('cooling_rate', 0.000625)
        self.MAX_ITERATIONS = kwargs.get('max_iterations', 10000)

        self.logger = getLogger(self.__class__.__name__)

    def fit(self, initial):
        current, best = initial, initial
        current_cost = best_cost = self.cost(current)

        temperature, iteration = self.MAX_TEMPERATURE, 0
        while iteration < self.MAX_ITERATIONS and temperature > 1:
            self.logger.info(
                'Iteration: %04d, Temperature: %09.3f' % (
                    iteration,
                    temperature
                )
            )
            self.logger.info(
                'Best: %s, Cost: %07.2f' % (
                    best,
                    best_cost
                )
            )

            candidate = self.mutate(current)
            candidate_cost = self.cost(candidate)

            if self.acceptance_probability(current_cost, candidate_cost, temperature) > random():
                current, current_cost = candidate, candidate_cost

            if current_cost < best_cost:
                best, best_cost = current, current_cost
                temperature, iteration = self.MAX_TEMPERATURE, 0

            iteration += 1
            temperature *= (1 - self.COOLING_RATE)

        return best, best_cost


class CompressedAnnealing(AnnealingMixin):
    class Traits(AnnealingMixin.Traits):
        class Penalty:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.COOLING_RATE = kwargs.get('cooling_rate', 0.05)
        self.ACCEPTANCE_RATIO = kwargs.get('acceptance_ratio', 0.94)
        self.INITIAL_PRESSURE = kwargs.get('initial_pressure', 0)
        self.COMPRESSION_RATE = kwargs.get('compression_rate', 0.06)
        self.PRESSURE_CAP_RATIO = kwargs.get('pressure_cap_ratio', 0.9999)
        self.ITERATIONS_PER_TEMPERATURE = kwargs.get(
            'iterations_per_temperature',
            1000
        )
        self.MINIMUM_TEMPERATURE_CHANGES = kwargs.get(
            'minimum_temperature_changes',
            100
        )
        self.IDLE_TEMPERATURE_CHANGES = kwargs.get(
            'idle_temperature_changes',
            75
        )
        self.TRIAL_ITERATIONS = kwargs.get('trial_iterations', 30000)
        self.TRIAL_NEIGHBOR_PAIRS = kwargs.get('trial_neighbor_pairs', 5000)

        self.logger = getLogger(self.__class__.__name__)

    def calibrate(self, initial):
        dv, self.MAX_PRESSURE = 0, 0
        for r in range(0, 2 * self.TRIAL_NEIGHBOR_PAIRS):
            self.logger.info(
                'Maximum Pressure: %09.3f' % (
                    self.MAX_PRESSURE,
                )
            )

            n1, n2 = self.mutate(initial), self.mutate(initial)

            c1, p1 = self.cost(n1), self.penalty(n1)
            c2, p2 = self.cost(n2), self.penalty(n2)

            e1 = c1 + self.INITIAL_PRESSURE * p1
            e2 = c2 + self.INITIAL_PRESSURE * p2

            dv += abs(e2 - e1)

            p1 = (c1 / p1) * (
                self.PRESSURE_CAP_RATIO /
                (1.0 - self.PRESSURE_CAP_RATIO)
            )
            p2 = (c2 / p2) * (
                self.PRESSURE_CAP_RATIO /
                (1.0 - self.PRESSURE_CAP_RATIO)
            )

            self.MAX_PRESSURE = max([self.MAX_PRESSURE, p1, p2])

        self.MAX_TEMPERATURE = dv / log(1 / self.ACCEPTANCE_RATIO)

        accepted = 0
        while True:
            self.logger.info(
                'Maximum Temperature: %013.3f' % (
                    self.MAX_TEMPERATURE,
                )
            )

            accepted = 0

            current = initial
            current_cost = self.cost(current)
            current_penalty = self.penalty(current)

            for i in range(0, self.TRIAL_ITERATIONS):
                candidate = self.mutate(current)

                candidate_cost = self.cost(candidate)
                candidate_penalty = self.penalty(candidate)

                current_fit = current_cost + self.INITIAL_PRESSURE * current_penalty
                candidate_fit = candidate_cost + self.INITIAL_PRESSURE * candidate_penalty

                if self.acceptance_probability(current_fit, candidate_fit, self.MAX_TEMPERATURE) > random():
                    current = candidate
                    current_cost = candidate_cost
                    current_penalty = candidate_penalty

                    accepted += 1

            if accepted / self.TRIAL_ITERATIONS >= self.ACCEPTANCE_RATIO:
                break

            self.MAX_TEMPERATURE *= 1.5

    def fit(self, initial):
        if not hasattr(self, 'MAX_TEMPERATURE') or not hasattr(self, 'MAX_PRESSURE'):
            self.calibrate(initial)

        current = best = initial

        current_cost = best_cost = self.cost(initial)
        current_penalty = best_penalty = self.penalty(initial)

        pressure, temperature = self.INITIAL_PRESSURE, self.MAX_TEMPERATURE
        k, idle = -1, -1
        while True:
            k += 1
            idle += 1

            self.logger.info(
                'Temperature: %013.3f, Pressure: %09.3f' % (
                    temperature,
                    pressure
                )
            )
            self.logger.info(
                'Best: %s, Cost: %07.2f, Penalty: %07.2f' % (
                    best,
                    best_cost,
                    best_penalty
                )
            )

            for i in range(0, self.ITERATIONS_PER_TEMPERATURE):
                candidate = self.mutate(current)

                candidate_cost = self.cost(candidate)
                candidate_penalty = self.penalty(candidate)

                current_fit = current_cost + pressure * current_penalty
                candidate_fit = candidate_cost + pressure * candidate_penalty

                if self.acceptance_probability(current_fit, candidate_fit, temperature) > random():
                    current = candidate
                    current_cost = candidate_cost
                    current_penalty = candidate_penalty

                if current_penalty <= best_penalty and current_cost < best_cost:
                    best = current
                    best_cost = current_cost
                    best_penalty = current_penalty

                    idle = 0

            if k >= self.MINIMUM_TEMPERATURE_CHANGES and idle >= self.IDLE_TEMPERATURE_CHANGES:
                break

            temperature *= (1 - self.COOLING_RATE)
            pressure = self.MAX_PRESSURE * (
                1.0 - (
                    (self.MAX_PRESSURE - self.INITIAL_PRESSURE) / self.MAX_PRESSURE
                ) * exp(-1.0 * self.COMPRESSION_RATE * k)
            )

        return best
