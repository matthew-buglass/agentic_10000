from dataclasses import dataclass
from enum import Enum
from logging import setLogRecordFactory
from random import randint as ri
from typing import List, Tuple, Optional
from unittest import case


@dataclass
class PlayChoices:
	STOP: int = 0
	PASS: int = 1
	KEEP_DICE_ONE: int = 2
	KEEP_DICE_TWO: int = 3
	KEEP_DICE_THREE: int = 4
	KEEP_DICE_FOUR: int = 5
	KEEP_DICE_FIVE: int = 6
	KEEP_DICE_ONE_TWO: int = 7
	KEEP_DICE_ONE_THREE: int = 8
	KEEP_DICE_ONE_FOUR: int = 9
	KEEP_DICE_ONE_FIVE: int = 10
	KEEP_DICE_TWO_THREE: int = 11
	KEEP_DICE_TWO_FOUR: int = 12
	KEEP_DICE_TWO_FIVE: int = 13
	KEEP_DICE_THREE_FOUR: int = 14
	KEEP_DICE_THREE_FIVE: int = 15
	KEEP_DICE_FOUR_FIVE: int = 16
	KEEP_DICE_ONE_TWO_THREE: int = 17
	KEEP_DICE_ONE_TWO_FOUR: int = 18
	KEEP_DICE_ONE_TWO_FIVE: int = 19
	KEEP_DICE_ONE_THREE_FOUR: int = 20
	KEEP_DICE_ONE_THREE_FIVE: int = 21
	KEEP_DICE_ONE_FOUR_FIVE: int = 22
	KEEP_DICE_TWO_THREE_FOUR: int = 23
	KEEP_DICE_TWO_THREE_FIVE: int = 24
	KEEP_DICE_TWO_FOUR_FIVE: int = 25
	KEEP_DICE_THREE_FOUR_FIVE: int = 26
	KEEP_DICE_ONE_TWO_THREE_FOUR: int = 27
	KEEP_DICE_ONE_TWO_THREE_FIVE: int = 28
	KEEP_DICE_ONE_TWO_FOUR_FIVE: int = 29
	KEEP_DICE_ONE_THREE_FOUR_FIVE: int = 30
	KEEP_DICE_TWO_THREE_FOUR_FIVE: int = 31
	KEEP_DICE_ONE_TWO_THREE_FOUR_FIVE: int = 32

	play_to_indexes = {
		0: [],
		1: [],
		2: [0],
		3: [1],
		4: [2],
		5: [3],
		6: [4],
		7: [0, 1],
		8: [0, 2],
		9: [0, 3],
		10: [0, 4],
		11: [1, 2],
		12: [1, 3],
		13: [1, 4],
		14: [2, 3],
		15: [2, 4],
		16: [3, 4],
		17: [0, 1, 2],
		18: [0, 1, 3],
		19: [0, 1, 4],
		20: [0, 2, 3],
		21: [0, 2, 4],
		22: [0, 3, 4],
		23: [1, 2, 3],
		24: [1, 2, 4],
		25: [1, 3, 4],
		26: [2, 3, 4],
		27: [0, 1, 2, 3],
		28: [0, 1, 2, 4],
		29: [0, 1, 3, 4],
		30: [0, 2, 3, 4],
		31: [1, 2, 3, 4],
		32: [0, 1, 2, 3, 4],
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
    die_one: Optional[int] = None
    die_two: Optional[int] = None
    die_three: Optional[int] = None
    die_four: Optional[int] = None
    die_five: Optional[int] = None

    @classmethod
    def from_list(cls, data: List[int]) -> "Roll":
        assert len(data) <= 5, "Maximum of 5 dice allowed."
        obj = Roll()
        for i in range(len(data)):
            match i + 1:
                case 1:
                   obj.die_one = data[i]
                case 2:
                    obj.die_two = data[i]
                case 3:
                    obj.die_three = data[i]
                case 4:
                    obj.die_four = data[i]
                case 5:
                    obj.die_five = data[i]
        return obj


class TenThousandEngine:
    """
    A Game manager that encodes and coordinates the rules and the playing of the game.
    """
    illegal_move_mapping = {}
    win_con = 10000
    num_dice_total = 5

    def __init__(self, players: List):
        self.players = players

        self.scores = {}
        for player in players:
            self.scores[player] = 0

        self.num_dice_to_roll = 5
        self.turn_state = TurnState()

    def _can_select_dice(self, choice: PlayChoices, roll: Roll) -> bool:
        match choice:
            case PlayChoices.STOP:
                return (
                        True
                )
            case PlayChoices.PASS:
                return (
                        self.turn_state.is_covered
                )
            case PlayChoices.KEEP_DICE_ONE:
                return (
                        roll.die_one is not None
                )
            case PlayChoices.KEEP_DICE_TWO:
                return (
                        roll.die_two is not None
                )
            case PlayChoices.KEEP_DICE_THREE:
                return (
                        roll.die_three is not None
                )
            case PlayChoices.KEEP_DICE_FOUR:
                return (
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_FIVE:
                return (
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None
                )
            case PlayChoices.KEEP_DICE_ONE_THREE:
                return (
                        roll.die_one is not None and
                        roll.die_three is not None
                )
            case PlayChoices.KEEP_DICE_ONE_FOUR:
                return (
                        roll.die_one is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_ONE_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_TWO_THREE:
                return (
                        roll.die_two is not None and
                        roll.die_three is not None
                )
            case PlayChoices.KEEP_DICE_TWO_FOUR:
                return (
                        roll.die_two is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_TWO_FIVE:
                return (
                        roll.die_two is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_THREE_FOUR:
                return (
                        roll.die_three is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_THREE_FIVE:
                return (
                        roll.die_three is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_FOUR_FIVE:
                return (
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_THREE:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_three is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_FOUR:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_THREE_FOUR:
                return (
                        roll.die_one is not None and
                        roll.die_three is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_ONE_THREE_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_three is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_FOUR_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_TWO_THREE_FOUR:
                return (
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_TWO_THREE_FIVE:
                return (
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_TWO_FOUR_FIVE:
                return (
                        roll.die_two is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_THREE_FOUR_FIVE:
                return (
                        roll.die_three is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_THREE_FOUR:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_four is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_THREE_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_FOUR_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_THREE_FOUR_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_three is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_TWO_THREE_FOUR_FIVE:
                return (
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )
            case PlayChoices.KEEP_DICE_ONE_TWO_THREE_FOUR_FIVE:
                return (
                        roll.die_one is not None and
                        roll.die_two is not None and
                        roll.die_three is not None and
                        roll.die_four is not None and
                        roll.die_five is not None
                )

    def _roll(self) -> Roll:
        rolls = [ri(1,6) for _ in range(self.num_dice_to_roll)]
        return Roll.from_list(rolls)

    def choose(self, choice: PlayChoices) -> int:
        """
        Takes a player's choice and either applies it to the game if it is legal and returns 0, or
        returns a punishment value if the move is illegal.

        Args:
            choice:

        Returns:

        """
        pass

