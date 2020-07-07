
from functools import wraps


def plot(method):
    from matplotlib import pyplot as plt
    from pathlib import Path
    from math import modf

    @wraps(method)
    def wrapper(ctx, **kwargs):
        tsp = ctx.obj['class'](**{
            'metric': ctx.obj['metric'],
            'service': ctx.obj.get('service', None),
            'timewindow': ctx.obj.get('timewindow', None),
            **kwargs
        })

        route, cost = getattr(tsp, method.__name__)(
            ctx.obj['depot'], ctx.obj['cities']
        )

        figure = plt.figure()

        plt.title(
            f'{method.__name__.replace("_", " ").title()} '
            f'(Cities: {len(route) - 1}, Cost: {cost:07.2f})'
        )

        dx, dy = route[0]
        xs, ys = [c[0] for c in route[1:-1]], [c[1] for c in route[1:-1]]

        plt.scatter(xs, ys, c='blue', label='Cities')

        plt.scatter([dx], [dy], c='red', label='Depot')
        plt.text(
            dx - 0.5 if dx < 0 else dx + 0.5,
            dy - 0.5 if dy < 0 else dy + 0.5,
            f'({dx:05.2f}, {dy:5.2f})', fontsize=8
        )

        plt.plot([dx] + xs + [dx], [dy] + ys + [dy], 'k--', label='Route')

        if ctx.obj['graph'] is True:
            for cx, cy in zip(xs, ys):
                plt.text(
                    cx - 0.5 if cx < 0 else cx + 0.5,
                    cy - 0.5 if cy < 0 else cy + 0.5,
                    f'({cx:05.2f}, {cy:5.2f})', fontsize=6
                )

            plt.axis('off')
        else:
            plt.legend()

        plt.xlim(
            (ctx.obj['x_axis'][0] - 1) * 1.1,
            (ctx.obj['x_axis'][1] + 1) * 1.1
        )
        plt.ylim(
            (ctx.obj['y_axis'][0] - 1) * 1.1,
            (ctx.obj['y_axis'][1] + 1) * 1.1
        )
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.grid()

        if ctx.obj['path'] is not None:
            path = Path(ctx.obj['path'])

            f, i = modf(cost)
            f, i = int(f * 100), int(i)

            if path.suffix == '':
                folder = path
                name = f'{method.__name__}_{len(route) - 1:03d}_{i:04d}_{f:03d}.png'
            else:
                folder = path.parent
                name = path.name

            folder.mkdir(parents=True, exist_ok=True)

            figure.savefig(folder / name)
        else:
            plt.show()

        ctx.obj['cities'] = route[1:-1]

    return wrapper


def safe(method):
    from click import echo, style

    # @wraps(method)
    # def wrapper(*args, **kwargs):
    #     try:
    #         return method(*args, **kwargs)
    #     except Exception as e:
    #         name = method.__name__.replace("_", " ").title()
    #         echo(style(f"{name}: ", bold=True) + str(e))
    #         exit(1)

    return method
