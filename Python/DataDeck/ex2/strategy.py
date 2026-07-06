from abc import ABC, abstractmethod

from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> str:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}'"
                " for this normal strategy"
            )
        return creature.attack()


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> str:
        if isinstance(creature, TransformCapability):
            lines: list[str] = []
            lines.append(creature.transform())
            lines.append(creature.attack())
            lines.append(creature.revert())
            return "\n".join(lines)
        raise InvalidStrategyError(
            f"Invalid Creature '{creature.name}'"
            " for this aggressive strategy"
        )


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> str:
        if isinstance(creature, HealCapability):
            lines: list[str] = []
            lines.append(creature.attack())
            lines.append(creature.heal())
            return "\n".join(lines)
        raise InvalidStrategyError(
            f"Invalid Creature '{creature.name}'"
            " for this defensive strategy"
        )
