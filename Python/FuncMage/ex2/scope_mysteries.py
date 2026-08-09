from collections.abc import Callable


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable:
    base_power = initial_power

    def power_accumulator(power: int) -> int:
        nonlocal base_power
        base_power += power
        return base_power
    return power_accumulator

