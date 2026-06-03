class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error"):
        self.message = message
        super().__init__(self.message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error"):
        self.message = message
        super().__init__(self.message)


def test_custom_exception() -> None:
    print("=== Garden Custom Exceptions Demo ===\n")
    try:
        print("Testing PlantError...")
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught {e.__class__.__name__}: {e}\n")
    try:
        print("Testing WaterError...")
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught {e.__class__.__name__}: {e}\n")
    try:
        print("Testing catching all garden errors...")
        raise PlantError("The tomato is wilting!")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as e:
        print(f"Caught GardenError: {e}\n")
    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_exception()
