import enum


class ChoiceMeta(enum.EnumMeta):
    def __contains__(cls, other):
        if isinstance(other, cls):
            value = other
        else:
            try:
                value = cls(other)
            except ValueError:
                return False
        return super().__contains__(value)


class Choice(enum.Enum, metaclass=ChoiceMeta):

    def __eq__(self, other):
        if not isinstance(other, Choice):
            try:
                other = self.__class__(other)
            except ValueError:
                return False
        return other.value == self.value

    def is_valid(self, choice_value):
        return any(
            c.value == choice_value for c in self.choices
        )


"""
from pentaquark.properties.choices import Choice

class MyChoice(Choice):
    ONE = 1
    TWO = 2

assert MyChoice.ONE in MyChoice
assert 1 in MyChoice
assert 10 not in MyChoice

assert MyChoice.ONE != MyChoice.TWO
assert 1 == MyChoice.ONE
assert 2 != MyChoice.ONE
"""
