
from random import uniform

import matplotlib.pyplot as plt

from pytsp import TravellingSalesman

if __name__ == '__main__':
    x_axis, y_axis = (-50, +50), (-50, +50)

    cities = [
        (uniform(x_axis[0], x_axis[1]), uniform(y_axis[0], y_axis[1]))
        for i in range(10)
    ]

    depot, cities = cities[0], cities[1:]

    tsp = TravellingSalesman(metric='euclidean')

    route, cost = tsp.nearest_neighbor(depot, cities)

    plt.title(
        f'(Cities: {len(route) - 1}, Cost: {cost:07.2f})'
    )

    dx, dy = route[0]
    xs, ys = [c[0] for c in route[1:-1]], [c[1] for c in route[1:-1]]

    plt.scatter(xs, ys, c='blue', label='Cities')

    plt.scatter([dx], [dy], c='red', label='Depot')
    plt.text(
        dx - 0.5 if dx < 0 else dx + 0.5,
        dy - 0.5 if dy < 0 else dy + 0.5,
        f'({dx:05.2f}, {dy:5.2f})', fontsize=10
    )

    plt.plot([dx] + xs + [dx], [dy] + ys + [dy], 'k--', label='Route')

    plt.xlim((x_axis[0] - 1) * 1.1, (x_axis[1] + 1) * 1.1)
    plt.ylim((y_axis[0] - 1) * 1.1, (y_axis[1] + 1) * 1.1)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.grid()
    plt.legend()

    plt.show()
