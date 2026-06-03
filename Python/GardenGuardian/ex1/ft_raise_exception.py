def input_temperature(temp_str: str) -> int:
    num = int(temp_str)
    if (num > 40):
        raise ValueError(
            f"{num}°C is too hot for plants (max 40°C)")
    elif (num < 0):
        raise ValueError(
            f"{num}°C is too cold for plants (min 0°C)")
    else:
        return num


def test_temperature() -> None:
    print("=== Garden Temperature Checker===\n")
    input_data = "25"
    result = 0
    print(f"Input data is ’{input_data}’")
    try:
        result = input_temperature(input_data)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")
    else:
        print(f"Temperature is now {result}°C\n")
    input_data = "abc"
    print(f"Input data is ’{input_data}’")
    try:
        result = input_temperature(input_data)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {result}°C\n")
    input_data = "100"
    print(f"Input data is ’{input_data}’")
    try:
        result = input_temperature(input_data)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {result}°C\n")
    input_data = "-50"
    print(f"Input data is ’{input_data}’")
    try:
        result = input_temperature(input_data)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {result}°C\n")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
