class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._height = float(height) if height >= 0 else 0.0
        self._age = age if age >= 0 else 0

    def grow(self, cm: float) -> None:
        self._height += cm

    def age(self) -> None:
        self._age += 1

    def show(self) -> str:
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
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter

    def show(self) -> str:
        return (f"{super().show()}\nTrunk diameter: {self._trunk_diameter}cm")

    def produce_shade(self) -> None:
        print(f"Tree Oak now produces a shade of {round(self._height, 1)}"
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

    def age(self) -> None:
        super().age()
        self._nutritional_value += 0.5


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print("== Flower")
    rose = Flower("Rose", 15.0, 10, "red", False)
    print(f"{rose.show()}")
    print("[asking the rose to bloom]")
    rose.bloom()
    print(f"{rose.show()}")
    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    print(f"{oak.show()}")
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April", 0)
    print(f"{tomato.show()}")
    print("[make tomato grow and age for 20 days]")
    for i in range(0, 20):
        tomato.grow(2.1)
        tomato.age()
    print(f"{tomato.show()}")
