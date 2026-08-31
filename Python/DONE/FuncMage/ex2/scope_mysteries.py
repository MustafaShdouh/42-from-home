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
        if power < 0:
            raise ValueError("Power can't be negative.")
        nonlocal base_power
        base_power += power
        return base_power
    return power_accumulator


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchantment_adder(item: str) -> str:
        return f"{enchantment_type} {item}"
    return enchantment_adder


def memory_vault() -> dict[str, Callable]:
    vault = {}

    def store(key, value):
        vault[key] = value

    def recall(key):
        return vault.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main():
    print("Testing mage_counter:")
    count = mage_counter()
    for i in range(3):
        print(f"* {count()}")

    try:
        print("\nTesting spell_accumulator:")
        accumulator = spell_accumulator(0)
        for i in range(3):
            print(f"{i+1}. {accumulator(10)}")
    except ValueError as e:
        print(e)

    print("\nTesting enchantment_factory:")
    flame_factory = enchantment_factory("Flaming")
    print(flame_factory("Sword"))
    print()

    print("Testing memory_vault:")
    vault = memory_vault()
    print("Storing the key '1' with the value 42")
    store_spell = vault['store']
    recall_spell = vault['recall']
    store_spell('1', 42)
    print({recall_spell('1')})


if __name__ == "__main__":
    main()
