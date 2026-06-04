#!/usr/bin/env python3
import sys


# FOR MY EVALUATOR AND FOR ME IF I FORGET
# we are allowed to use all built in functions for list
# including append, but if we want we can use my_list += [value]
# but it is messy and append is the industry standard
# We are allowed to use all the built in functions for the data
# structures introduced in every exercise
def main() -> None:
    print("=== Player Score Analytics ===")
    script_name = sys.argv[0]
    scores = []
    for arg in sys.argv[1:]:
        try:
            value = int(arg)
            scores.append(value)
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    if not scores:
        print(
            f"No scores provided. Usage: "
            f"python3 {script_name} <score1> <score2> ...")
    else:
        length = len(scores)
        scores_sum = sum(scores)
        scores_max = max(scores)
        scores_min = min(scores)
        scores_avg = float(scores_sum / length)
        scores_range = scores_max - scores_min
        print(f"Scores processed: {scores}")
        print(f"Total players: {length}")
        print(f"Total score: {scores_sum}")
        print(f"Average score: {scores_avg}")
        print(f"High score: {scores_max}")
        print(f"Low score: {scores_min}")
        print(f"Score range: {scores_range}")


if __name__ == "__main__":
    main()
