from django_handy.objs import classproperty


class Members:
    # noinspection PyPep8Naming
    @classproperty
    def ALL(self):
        return tuple(
            v for k, v in self.__dict__.items()
            if not k.startswith('__') and isinstance(v, str)
        )

    # noinspection PyPep8Naming
    @classproperty
    def CHOICES(self):
        return Choices(*self.ALL)


class Choices:
    def __init__(self, *choices):
        self._map = {}
        self._choices = ()
        for choice in choices:
            if isinstance(choice, (list, tuple)):
                db_value, human_name = choice
            else:
                db_value, human_name = (choice, choice)

            self._map[db_value] = human_name
            self._choices += ((db_value, human_name),)

    def __len__(self):
        return len(self._choices)

    def __iter__(self):
        return iter(self._choices)

    def __getitem__(self, key):
        return self._map[key]
