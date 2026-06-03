#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Command Quest ===")
    script_name = sys.argv[0]
    print(f"Program name: {script_name}")
    length = len(sys.argv)
    if length == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {length - 1}")
        i = 1
        while i < length:
            print(f"Argument {i}: {sys.argv[i]}")
            i += 1
    print(f"Total arguments: {length}")


if __name__ == "__main__":
    main()
