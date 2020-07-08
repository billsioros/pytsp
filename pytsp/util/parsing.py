
from abc import ABC, abstractmethod, abstractproperty
from csv import reader
from pathlib import Path
from re import match


class Parser(ABC):
    def __init__(self, filename):
        super().__init__()

        self.file = Path(filename)

        assert self.file.is_file(), f'`{filename}` is not a file'
        assert match(self.extension, self.file.suffix[1:]), f'Unexpected extension `{self.file.suffix}`'

    @abstractproperty
    def extension(self):
        return ''

    @abstractmethod
    def __call__(self):
        return set(), {}

class List(Parser):
    @property
    def extension(self):
        return r'txt'

    def __call__(self):
        points = set()

        with self.file.open() as stream:
            for line, point in enumerate(stream.readlines()):
                if match(r'^\([0-9\.]+\s*,\s*[0-9\.]+\)$', point):
                    points.add(eval(point))
                else:
                    raise ValueError(f'{self.file}:{line + 1:02d}: Failed to evaluate entry `{point}`')

        return points, {}


class Matrix(Parser):
    @property
    def extension(self):
        return r'tsv'

    def __call__(self):
        points, distances = set(), {}

        with self.file.open() as stream:
            try:
                stream.seek(0)
                for line, entry in enumerate(reader(stream, dialect='excel-tab')):
                    point_a, point_b, distance = entry[0], entry[1], entry[2]

                    for point in [point_a, point_b]:
                        if not match(r'^\([0-9\.]+\s*,\s*[0-9\.]+\)$', point):
                            raise ValueError(f'{self.file}:{line + 1:02d}: Failed to evaluate entry `{point}`')

                    point_a, point_b = eval(point_a), eval(point_b)

                    points = points.union({point_a, point_b})

                    if point_a not in distances:
                        distances[point_a] = {}

                    try:
                        distances[point_a][point_b] = int(distance)
                    except:
                        raise ValueError(f'{self.file}:{line + 1:02d}: Failed to evaluate entry `{distance}`')
            except Exception as e:
                raise e
                raise ValueError(f'`{self.file}` is malformed')

        return points, distances
