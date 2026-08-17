import functools
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    number = 0
    if operation == 'add':
        number = functools.reduce(lambda x, y: operator.add(x, y), spells)
    elif operation == 'multiply':
        number = functools.reduce(lambda x, y: operator.mul(x, y), spells)
    elif operation == 'max':
        number = functools.reduce(lambda x, y: operator.gt(x, y), spells)
    return number

out = spell_reducer([1, 2, 3], "max")
print(out)
