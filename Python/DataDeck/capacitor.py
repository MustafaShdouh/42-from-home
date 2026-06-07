from ex0 import CreatureFactory
from ex1 import (
    HealCapability,
    TransformCapability,
    HealingCreatureFactory,
    TransformCreatureFactory,
)


def test_healing(factory: CreatureFactory) -> None:
    """Test Creatures with healing capability."""
    print("Testing Creature with healing capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    assert isinstance(base, HealCapability)
    print(base.heal())
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    assert isinstance(evolved, HealCapability)
    print(evolved.heal())


def test_transform(factory: CreatureFactory) -> None:
    """Test Creatures with transform capability."""
    print("Testing Creature with transform capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    assert isinstance(base, TransformCapability)
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    assert isinstance(evolved, TransformCapability)
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


def main() -> None:
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    test_healing(healing_factory)
    test_transform(transform_factory)


if __name__ == "__main__":
    main()
