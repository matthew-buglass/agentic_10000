from itertools import combinations_with_replacement, permutations
from typing import List, Tuple


def get_play_names_and_indexes() -> List[Tuple[str, List[int]]]:
    plays = []
    num_dice = 5
    for i in range(2**num_dice):
        name = f"KEEP_DICE_{bin(i)[2:].zfill(num_dice)}"
        indexes = [j for j, indx in enumerate(bin(i)[2:].zfill(num_dice)) if indx == "1"]
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