from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    """Run a tournament where each opponent fights every other."""
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                factory_a, strategy_a = opponents[i]
                factory_b, strategy_b = opponents[j]
                creature_a = factory_a.create_base()
                creature_b = factory_b.create_base()
                print("* Battle *")
                print(creature_a.describe())
                print("vs.")
                print(creature_b.describe())
                print("now fight!")
                print(strategy_a.act(creature_a))
                print(strategy_b.act(creature_b))
    except InvalidStrategyError as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    tournaments: list[
        tuple[str, list[tuple[CreatureFactory, BattleStrategy]]]
    ] = [
        (
            "Tournament 0 (basic)",
            [
                (flame_factory, normal),
                (healing_factory, defensive),
            ],
        ),
        (
            "Tournament 1 (error)",
            [
                (flame_factory, aggressive),
                (healing_factory, defensive),
            ],
        ),
        (
            "Tournament 2 (multiple)",
            [
                (aqua_factory, normal),
                (healing_factory, defensive),
                (transform_factory, aggressive),
            ],
        ),
    ]

    for name, opponents in tournaments:
        print(name)
        print(f"[ {format_opponents(opponents)} ]")
        battle(opponents)


def format_opponents(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> str:
    """Format opponent list for display."""
    labels: list[str] = []
    for factory, strategy in opponents:
        factory_name = get_factory_label(factory)
        strategy_name = get_strategy_label(strategy)
        labels.append(f"({factory_name}+{strategy_name})")
    return ", ".join(labels)


def get_factory_label(factory: CreatureFactory) -> str:
    """Get a display label for a factory."""
    if isinstance(factory, FlameFactory):
        return "Flameling"
    if isinstance(factory, AquaFactory):
        return "Aquabub"
    if isinstance(factory, HealingCreatureFactory):
        return "Healing"
    if isinstance(factory, TransformCreatureFactory):
        return "Transform"
    return "Unknown"


def get_strategy_label(strategy: BattleStrategy) -> str:
    """Get a display label for a strategy."""
    if isinstance(strategy, NormalStrategy):
        return "Normal"
    if isinstance(strategy, AggressiveStrategy):
        return "Aggressive"
    if isinstance(strategy, DefensiveStrategy):
        return "Defensive"
    return "Unknown"


if __name__ == "__main__":
    main()
