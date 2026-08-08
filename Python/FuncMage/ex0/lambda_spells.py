def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    try:
        return list(sorted(artifacts, key=lambda item:
                    item["power"], reverse=True))
    except (TypeError, AttributeError, KeyError) as e:
        print(e)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    try:
        return list(filter(lambda x: x["power"] >= min_power, mages))
    except (ValueError, TypeError, AttributeError, KeyError) as e:
        print(e)


def spell_transformer(spells: list[str]) -> list[str]:
    try:
        return list(map(lambda x: "* " + x + " *", spells))
    except TypeError as e:
        print(e)


def mage_stats(mages: list[dict]) -> dict:
    try:
        max_power = max(mages, key=lambda x: x["power"])["power"]
        min_power = min(mages, key=lambda x: x["power"])["power"]
        all_powers = list(map(lambda x: x["power"], mages))
        average_power = round(sum(all_powers) / len(all_powers), 2)
        return {
            "max_power": max_power,
            "min_power": min_power,
            "average_power": average_power,
        }
    except (TypeError, ValueError, ZeroDivisionError, KeyError) as e:
        print(e)


def main():
    artifacts = [
        {"name": "Shadow Blade", "power": 94, "type": "relic"},
        {"name": "Crystal Orb", "power": 83, "type": "armor"},
        {"name": "Fire Staff", "power": 66, "type": "weapon"},
        {"name": "Crystal Orb", "power": 93, "type": "weapon"},
    ]

    sorted_artifacts = artifact_sorter(artifacts)

    print("Sorted Artifacts:\n")
    try:
        for i, x in enumerate(sorted_artifacts, start=1):
            print(f"{i}: {x}")
        print(f"Total Artifacts: {i}\n")
    except TypeError as e:
        print(e)

    mages = [
        {"name": "Alex", "power": 73, "element": "shadow"},
        {"name": "Nova", "power": 62, "element": "fire"},
        {"name": "Alex", "power": 54, "element": "ice"},
        {"name": "Morgan", "power": 95, "element": "fire"},
        {"name": "Storm", "power": 89, "element": "earth"},
    ]

    filtered_powers = power_filter(mages, 78)

    try:
        for i, x in enumerate(filtered_powers, start=1):
            print(f"{i}: {x}")
        print(f"Total Mages: {i}\n")
    except TypeError as e:
        print(e)
    print("Transformed Spells:")
    spells = ["meteor", "flash", "shield", "tsunami"]
    transformed_spells = spell_transformer(spells)
    for i, x in enumerate(transformed_spells, start=1):
        print(f"{i}: {x}")

    print("\nMage Sats:")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
