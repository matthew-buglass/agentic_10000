import re
from collections import Counter
from dataclasses import dataclass
from random import randint as ri
from typing import List, Optional, Tuple
from pydantic import BaseModel

from agents.agents import Agent


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

    def get_indexes_from_play(self, play: int) -> List[int]:
        return [match.start(0) for match in re.finditer("1", f'{play:05b}')]


class TurnState(BaseModel):
    current_player_index: int
    current_score: int = 0
    is_covered: bool = False


class GameState(BaseModel):
    game_scores: list[int]
    turn_state: TurnState


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

class IllegalMoveException(Exception):
    """An exception for when a move is illegal"""

class FailedToScoreException(Exception):
    """An exception for when a user failed to score"""

high_straight = [2, 3, 4, 5, 6]
low_straight = [1, 2, 3, 4, 5]

def score_selection(selected_numbers: list[int]) -> (int, bool):
    """
    Takes a list of integers that represent a valid selection and tallies the score for that selection and determines whether that score is coverd

    Returns:
        A tuple where the first element is the score for the selection and whether that selection is covered.
    """
    # Sort the selection for consistency
    sorted_selection = selected_numbers.copy()
    sorted_selection.sort()

    if sorted_selection == high_straight or sorted_selection == low_straight:
        return 1_000, False

    selection_counter = Counter(sorted_selection)
    is_covered = False
    score = 0
    for num, count in selection_counter.items():
        # 100 points for each 1, score is covered
        if num == 1 and count < 3:
            is_covered = True
            score += 100 * count
        # 50 points for each 5, score is covered
        elif num == 5 and count < 3:
            is_covered = True
            score += 50 * count
        # For sets of 3, 4 or 5.
        elif count >= 3:
            # 1000 points for 1's
            if num == 1:
                base_score = 1000
            # face value * 100 for the rest
            else:
                base_score = num * 100

            remainder = count % 3
            # Double the base score for each die in the set oast the third
            set_score = base_score * 2 ** remainder

            # Adjust the score, sets don't affect coverage
            score += set_score

    return score, is_covered

def is_legal_selection(values: list[int]) -> bool:
    """
    Takes the numbers selected and checks if they are legal to take.

    Args:
        values: a Counter object mapping the integer face value of the dice to the number

    Returns:
        A boolean indicating if the dice is legal or not.
    """
    # Sort the selection for consistency
    sorted_selection = values.copy()
    sorted_selection.sort()

    if sorted_selection == high_straight or sorted_selection == low_straight:
        return True
    if len(sorted_selection) > 5:
        return False

    values_counter = Counter(sorted_selection)
    for num, count in values_counter.items():
        # Not in range
        if num < 1 or num > 6:
            return False
        # Non-covering dice that is not in a set
        if num not in [1, 5] and count < 3:
            return False
    return True


class TenThousandEngine:
    """
    A Game manager that encodes and coordinates the rules and the playing of the game.
    """
    winning_score = 10_000
    num_dice_total = 5

    def __init__(self, players: list[Agent]):
        self.players = players

        self.scores = {}
        for player in players:
            self.scores[player] = 0

        self.num_dice_to_roll = 5
        turn_state = TurnState(current_player_index=0)
        self.game_state = GameState(game_scores=[0 for _ in range(len(players))], turn_state=turn_state)
        self.current_roll: Optional[Roll] = None
        self.current_player_index = 0

    def _roll(self) -> Roll:
        rolls = [ri(1,6) for _ in range(self.num_dice_to_roll)]
        self.rolls = Roll(rolls)
        return self.rolls

    def choose(self, choice: int) -> (int, bool):
        """
        Takes a player's choice and applies it to the game.

        Args:
            choice: and integer representing the player choice. Must be between 0 and (2 ^ number_of_dice) - 1.

        Raises:
            FailedToScoreException: When a user failed to score on this turn.
            IllegalMoveException: When a user made an illegal move.

        Returns:
            A tuple of an integer and a boolean where the integer it the score for the current turn and the boolean
            is whether the turn is covered.
        """
        try:
            values = self.current_roll.get_values_from_indices(PlayChoices.get_indexes_from_play(play=choice))
        except IndexError:
            raise IllegalMoveException()

        # All dice have to be a value
        if self._is_legal_move(values):
            raise IllegalMoveException()

        current_player_index = self.game_state.turn_state.current_player_index

        match choice:
            case PlayChoices.KEEP_DICE_00000: # Not choosing any dice
                if self.game_state.turn_state.is_covered:
                    self.players[current_player_index].adjust_score(self.game_state.turn_state.current_score)
                    self.game_state.turn_state.current_player_index = (current_player_index + 1) % len(self.players)
                    return self.game_state.turn_state.current_score, False
                else:
                    self.game_state.turn_state.current_player_index = (current_player_index + 1) % len(self.players)
                    raise FailedToScoreException
            case _:
                score, is_covered = score_selection(values)
                self.game_state.turn_state.is_covered = is_covered
                self.game_state.turn_state.current_score += score
                return 0, True
