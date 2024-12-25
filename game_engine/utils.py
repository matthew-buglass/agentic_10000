from itertools import combinations

from game_engine.game_models import PlayChoices


def get_play_names():
    numbers = [1, 2, 3, 4, 5]
    name_mapping = {
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
    }

    plays = ["STOP", "PASS"]
    for i in range(min(numbers), max(numbers) + 1):
        perms = combinations(numbers, i)
        for perm in perms:
            name = f"KEEP_DICE_{'_'.join([name_mapping[num] for num in perm])}"
            plays.append(name)

    return plays

def print_play_options():
    plays = get_play_names()
    for i in range(len(plays)):
        print(plays[i], "=", i)

def can_choose(choice: PlayChoices, roll: )

if __name__ == "__main__":
    print_play_options()