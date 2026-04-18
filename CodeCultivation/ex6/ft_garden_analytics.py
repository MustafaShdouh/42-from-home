class Plant:
    class Statistics:
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

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, {self._age_calls} age, "
                  f"{self._show_calls} show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._height = height
        self._age = age
        self._statistics = self.Statistics()

    def grow(self, cm: float) -> None:
        self._height += cm
        self._statistics.record_grows()

    def age(self) -> None:
        self._age += 1
        self._statistics.record_ages()

    def show(self) -> str:
        self._statistics.record_shows()
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
        return self._age

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        if age < 365:
            return (False)
        else:
            return (True)

    @classmethod
    def anonymous(self) -> None:
        self._name = "Unknown"
        self._height = 0.0
        self._age = 0


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
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float):
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter
        self._shade_calls = 0

    def show(self) -> str:
        return (f"{super().show()}\nTrunk diameter: {self._trunk_diameter}cm")

    def produce_shade(self) -> None:
        print(f"Tree Oak now produces a shade of {round(self._height, 1)}"
              f"cm long and {round(self._trunk_diameter, 1)}cm wide.")
        self._shade_calls += 1


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, harvest_season: str,
                 nutritional_value: float):
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = nutritional_value

    def show(self) -> str:
        return (f"{super().show()}\nHarvest season: {self._harvest_season}\n"
                f"Nutritional value: {int(self._nutritional_value)}")

    def grow(self, cm: float) -> None:
        super().grow(cm)
        self._nutritional_value += 0.5

    def age(self) -> None:
        super().age()
        self._nutritional_value += 0.5


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str, bloomed: bool) -> None:
        super().__init__(name, height, age, color, bloomed)
        self._seeds = 0

    def show(self) -> str:
        return (f"{super().show()}\nSeeds: {self._seeds}")

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42


def display_


if __name__ == "__main__":
