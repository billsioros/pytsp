"""
pytsp - The Travelling Salesman (with Time Windows)
----

>>> from random import seed, uniform
>>> from core import TravellingSalesman

>>> x_axis, y_axis = (-50, +50), (-50, +50)

>>> cities = [
    (uniform(x_axis[0], x_axis[1]), uniform(y_axis[0], y_axis[1]))
    for i in range(10)
]

>>> tsp = TravellingSalesman(metric='euclidean')
>>> depot, cities = cities[0], cities[1:]

>>> route, cost = tsp.nearest_neighbor(depot, cities)
"""

__author__ = 'Vasileios Sioros (billsioros)'
__copyright__ = 'Copyright 2020, Vasileios Sioros (billsioros)'
__credits__ = [
    'Vasileios Sioros (billsioros)',
]
__license__ = 'MIT License'
__version__ = '1.0'
__maintainer__ = 'Vasileios Sioros'
__email__ = 'billsioros97@gmail.com'
__status__ = 'Development'

__all__ = [
    'AnnealingMixin',
    'CompressedAnnealing',
    'SimulatedAnnealing',
    'GeneticAlgorithm',
    'Model',
    'cached',
    'jarvis',
    'TravellingSalesman',
    'TravellingSalesmanTimeWindows'
]

from pytsp.core import (AnnealingMixin, CompressedAnnealing, GeneticAlgorithm,
                        Model, SimulatedAnnealing, TravellingSalesman,
                        TravellingSalesmanTimeWindows, cached, jarvis)
