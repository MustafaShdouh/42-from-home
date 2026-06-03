#!/usr/bin/env python3
import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw_input = input(
            "Enter new coordinates as floats in format 'x,y,z': ")
        input_list = raw_input.split(",")
        if (len(input_list) != 3):
            print("Invalid syntax")
            continue
        if len(input_list) == 3:
            coords = []
            for item in input_list:
                try:
                    coords.append(float(item))
                except ValueError:
                    print(
                        f"Error on parameter '{item}': could not "
                        f"convert string to float: '{item}'")
                    break
            if len(coords) == 3:
                return coords[0], coords[1], coords[2]


def main() -> None:
    print("=== Game Coordinate System ===\n")
    print("Get a first set of coordinates")
    coords1 = get_player_pos()
    print(f"Got a first tuple: {coords1}")
    x1, y1, z1 = coords1
    print(
        f"It includes: X={x1}, Y={y1}, Z={z1}")
    center = round(math.sqrt(x1**2 + y1**2 + z1**2), 4)
    print(f"Distance to center: {center}")
    print("\nGet a second set of coordinates")
    coords2 = get_player_pos()
    x2, y2, z2 = coords2
    distance = round(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2), 4)
    print(f"Distance between the 2 sets of coordinates: {distance}")


if __name__ == "__main__":
    main()
