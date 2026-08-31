from collections.abc import Callable
from data_generator import FuncMageDataGenerator as gen


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    if not (callable(spell1) and callable(spell2)):
        raise TypeError("Object is not callable.")

    def combined_spell(target: str, power: int) -> tuple[str, str]:
        if int(power) <= 0:
            raise ValueError("Power can't be zero or negative")
        str1 = spell1(target, int(power))
        str2 = spell2(target, int(power))
        return str1, str2

    return combined_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    if multiplier <= 0:
        raise ValueError("cannot amplify with 0 or negative number.")
    if not callable(base_spell):
        raise TypeError("Object is not callable.")

    def amplified(target: str, power: int) -> str:
        if int(power) <= 0:
            raise ValueError("Power can't be zero or negative")
        return base_spell(target, int(power) * int(multiplier))

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not (callable(condition) and callable(spell)):
        raise TypeError("Object is not callable.")

    def conditional_function(target: str, power: int) -> str:
        if condition(str(target), int(power)):
            return spell(str(target), int(power))
        return "Spell fizzled"

    return conditional_function


def spell_sequence(spells: list[Callable]) -> Callable:
    for spell in spells:
        if not callable(spell):
            raise TypeError("Object is not callable.")

    def spell_casting(target: str, power: int) -> list[str]:
        if int(power) <= 0:
            raise ValueError("Power can't be zero or negative")
        return [spell(str(target), int(power)) for spell in spells]

    return spell_casting


def heal(target: str, power: int) -> str:
    return f"{target!s} healed for {power} HP."


def fireball(target: str, power: int) -> str:
    return f"{target!s} casted fireball for {power} damage."


def zap(target: str, power: int) -> str:
    return f"{target!s} was zapped for {power} damage."


def poison(target: str, power: int) -> str:
    return f"{target!s} was poisoned for {power} damage."


def is_powerful(target: str, power: int) -> bool:
    return not int(power) <= 0


def main():
    random_mages = gen.generate_mages(1)

    test_subject = random_mages[0]
    dynamic_target = test_subject["name"]
    dynamic_power = test_subject["power"]

    print(
        f"Dynamically testing on {dynamic_target} "
        f"(Generated Power: {dynamic_power})"
    )

    print("\nTesting spell_combiner:")
    try:
        combined = spell_combiner(fireball, heal)
        print(combined(dynamic_target, dynamic_power))
    except (ValueError, TypeError) as e:
        print(e)

    print("\nTesting power_amplifier (10x multiplier):")
    try:
        amplified = power_amplifier(fireball, 10)
        print(amplified(dynamic_target, dynamic_power))
    except ValueError as e:
        print(e)

    print("\nTesting conditional_caster:")
    try:
        condition = conditional_caster(is_powerful, fireball)
        print(condition(dynamic_target, dynamic_power))
    except ValueError as e:
        print(e)

    print("\nTesting spell_sequence:")
    try:
        spell_list = [fireball, zap, poison]
        sequence = spell_sequence(spell_list)

        results = sequence(dynamic_target, dynamic_power)
        for r in results:
            print(f"{r}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
