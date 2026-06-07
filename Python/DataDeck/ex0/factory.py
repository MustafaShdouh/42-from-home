from abc import ABC, abstractmethod

from ex0.creature import Creature


class CreatureFactory(ABC):
    """Abstract factory for creating Creature families."""

    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    """Factory for the Fire family of Creatures."""

    def create_base(self) -> Creature:
        from ex0.creature import Flameling
        return Flameling()

    def create_evolved(self) -> Creature:
        from ex0.creature import Pyrodon
        return Pyrodon()


class AquaFactory(CreatureFactory):
    """Factory for the Water family of Creatures."""

    def create_base(self) -> Creature:
        from ex0.creature import Aquabub
        return Aquabub()

    def create_evolved(self) -> Creature:
        from ex0.creature import Torragon
        return Torragon()
