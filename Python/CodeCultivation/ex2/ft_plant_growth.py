class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.plant_age = age

    def grow(self, cm: float) -> None:
        self.height += cm

    def age(self) -> None:
        self.plant_age += 1

    def show(self) -> str:
        return (f"{self.name}: {round(self.height, 1)}cm, {self.plant_age}"
                " days old")


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    rose = Plant("Rose", 25.0, 30)
    start_height = rose.height
    print(rose.show())
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.grow(0.8)
        rose.age()
        print(rose.show())
    total_height = rose.height - start_height
    print(f"Growth this week: {round(total_height, 1)}cm")
