def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "text" + 5
    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {e.__class__.__name__}: {e}")
        else:
            print("Operation completed successfully\n")
        # or we can do
        # try:
        #     garden_operations(i)
        # except ValueError as e:
        # print("Caught ValueError: {e}")....same for rest
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
