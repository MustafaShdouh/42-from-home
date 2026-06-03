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
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25.0, 30)
    print(f"Created: {rose.show()}")
    oak = Plant("Oak", 200.0, 365)
    print(f"Created: {oak.show()}")
    cactus = Plant("Cactus", 5.0, 90)
    print(f"Created: {cactus.show()}")
    sun_flower = Plant("Sunflower", 80.0, 45)
    print(f"Created: {sun_flower.show()}")
    fern = Plant("Fern", 15.0, 120)
    print(f"Created: {fern.show()}")
