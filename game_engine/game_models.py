from collections import Counter
from dataclasses import dataclass
from random import randint as ri
from typing import List, Optional, Tuple


@dataclass
class PlayChoices:
    KEEP_DICE_00000: int = 0
    KEEP_DICE_00001: int = 1
    KEEP_DICE_00010: int = 2
    KEEP_DICE_00011: int = 3
    KEEP_DICE_00100: int = 4
    KEEP_DICE_00101: int = 5
    KEEP_DICE_00110: int = 6
    KEEP_DICE_00111: int = 7
    KEEP_DICE_01000: int = 8
    KEEP_DICE_01001: int = 9
    KEEP_DICE_01010: int = 10
    KEEP_DICE_01011: int = 11
    KEEP_DICE_01100: int = 12
    KEEP_DICE_01101: int = 13
    KEEP_DICE_01110: int = 14
    KEEP_DICE_01111: int = 15
    KEEP_DICE_10000: int = 16
    KEEP_DICE_10001: int = 17
    KEEP_DICE_10010: int = 18
    KEEP_DICE_10011: int = 19
    KEEP_DICE_10100: int = 20
    KEEP_DICE_10101: int = 21
    KEEP_DICE_10110: int = 22
    KEEP_DICE_10111: int = 23
    KEEP_DICE_11000: int = 24
    KEEP_DICE_11001: int = 25
    KEEP_DICE_11010: int = 26
    KEEP_DICE_11011: int = 27
    KEEP_DICE_11100: int = 28
    KEEP_DICE_11101: int = 29
    KEEP_DICE_11110: int = 30
    KEEP_DICE_11111: int = 31

    play_to_indexes = {
        0: [],
        1: [4],
        2: [3],
        3: [3, 4],
        4: [2],
        5: [2, 4],
        6: [2, 3],
        7: [2, 3, 4],
        8: [1],
        9: [1, 4],
        10: [1, 3],
        11: [1, 3, 4],
        12: [1, 2],
        13: [1, 2, 4],
        14: [1, 2, 3],
        15: [1, 2, 3, 4],
        16: [0],
        17: [0, 4],
        18: [0, 3],
        19: [0, 3, 4],
        20: [0, 2],
        21: [0, 2, 4],
        22: [0, 2, 3],
        23: [0, 2, 3, 4],
        24: [0, 1],
        25: [0, 1, 4],
        26: [0, 1, 3],
        27: [0, 1, 3, 4],
        28: [0, 1, 2],
        29: [0, 1, 2, 4],
        30: [0, 1, 2, 3],
        31: [0, 1, 2, 3, 4],
    }

    def get_indexes_from_play(self, play: int) -> List[int]:
        return self.play_to_indexes[play]


class TurnState:
    def __init__(self):
        self.current_player = None
        self.current_score = 0
        self.is_covered = False


class GameState:
    def __init__(self):
        pass


@dataclass
class Roll:
    def __init__(self, data: List[int]):
        assert len(data) <= 5, "Maximum of 5 dice allowed."
        self.data = [None] * 5
        for i, val in enumerate(data):
            self.data[i] = val

    @property
    def dice_one(self) -> Optional[int]:
        return self.data[0]

    @property
    def dice_two(self) -> Optional[int]:
        return self.data[1]

    @property
    def dice_three(self) -> Optional[int]:
        return self.data[2]

    @property
    def dice_four(self) -> Optional[int]:
        return self.data[3]

    @property
    def dice_five(self) -> Optional[int]:
        return self.data[4]

    def get_values_from_indices(self, indices: List[int]) -> List[Optional[int]]:
        return [self.data[i] for i in indices]


class TenThousandEngine:
    """
    A Game manager that encodes and coordinates the rules and the playing of the game.
    """
    illegal_move_mapping = {}
    win_con = 10000
    num_dice_total = 5

    # Punishment values
    illegal_move = -1000

    def __init__(self, players: List):
        self.players = players

        self.scores = {}
        for player in players:
            self.scores[player] = 0

        self.num_dice_to_roll = 5
        self.turn_state = TurnState()
        self.current_roll: Optional[Roll] = None

    def _count_score(self, values_counter: Counter[int]) -> Tuple[int, bool]:
        """
        Counts the scores associated with the values counter
        Args:
            values_counter: a counter mapping the integer face value of the dice to the number
                of those types of dice that were kept.

        Returns:
            The score of the kept dice and whether the score is covered.
        """
        is_covered = False
        score = 0
        for num, count in values_counter.items():
            if num == 1 and count < 3:
                is_covered = True
                score += 100 * count
            elif num == 5 and count < 3:
                is_covered = True
                score += 50 * count
            else:
                three_of_a_kind = count // 3 > 0
                remainder = count % 3
                temp_score = 0
                if three_of_a_kind:
                    if num == 1:
                        temp_score += 1000
                    else:
                        temp_score += num * 100
                score += temp_score * (remainder + 1)

        return score, is_covered

    def _roll(self) -> Roll:
        rolls = [ri(1,6) for _ in range(self.num_dice_to_roll)]
        self.rolls = Roll(rolls)
        return self.rolls

    @staticmethod
    def is_legal_move(values_counter: Counter) -> bool:
        """
        Takes the numbers selected and checks if they are legal to take.

        Args:
            values_counter: a Counter object mapping the integer face value of the dice to the number

        Returns:
            A boolean indicating if the dice is legal or not.
        """
        for num, count in values_counter.items():
            if num == 1 and count < 3:
                return True
            elif num == 5 and count < 3:
                return True
            elif count >= 3:
                return True
        return False

    def choose(self, choice: int) -> int:
        """
        Takes a player's choice and either applies it to the game if it is legal and returns 0, or
        returns a punishment value if the move is illegal.

        Args:
            choice: and integer representing the player choice. Must be between 0 and (2 ^ number_of_dice) - 1.

        Returns:

        """
        try:
            values = self.current_roll.get_values_from_indices(PlayChoices.get_indexes_from_play(play=choice))
        except IndexError:
            return self.illegal_move

        val_counter = Counter(values)
        # All dice have to be a value
        if self.is_legal_move(val_counter):
            return self.illegal_move

        match choice:
            case PlayChoices.KEEP_DICE_00000: # Not choosing any dice
                if self.turn_state.is_covered:
                    pass # increase score
                else:
                    pass # wipe dice
            case _:
                score, is_covered = self._count_score(val_counter)
                self.turn_state.is_covered = is_covered
                self.turn_state.current_score += score
                return score
