class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.plant_age = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.plant_age} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant("Rose", 25, 30)
    sun = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)
    rose.show()
    sun.show()
    cactus.show()
