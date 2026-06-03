#!/usr/bin/env python3
import random


def gen_player_achievements() -> set[str]:
    achievements = ["Crafting Genius", "Strategist",
                    "World Savior", "Speed Runner",
                    "Survivor", "Master Explorer",
                    "Treasure Hunter", "Unstoppable",
                    "First Steps", "Collector Supreme",
                    "Untouchable", "Sharp Mind", "Boss Slayer",]
    achievement_count = random.randint(3, 12)
    player_achievements = set(random.sample(achievements, achievement_count))
    return player_achievements


def main() -> None:
    print("=== Achievement Tracker System ===\n")
    alice = gen_player_achievements()
    print(f"Player Alice: {alice}")
    bob = gen_player_achievements()
    print(f"Player Bob: {bob}")
    charlie = gen_player_achievements()
    print(f"Player Charlie: {charlie}")
    dylan = gen_player_achievements()
    print(f"Player Dylan: {dylan}\n")
    distinct_achievements = alice | bob | charlie | dylan
    print(f"All distinct achievements: {distinct_achievements}\n")
    common_achievements = alice & bob & charlie & dylan
    print(f"Common achievements: {common_achievements}\n")
    alice_diff = alice - bob - charlie - dylan
    print(f"Only Alice has: {alice_diff}")
    bob_diff = set.difference(bob, alice, dylan, charlie)
    print(f"Only Bob has: {bob_diff}")
    charlie_diff = set.difference(charlie, bob, dylan, alice)
    print(f"Only Charlie has: {charlie_diff}")
    dylan_diff = set.difference(dylan, bob, alice, charlie)
    print(f"Only Dylan has: {dylan_diff}\n")
    alice_missing = set.difference(distinct_achievements, alice)
    print(f"Alice is missing: {alice_missing}")
    bob_missing = set.difference(distinct_achievements, bob)
    print(f"Bob is missing: {bob_missing}")
    charlie_missing = set.difference(distinct_achievements, charlie)
    print(f"Charlie is missing: {charlie_missing}")
    dylan_missing = set.difference(distinct_achievements, dylan)
    print(f"Dylan is missing: {dylan_missing}")


if __name__ == "__main__":
    main()
