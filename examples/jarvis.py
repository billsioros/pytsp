
from random import uniform

import matplotlib.pyplot as plt

from pytsp import jarvis

if __name__ == '__main__':
    """
    Visualizing the Convex Hull of a given set of points
    with the help of the Jarvis March Algorithm
    """

    NUMBER, X_AXIS, Y_AXIS = 5, [-50, +50], [-50, +50]

    assert len(X_AXIS) == 2 and X_AXIS[0] < X_AXIS[1]
    assert len(Y_AXIS) == 2 and Y_AXIS[0] < Y_AXIS[1]

    pxs = [uniform(X_AXIS[0], X_AXIS[1]) for _ in range(NUMBER)]
    pys = [uniform(Y_AXIS[0], Y_AXIS[1]) for _ in range(NUMBER)]

    points = [(x, y) for x, y in zip(pxs, pys)]

    convex_hull = jarvis(points)

    cxs = [point[0] for point in convex_hull]
    cys = [point[1] for point in convex_hull]

    plt.plot(pxs, pys, 'k.', markersize=12)
    plt.plot(cxs + [convex_hull[0][0]], cys + [convex_hull[0][1]], 'b-')
    plt.plot(cxs, cys, 'm.', markersize=12)

    plt.title(
        f'The {len(convex_hull)} points of the Convex Hull of {NUMBER} randomly generated points')
    plt.grid()
    plt.xlim([X_AXIS[0], X_AXIS[1]])
    plt.xlim([Y_AXIS[0], Y_AXIS[1]])
    plt.axis('equal')
    plt.show()
