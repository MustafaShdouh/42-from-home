#!/usr/bin/env python3
import random


def main() -> None:
    print("=== Game Data Alchemist ===\n")
    players = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma',
               'Gregory', 'john', 'kevin', 'Liam']
    print(f"Initial list of players: {players}")
    all_cap = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {all_cap}")
    only_cap = [name for name in players if name[0].isupper()]
    print(f"New list of capitalized names only: {only_cap}")
    score_dict = {name: random.randint(10, 1000) for name in all_cap}
    print(f"Score dict: {score_dict}")
    average = round(sum(score_dict.values()) / len(score_dict), 2)
    print(f"Score average is {average}")
    high_scores = {name: score for name, score in score_dict.items()
                   if score > average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
