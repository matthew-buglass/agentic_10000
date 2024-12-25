from itertools import combinations


def print_play_options():
    numbers = [1,2,3,4,5]
    name_mapping = {
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
    }

    counter = 1
    print("PASS = 0")
    for i in range(min(numbers), max(numbers)+1):
        perms = combinations(numbers, i)
        for perm in perms:
            name = f"KEEP_DICE_{'_'.join([name_mapping[num] for num in perm])} = {counter}"
            print(name)
            counter += 1

if __name__ == "__main__":
    print_play_options()