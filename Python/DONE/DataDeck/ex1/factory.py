from ex0.creature import Creature
from ex0.factory import CreatureFactory


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        from ex1.creatures import Sproutling
        return Sproutling()

    def create_evolved(self) -> Creature:
        from ex1.creatures import Bloomelle
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        from ex1.creatures import Shiftling
        return Shiftling()

    def create_evolved(self) -> Creature:
        from ex1.creatures import Morphagon
        return Morphagon()
