
from core import Trait


class Greet(Trait):
    TRAITS = ['greet', ]

    class Greet:
        def greetings(self):
            return f'Greetings {self.name}'

        def hello(self):
            return f'Hello {self.name}'

        def good_evening(self):
            return f'Good evening {self.name}'

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name

    def __call__(self):
        return self.greet()


if __name__ == '__main__':
    greet = Greet('Vasilis', greet='hello')

    print(greet())

    greet.greet = 'greetings'

    print(greet())

    greet.greet = Greet.Greet.good_evening

    print(greet())
