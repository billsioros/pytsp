
import logging
from random import seed, uniform

import click

from pytsp.cli import Dictionary, Method, Timewindow, plot, safe
from pytsp.core import TravellingSalesman, TravellingSalesmanTimeWindows


@click.group()
@click.option(
    '-d', '--depot',
    type=click.Tuple([float, float]), default=(None, None),
    help='the depot'
)
@click.option(
    '-c', '--cities',
    type=click.INT, default=10,
    help='the number of cities',
    show_default=True
)
@click.option(
    '-m', '--metric',
    type=Method(TravellingSalesman.Traits.Metric), default='euclidean',
    help='the distance metric to be used',
    show_default=True
)
@click.option(
    '-x', '--x-axis', 'x_axis',
    type=click.Tuple([float, float]), default=[0, 50],
    help='the horizontal axis limits',
    show_default=True
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.Tuple([float, float]), default=[0, 50],
    help='the vertical axis limits',
    show_default=True
)
@click.option(
    '-s', '--random-seed', 'random_seed',
    type=click.INT, default=None,
    help='the random number generator seed'
)
@click.option(
    '-p', '--path',
    type=click.STRING, default=None,
    help='where to save the resulting figure file'
)
@click.option(
    '-l', '--logging-lvl', 'logging_lvl',
    type=Dictionary(logging._nameToLevel), default='CRITICAL',
    help='the logging level',
    show_default=True
)
@click.option(
    '-g', '--graph',
    is_flag=True, default=False, show_default=True,
    help='show a plain graph'
)
@click.pass_context
def cli(
    ctx,
    depot, cities, metric,
    x_axis, y_axis,
    random_seed, path, logging_lvl,
    graph
):
    """
    Visualization of various `Travelling Salesman` algorithms
    """

    if random_seed is not None:
        seed(random_seed)

    if depot != (None, None):
        cities -= 1

    cities = [
        (uniform(x_axis[0], x_axis[1]), uniform(y_axis[0], y_axis[1]))
        for i in range(cities)
    ]

    if depot == (None, None):
        depot, cities = cities[0], cities[1:]

    ctx.obj = {
        'depot': depot,
        'cities': cities,
        'metric': metric,
        'x_axis': x_axis,
        'y_axis': y_axis,
        'path': path,
        'graph': graph
    }

    logging.basicConfig(
        format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
        level=logging_lvl,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


@cli.group(chain=True)
@click.pass_context
def tsp(ctx, *args, **kwargs):
    """
    Various algorithms targeting the `Travelling Salesman` Problem
    """
    ctx.obj['class'] = TravellingSalesman


@cli.group(chain=True)
@click.option(
    '-s', '--service-time', 'service_time',
    type=click.Tuple([float, float]), default=(30, 60),
    help='the minimum and maximum service time of each city',
    show_default=True
)
@click.option(
    '-t', '--time-window', 'time_window',
    type=click.Tuple([Timewindow(), Timewindow()]), default=((7, 0), (8, 15)),
    help='the minimum and maximum time window values',
    show_default=True
)
@click.pass_context
def tsptw(ctx, service_time, time_window, *args, **kwargs):
    """
    Various algorithms targeting the `Travelling Salesman with Time Windows` Problem
    """

    def service(self, city):
        return uniform(service_time[0], service_time[1])

    def timewindow(self, city):
        return timewindow.cache[round(city[0], 1), round(city[1], 1)]

    depot = ctx.obj['depot']

    timewindow.cache = {}
    timewindow.cache[round(depot[0], 1), round(depot[1], 1)] = (0, 0)
    for city in ctx.obj['cities']:
        beg = uniform(time_window[0], time_window[1])
        end = uniform(beg + service_time[0], time_window[1])

        timewindow.cache[round(city[0], 1), round(city[1], 1)] = (beg, end)

    ctx.obj['class'] = TravellingSalesmanTimeWindows
    ctx.obj['service'] = service
    ctx.obj['timewindow'] = timewindow


for group in [tsp, tsptw]:
    @group.command()
    @click.pass_context
    @safe
    @plot
    def nearest_neighbor(*args, **kwargs):
        pass

for group in [tsp, tsptw]:
    @group.command()
    @click.option(
        '-c', '--criterion',
        type=Method(TravellingSalesman.Traits.Criterion), default='eccentricity',
        help='the criterion for choosing which city to integrate next into the partial tour',
        show_default=True
    )
    @click.pass_context
    @safe
    @plot
    def convex_hull(*args, **kwargs):
        pass

for group in [tsp, tsptw]:
    @group.command()
    @click.pass_context
    @safe
    @plot
    def opt_2(*args, **kwargs):
        pass


for group in [tsp, tsptw]:
    @group.command()
    @click.option(
        '-m', '--mutate',
        type=Method(TravellingSalesman.Traits.Mutate), default='shift-1',
        help='the mutation function to be used',
        show_default=True
    )
    @click.option(
        '-t', '--max-temperature', 'max_temperature',
        type=click.FLOAT, default=100000,
        help='the maximum temperature',
        show_default=True
    )
    @click.option(
        '-c', '--cooling-rate', 'cooling_rate',
        type=click.FloatRange(0, 1), default=0.000625,
        help='the cooling rate',
        show_default=True
    )
    @click.option(
        '-i', '--max-iterations', 'max_iterations',
        type=click.INT, default=10000,
        help='the maximum number of iterations',
        show_default=True
    )
    @click.pass_context
    @safe
    @plot
    def simulated_annealing(*args, **kwargs):
        pass

for group in [tsptw]:
    @group.command()
    @click.option(
        '-m', '--mutate',
        type=Method(TravellingSalesman.Traits.Mutate), default='shift_1',
        help='the mutation function to be used',
        show_default=True
    )
    @click.option(
        '--cooling-rate', 'cooling_rate',
        type=click.FloatRange(0, 1), default=0.05,
        help='the cooling rate',
        show_default=True
    )
    @click.option(
        '--acceptance-ratio', 'acceptance_ratio',
        type=click.FloatRange(0, 1), default=0.94,
        help='the initial acceptance ratio',
        show_default=True
    )
    @click.option(
        '--initial-pressure', 'initial_pressure',
        type=click.FLOAT, default=0,
        help='the initial pressure',
        show_default=True
    )
    @click.option(
        '--compression-rate', 'compression_rate',
        type=click.FloatRange(0, 1), default=0.06,
        help='the compression rate',
        show_default=True
    )
    @click.option(
        '--pressure-cap-ratio', 'pressure_cap_ratio',
        type=click.FloatRange(0, 1), default=0.9999,
        help='the pressure cap ratio',
        show_default=True
    )
    @click.option(
        '--iterations-per-temperature', 'iterations_per_temperature',
        type=click.INT, default=1000,
        help='the number of iterations per temperature value',
        show_default=True
    )
    @click.option(
        '--minimum-temperature-changes', 'minimum_temperature_changes',
        type=click.INT, default=100,
        help='the minimum number of temperature changes that have to occur',
        show_default=True
    )
    @click.option(
        '--idle-temperature-changes', 'idle_temperature_changes',
        type=click.INT, default=75,
        help='the maximum number of idle temperature changes',
        show_default=True
    )
    @click.option(
        '--trial-iterations', 'trial_iterations',
        type=click.INT, default=30000,
        help='the number of trial iterations',
        show_default=True
    )
    @click.option(
        '--trial-neighbor-pairs', 'trial_neighbor_pairs',
        type=click.INT, default=5000,
        help='the number of trial neighbor pairs',
        show_default=True
    )
    @click.pass_context
    @safe
    @plot
    def compressed_annealing(*args, **kwargs):
        pass


for group in [tsp, tsptw]:
    @group.command()
    @click.option(
        '-m', '--mutate',
        type=Method(TravellingSalesman.Traits.Mutate), default='shift-1',
        help='the mutation function to be used',
        show_default=True
    )
    @click.option(
        '-c', '--crossover',
        type=Method(TravellingSalesman.Traits.Crossover), default='cut_and_stitch',
        help='the crossover function to be used',
        show_default=True
    )
    @click.option(
        '-s', '--select',
        type=Method(TravellingSalesman.Traits.Select), default='random_top_half',
        help='the selection function to be used',
        show_default=True
    )
    @click.option(
        '-h', '--heuristic',
        type=Method(TravellingSalesman.Traits.Heuristic), default='kruskal',
        help='the heuristic to be used in the calculation of the fitness',
        show_default=True
    )
    @click.option(
        '-f', '--fitness',
        type=Method(TravellingSalesman.Traits.Fitness), default='weighted_mst',
        help='the function determining the fitness of an individual',
        show_default=True
    )
    @click.option(
        '-p', '--mutation-probability', 'mutation_probability',
        type=click.FloatRange(0, 1), default=0.3,
        help='the probability of an individual mutating',
        show_default=True
    )
    @click.option(
        '-t', '--fitness-threshold', 'fitness_threshold',
        type=click.FloatRange(0, 1), default=0.65,
        help='the fitness threshold of acceptable solutions',
        show_default=True
    )
    @click.option(
        '-i', '--max-iterations', 'max_iterations',
        type=click.INT, default=1000,
        help='the maximum number of iterations',
        show_default=True
    )
    @click.option(
        '--population-size', 'population_size',
        type=click.INT, default=50,
        help='the size of the population',
        show_default=True
    )
    @click.pass_context
    @safe
    @plot
    def genetic_algorithm(*args, **kwargs):
        pass


if __name__ == '__main__':
    cli()
