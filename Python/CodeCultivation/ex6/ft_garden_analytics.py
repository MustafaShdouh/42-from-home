class Plant:
    class _Statistics:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def record_grows(self) -> None:
            self._grow_calls += 1

        def record_ages(self) -> None:
            self._age_calls += 1

        def record_shows(self) -> None:
            self._show_calls += 1

        def display(self) -> str:
            return (f"Stats: {self._grow_calls} grow, {self._age_calls} age, "
                    f"{self._show_calls} show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._height = float(height) if height >= 0 else 0.0
        self._age = age if age >= 0 else 0.0
        self._baseStats = self._Statistics()

    def grow(self, cm: float) -> None:
        self._height += cm
        self._baseStats.record_grows()

    def age(self, days: int) -> None:
        self._age += days
        self._baseStats.record_ages()

    def show(self) -> str:
        self._baseStats.record_shows()
        return (f"{self._name}: {round(self._height, 1)}cm, {self._age}"
                " days old")

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
            print(f"Height updated: {round(self._height)}cm")

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age
            print(f"Age updated: {self._age} days")

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return int(self._age)

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        if age < 365:
            return (False)
        else:
            return (True)

    @classmethod
    def anonymous(cls) -> 'Plant':
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int,
                 color: str, bloomed: bool) -> None:
        super().__init__(name, height, age)
        self._color = color
        self._bloomed = bloomed

    def show(self) -> str:
        if self._bloomed is False:
            return (f"{super().show()}\nColor: {self._color}\n{self._name}"
                    " has not bloomed yet")
        else:
            return (f"{super().show()}\nColor: {self._color}\n{self._name}"
                    " is blooming beautifully!")

    def bloom(self) -> None:
        self._bloomed = True


class Tree(Plant):
    class _TreeStats(Plant._Statistics):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls = 0

        def record_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> str:
            return (f"{super().display()}\n{self._shade_calls} shade")

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        self._name = name
        self._height = float(height) if height >= 0 else 0.0
        self._age = age if age >= 0 else 0
        self._trunk_diameter = float(trunk_diameter)
        self._treeStats = self._TreeStats()
        self._baseStats = self._treeStats

    def show(self) -> str:
        return (f"{super().show()}\nTrunk diameter: {self._trunk_diameter}cm")

    def produce_shade(self) -> None:
        self._treeStats.record_shade()
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}"
              f"cm long and {round(self._trunk_diameter, 1)}cm wide.")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, harvest_season: str,
                 nutritional_value: float) -> None:
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = nutritional_value

    def show(self) -> str:
        return (f"{super().show()}\nHarvest season: {self._harvest_season}\n"
                f"Nutritional value: {int(self._nutritional_value)}")

    def grow(self, cm: float) -> None:
        super().grow(cm)
        self._nutritional_value += 0.5

    def age(self, days: int) -> None:
        super().age(days)
        self._nutritional_value += 0.5


class Seed(Flower):
    def __init__(self, name: str, height: float, age:
                 int, color: str, bloomed: bool) -> None:
        super().__init__(name, height, age, color, bloomed)
        self._seeds = 0

    def show(self) -> str:
        return (f"{super().show()}\nSeeds: {self._seeds}")

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42


def display_statistics(plant: Plant) -> None:
    print(f"[statistics for {plant._name}]")
    print(plant._baseStats.display())


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(
        f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}\n")
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red", False)
    print(rose.show())
    display_statistics(rose)
    print("[asking the rose to grow and bloom]")
    rose.bloom()
    rose.grow(8)
    print(rose.show())
    display_statistics(rose)
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    print(oak.show())
    display_statistics(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_statistics(oak)
    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80, 45, "yellow", False)
    print(sunflower.show())
    print("[make sunflower grow, age and bloom]")
    sunflower.age(20)
    sunflower.grow(30)
    sunflower.bloom()
    print(sunflower.show())
    display_statistics(sunflower)
    print("\n=== Anonymous")
    unknown = Plant.anonymous()
    print(unknown.show())
    display_statistics(unknown)
