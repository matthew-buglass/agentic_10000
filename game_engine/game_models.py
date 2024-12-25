from enum import Enum
from random import randint as ri
from typing import List, Tuple, Optional


class PlayChoices(Enum):
    STOP = 0
    PASS = 1
    KEEP_DICE_ONE = 2
    KEEP_DICE_TWO = 3
    KEEP_DICE_THREE = 4
    KEEP_DICE_FOUR = 5
    KEEP_DICE_FIVE = 6
    KEEP_DICE_ONE_TWO = 7
    KEEP_DICE_ONE_THREE = 8
    KEEP_DICE_ONE_FOUR = 9
    KEEP_DICE_ONE_FIVE = 10
    KEEP_DICE_TWO_THREE = 11
    KEEP_DICE_TWO_FOUR = 12
    KEEP_DICE_TWO_FIVE = 13
    KEEP_DICE_THREE_FOUR = 14
    KEEP_DICE_THREE_FIVE = 15
    KEEP_DICE_FOUR_FIVE = 16
    KEEP_DICE_ONE_TWO_THREE = 17
    KEEP_DICE_ONE_TWO_FOUR = 18
    KEEP_DICE_ONE_TWO_FIVE = 19
    KEEP_DICE_ONE_THREE_FOUR = 20
    KEEP_DICE_ONE_THREE_FIVE = 21
    KEEP_DICE_ONE_FOUR_FIVE = 22
    KEEP_DICE_TWO_THREE_FOUR = 23
    KEEP_DICE_TWO_THREE_FIVE = 24
    KEEP_DICE_TWO_FOUR_FIVE = 25
    KEEP_DICE_THREE_FOUR_FIVE = 26
    KEEP_DICE_ONE_TWO_THREE_FOUR = 27
    KEEP_DICE_ONE_TWO_THREE_FIVE = 28
    KEEP_DICE_ONE_TWO_FOUR_FIVE = 29
    KEEP_DICE_ONE_THREE_FOUR_FIVE = 30
    KEEP_DICE_TWO_THREE_FOUR_FIVE = 31
    KEEP_DICE_ONE_TWO_THREE_FOUR_FIVE = 32

class TurnState:
    def __init__(self):
        self.current_player = None
        self.current_score = 0
        self.is_covered = False

class GameState:
    def __init__(self):
        pass

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

    def _is_legal_choice(self, choice: PlayChoices) -> bool:
        if choice == PlayChoices.PASS:
            return self.turn_state.is_covered
        return False

    def _roll(self) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int], Optional[int]]:
        match self.num_dice_to_roll:
            case 1:
                return ri(1, 6), None, None, None, None
            case 2:
                return ri(1, 6), ri(1, 6), None, None, None
            case 3:
                return ri(1, 6), ri(1, 6), ri(1, 6), None, None
            case 4:
                return ri(1, 6), ri(1, 6), ri(1, 6), ri(1, 6), None
            case 5:
                return ri(1, 6), ri(1, 6), ri(1, 6), ri(1, 6), ri(1, 6)
            case _:
                return None, None, None, None, None



    def choose(self, choice: PlayChoices) -> int:
        """
        Takes a player's choice and either applies it to the game if it is legal and returns 0, or
        returns a punishment value if the move is illegal.

        Args:
            choice:

        Returns:

        """
        pass

