#!/usr/bin/env python3
import sys


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = {}
    for arg in sys.argv[1:]:
        parts = arg.split(":")
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue
        item_name, quantity_str = parts
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue
        try:
            quantity = int(quantity_str)
            inventory[item_name] = quantity
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")
    print(f"Got inventory: {inventory}")
    if inventory:
        item_list = list(inventory.keys())
        print(f"Item list: {item_list}")
        total_items = sum(inventory.values())
        print(f"Total quantity of the {len(inventory)} items: {total_items}")
        for item, qty in inventory.items():
            percentage = round((qty / total_items) * 100, 1)
            print(f"Item {item} represents {percentage}%")
        most_abundant = max(inventory, key=inventory.__getitem__)
        least_abundant = min(inventory, key=inventory.__getitem__)
        print(
            f"Item most abundant: {most_abundant} with quantity "
            f"{inventory[most_abundant]}")
        print(
            f"Item least abundant: {least_abundant} with quantity "
            f"{inventory[least_abundant]}")
    inventory.update({'magic_item': 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
