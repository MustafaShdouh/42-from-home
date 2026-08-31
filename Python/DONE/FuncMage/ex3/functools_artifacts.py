from functools import reduce, partial, lru_cache, singledispatch
from operator import mul, add
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    number = 0

    if not spells:
        return number

    try:
        new_spells = list(map(int, spells))
    except ValueError:
        raise ValueError("Invalid Input.")

    match operation.lower().strip():
        case 'add':
            number = reduce(add, new_spells)
            return number
        case 'multiply':
            number = reduce(mul, new_spells)
            return number
        case 'max':
            number = reduce(max, new_spells)
            return number
        case 'min':
            number = reduce(min, new_spells)
            return number
        case _:
            raise ValueError("Unknown or Invalid Operator.")
    return number


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    flame_enchantment = partial(base_enchantment, 50, "Fire")
    water_enchantment = partial(base_enchantment, 50, "Water")
    earth_enchantment = partial(base_enchantment, 50, "Earth")
    return {
        "flame": flame_enchantment,
        "water": water_enchantment,
        "earth": earth_enchantment
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    n = int(n)
    if n < 2:
        return n

    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def cast_spell(arg: Any) -> str:
        return "Unknown spell type"

    @cast_spell.register
    def _(arg: str) -> str:
        return f"Enchantment {arg}"

    @cast_spell.register
    def _(arg: int) -> str:
        return f"Damage spell: {arg} damage"

    @cast_spell.register
    def _(arg: list) -> str:
        return f"Multi-cast: {len(arg)} spells"

    return cast_spell


def enchantment(power: int, element: str, target: str) -> str:
    return f"Enchanted {target} with {power} {element} power!"


def main():
    print("Testing spell_reducer:")
    try:
        out = spell_reducer([1, 2, 3, 4], 'add')
        print(out)
    except ValueError as e:
        print(e)

    print("\nTesting partial_enchanter:")
    partial_dictionary = partial_enchanter(enchantment)

    cast_flame = partial_dictionary["flame"]
    cast_water = partial_dictionary["water"]
    cast_earth = partial_dictionary["earth"]

    print(cast_flame("Sword"))
    print(cast_water("Scepter"))
    print(cast_earth("Shield"))

    print("\nTesting memoized fibonacci:")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(f"Fib(100): {memoized_fibonacci(100)}")
    print("\nCache Statistics:")
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(['fireball', 'heal', 'shield']))
    print(dispatcher(3.14))


if __name__ == "__main__":
    main()
