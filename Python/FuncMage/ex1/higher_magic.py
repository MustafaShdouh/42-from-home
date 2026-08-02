from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        str1 = spell1(target, power)
        str2 = spell2(target, power)
        return str1, str2
    return combined_spell


def power_amplifier(base_spell: Callable, multiplied: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplied)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def conditional_function(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional_function


def spell_sequence(spells: list[Callable]) -> Callable:
    def spell_casting(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return spell_casting


def main():
    test_values = [8, 18, 11]
    test_targets = ["Dragon", "Goblin", "Wizard", "Knight"]
    print("Testing spell_combinder:")
    combined =


if __name__ == "__main__":
    main()
