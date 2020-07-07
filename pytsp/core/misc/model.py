
from functools import partial
from inspect import getmembers, isclass


class Meta(type):
    def __new__(cls, name, bases, attrs):
        try:
            traits = filter(
                lambda trait: not trait[0].startswith('__'),
                getmembers(attrs.get('Traits'), predicate=isclass)
            )
        except:
            raise AttributeError(f'No `Traits` meta directive')

        for trait_name, trait_type in traits:
            method = trait_name.lower()
            field = f'_{method}'

            if field in attrs or method in attrs:
                continue

            def getter(self, field=field):
                return partial(getattr(self, field), self)

            def setter(self, value, trait_name=trait_name, trait_type=trait_type, field=field):
                if callable(value):
                    setattr(self, field, value)
                elif isinstance(value, str):
                    value = getattr(trait_type, value)
                    setattr(self, field, value)
                else:
                    raise TypeError(
                        f'Unexpected `{trait_name}` type {type(value)}')

            attrs[method] = property(getter, setter)

        return super().__new__(cls, name, bases, attrs)


class Model(object, metaclass=Meta):
    class Traits:
        pass

    def __init__(self, *args, **kwargs):
        super().__init__()

        for trait, _ in getmembers(self.Traits, predicate=isclass):
            trait = trait.lower().replace('-', '_')
            if trait in kwargs:
                setattr(self, trait, kwargs[trait])
