
from functools import partial


class TraitMeta(type):
    def __new__(cls, name, bases, attrs):
        for trait in attrs.get('TRAITS', []):
            field = f'_{trait}'
            if trait in attrs or field in attrs:
                continue

            def getter(self, field=field):
                return partial(getattr(self, field), self)

            def setter(self, value, trait=trait, field=field):
                if value is None or callable(value):
                    setattr(self, field, value)
                elif isinstance(value, str):
                    value = value.lower().replace("-", "_")
                    value = getattr(getattr(self, trait.title()), value)
                    setattr(self, field, value)
                elif isinstance(value, list):
                    def value(v1, v2): return value[v1][v2]
                    setattr(self, field, value)
                else:
                    raise TypeError(f'Unexpected type {type(value)}')

            attrs[trait] = property(getter, setter)

        return super().__new__(cls, name, bases, attrs)


class Trait(object, metaclass=TraitMeta):
    TRAITS = []

    def __init__(self, *args, **kwargs):
        super().__init__()

        for trait in self.TRAITS:
            if trait in kwargs:
                setattr(self, trait, kwargs[trait])
