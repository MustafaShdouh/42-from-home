from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    if not (callable(spell1) and callable(spell2)):
        raise TypeError("Object is not callable.")

    def combined_spell(target: str, power: int) -> tuple[str, str]:
        if power <= 0:
            raise ValueError("Power can't be zero or negative")
        str1 = spell1(target, power)
        str2 = spell2(target, power)
        return str1, str2

    return combined_spell


def power_amplifier(base_spell: Callable, multiplied: int) -> Callable:
    if multiplied <= 0:
        raise ValueError("cannot amplify with 0 or negative number.")
    if not callable(base_spell):
        raise TypeError("Object is not callable.")

    def amplified(target: str, power: int) -> str:
        if power <= 0:
            raise ValueError("Power can't be zero or negative")
        return base_spell(target, power * multiplied)

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not (callable(condition) and callable(spell)):
        raise TypeError("Object is not callable.")

    def conditional_function(target: str, power: int) -> str:
        if power <= 0:
            raise ValueError("Power can't be zero or negative")
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional_function


def spell_sequence(spells: list[Callable]) -> Callable:
    for spell in spells:
        if not callable(spell):
            raise TypeError("Object is not callable.")

    def spell_casting(target: str, power: int) -> list[str]:
        if power <= 0:
            raise ValueError("Power can't be zero or negative")
        return [spell(target, power) for spell in spells]

    return spell_casting


def heal(target: str, power: int) -> str:
    return f"{target} healed for {power} HP."


def fireball(target: str, power: int) -> str:
    return f"{target} casted fireballed for {power} damage."


def zap(target: str, power: int) -> str:
    return f"{target} was zapped for {power} damage."


def poison(target: str, power: int) -> str:
    return f"{target} was poisoned for {power} damage."


def is_powerful(target: str, power: int) -> bool:
    if power <= 0:
        return False
    return True


def main():
    print("Testing spell_combiner:")
    try:
        combined = spell_combiner(fireball, heal)
        print(combined("Dragon", 20))
    except (ValueError, TypeError) as e:
        print(e)

    print("\nTesting power_amplifier:")
    try:
        amplified = power_amplifier(fireball, 10)
        print(amplified("Wizard", 10))
    except ValueError as e:
        print(e)

    print("\nTesting conditional_caster:")
    try:
        condition = conditional_caster(is_powerful, fireball)
        print(condition("Goblin", 1))
    except ValueError as e:
        print(e)

    print("\nTesting spell_sequence:")
    try:
        spell_list = [fireball, zap, poison]
        sequence = spell_sequence(spell_list)
        print(sequence("Knight", 20))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
