#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Command Quest ===")
    arg_iterator = iter(sys.argv)
    script_name = next(arg_iterator)
    print(f"Program name: {script_name}")
    length = len(sys.argv)
    if length == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {length - 1}")
        for i, arg in enumerate(arg_iterator, start=1):
            print(f"Argument {i}: {arg}")
    print(f"Total arguments: {length}")


if __name__ == "__main__":
    main()
