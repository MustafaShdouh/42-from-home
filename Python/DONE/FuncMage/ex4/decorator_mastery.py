import time
import functools
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Spell completed in {execution_time:.3f} seconds")

        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get('power', args[-1] if args else 0)

            if power < min_power:
                return "Insufficient power for this spell"

            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying... (attempt {attempt}/"
                              f"{max_attempts})")
                    else:
                        print("Spell casting failed after "
                              f"{max_attempts} attempts")
                        raise e
            return None
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(char.isalpha() or char.isspace() for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main():
    print("Testing spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.1)
        return "Fireball cast!"

    print(f"Result: {fireball()}\n")

    print("Testing retrying spell...")

    @retry_spell(max_attempts=3)
    def waaaaagh():
        raise ValueError("Waaaaaaagh spelled !")

    try:
        waaaaagh()
    except ValueError as e:
        print(e)

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("Jo"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
