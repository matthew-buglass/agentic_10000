from itertools import combinations
from typing import List, Tuple


def get_play_names_and_indexes() -> List[Tuple[str, List[int]]]:
    numbers = [1, 2, 3, 4, 5]
    name_mapping = {
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
    }

    plays = [("STOP", []), ("PASS", [])]
    for i in range(min(numbers), max(numbers) + 1):
        perms = combinations(numbers, i)
        for perm in perms:
            name = f"KEEP_DICE_{'_'.join([name_mapping[num] for num in perm])}"
            indexes = [i-1 for i in perm]
            plays.append((name, indexes))

    return plays

def print_play_choices_generator():
    plays = get_play_names_and_indexes()
    play_enums = []
    index_enums = {}
    for i in range(len(plays)):
        name, indexes = plays[i]
        play_enums.append(f"{name}: int = {i}")
        index_enums[i] = indexes

    print("@dataclass")
    print("class PlayChoices:")
    print("\t" + "\n\t".join(play_enums))
    print()
    dict_string = "{\n\t\t" + "\n\t\t".join([f"{k}: {v}," for k, v in index_enums.items()]) + "\n\t}"
    print(f"\tplay_to_indexes = {dict_string}")
    print()
    print("\tdef get_indexes_from_play(self, play: int) -> List[int]:")
    print("\t\treturn self.play_to_indexes[play]")


if __name__ == "__main__":
    print_play_choices_generator()