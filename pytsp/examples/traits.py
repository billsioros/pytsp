
from pytsp import Model


class Greet(Model):
    class Traits:
        class Greet:
            def greetings(self, name):
                return f'Greetings {self.title}{name}'

            def hello(self, name):
                return f'Hello {self.title}{name}'

    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title


def good_evening(self, name):
    return f'Good evening {self.title}{name}'


if __name__ == '__main__':
    greet = Greet('Mr.', greet='hello')

    print(greet.greet('Sioros'))

    greet.title = 'Sir.'
    greet.greet = 'greetings'

    print(greet.greet('Vasileios'))

    greet.title = ''
    greet.greet = good_evening

    print(greet.greet('Vasilis'))
