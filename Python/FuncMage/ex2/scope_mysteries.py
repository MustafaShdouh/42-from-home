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


def main():
    print("Testing mage_counter:")
    count = mage_counter()
    for i in range(3):
        print(f"* {count()}")
    try:
        print("Testing spell_accumulator:")
        accumulator = spell_accumulator(0)
        for i in range(3):
            print(f"{i+1}. {accumulator(10)}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
