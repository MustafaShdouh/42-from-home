#!/usr/bin/env python3
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    try:
        file: typing.IO[str] = open(filename, "r")
        content = file.read()
        print("---")
        print(content, end="")
        if content and content[-1] != '\n':
            print()
        print("---")
        file.close()
        print(f"File '{filename}' closed.")
        print("Transform data:")
        print("---")
        lines = content.split('\n')
        transformed = ""
        for line in lines:
            if line:
                transformed += line + "#\n"
        print(transformed, end="")
        print("---")
        new_name = input("Enter new file name (or empty): ")
        if new_name:
            print(f"Saving data to '{new_name}'")
            out_file: typing.IO[str] = open(new_name, "w")
            out_file.write(transformed)
            out_file.close()
            print(f"Data saved in file '{new_name}'.")
        else:
            print("Not saving data.")
    except Exception as e:
        print(f"Error opening file '{filename}': {e}")


if __name__ == "__main__":
    main()
