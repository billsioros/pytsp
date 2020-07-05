
from inspect import getmembers, isfunction

from click import Choice, Tuple


class Dictionary(Choice):
    name = 'dictionary'

    def __init__(self, choices, case_sensitive=False):
        self.__choices = {}
        for k, v in choices.items():
            self.__choices[k.replace('_', '-')] = v

        super().__init__(
            sorted(self.__choices.keys()),
            case_sensitive=case_sensitive
        )

    def convert(self, value, param, ctx):
        value = value.replace('_', '-')
        value = super().convert(value, param, ctx)

        return self.__choices[value]

    def get_metavar(self, param):
        return '|'.join(self.choices)


class Timewindow(Tuple):
    name = 'timewindow'

    def __init__(self):
        super().__init__([float, float])

    def convert(self, value, param, ctx):
        hours, minutes = super().convert(value, param, ctx)

        if hours > 23:
            self.fail("Hours should be in the range [00, 23]", param, ctx)

        if minutes > 59:
            self.fail("Minutes should be in the range [00, 59]", param, ctx)

        return hours * 3600 + minutes * 60


class Trait(Choice):
    name = 'trait'

    def __init__(self, cls, case_sensitive=False):
        super().__init__(
            [
                name
                for name, _ in getmembers(cls, predicate=isfunction)
                if not name.startswith("_")
            ],
            case_sensitive=case_sensitive
        )

    def convert(self, value, param, ctx):
        return super().convert(value.replace('-', '_'), param, ctx)
