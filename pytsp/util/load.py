
from abc import ABC, abstractmethod, abstractstaticmethod
from csv import reader
from pathlib import Path
from re import match


class Loader(ABC):
    def __init__(self, filename):
        super().__init__()

        self.file = Path(filename)

        assert self.file.is_file(), f'`{filename}` is not a file'
        assert match(self.extension(), self.file.suffix[1:]), f'Unexpected extension `{self.file.suffix}`'

    @abstractstaticmethod
    def extension():
        pass

    @abstractmethod
    def __call__(self):
        pass

class List(Loader):
    @staticmethod
    def extension():
        return r'txt'

    def __call__(self):
        entries = []

        with self.file.open() as stream:
            for line, entry in enumerate(stream.readlines()):
                if match(r'^\([\+\-0-9\.]+\s*,\s*[\+\-0-9\.]+\)$', entry):
                    entries.append(eval(entry))
                else:
                    raise ValueError(f'{self.file}:{line + 1:02d}: Failed to evaluate entry `{entry}`')

        return list(dict.fromkeys(entries))
