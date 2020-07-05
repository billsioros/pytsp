"""
pytsp - The Travelling Salesman (with Time Windows) in Python
----

>>> from random import seed, uniform
>>> from core import TravellingSalesman

>>> X_AXIS, Y_AXIS = (-50, +50), (-50, +50)

>>> cities = [
    (uniform(X_AXIS[0], X_AXIS[1]), uniform(Y_AXIS[0], Y_AXIS[1]))
    for i in range(10)
]

>>> tsp = TravellingSalesman(metric='euclidean')
>>> depot, cities = cities[0], cities[1:]

>>> route, cost = tsp.nearest_neighbor(depot, cities)
"""

__author__ = "Vasileios Sioros (billsioros)"
__copyright__ = "Copyright 2020, Vasileios Sioros (billsioros)"
__credits__ = [
    "Vasileios Sioros",
]
__license__ = "MIT License"
__version__ = "0.8"
__maintainer__ = "Vasileios Sioros"
__email__ = "billsioros97@gmail.com"
__status__ = "Development"

__all__ = [
    'AnnealingMixin',
    'CompressedAnnealing',
    'SimulatedAnnealing',
    'GeneticAlgorithm',
    'Trait',
    'cached',
    'jarvis',
    'TravellingSalesman',
    'TravellingSalesmanTimeWindows'
]

from pytsp.core import (AnnealingMixin, CompressedAnnealing, GeneticAlgorithm,
                  SimulatedAnnealing, Trait, TravellingSalesman,
                  TravellingSalesmanTimeWindows, cached, jarvis)
