from collections import Counter
from dataclasses import dataclass
from random import randint as ri
from pydantic import BaseModel

from agents.agents import Agent

@dataclass
class Roll:
    def __init__(self, data: list[int]):
        assert len(data) <= 5, "Maximum of 5 dice allowed."
        self.data = [None] * 5
        for i, val in enumerate(data):
            self.data[i] = val

    @property
    def dice_one(self) -> int | None:
        return self.data[0]

    @property
    def dice_two(self) -> int | None:
        return self.data[1]

    @property
    def dice_three(self) -> int | None:
        return self.data[2]

    @property
    def dice_four(self) -> int | None:
        return self.data[3]

    @property
    def dice_five(self) -> int | None:
        return self.data[4]

    def get_values_from_indices(self, indices: list[int]) -> list[int | None]:
        return [self.data[i] for i in indices]


class TurnState(BaseModel):
    current_player_id: str
    current_roll: Roll | None = None

    num_dice_to_roll: int = 5
    running_score: int = 0
    is_covered: bool = False


class GameState(BaseModel):
    player_map: dict[str, Agent]
    players: list[Agent]
    current_player_index: int = 0
    turn_state: TurnState

    def __init__(self, players: list[Agent], **kwargs):
        super().__init__(**kwargs)
        self.players = players
        self.player_map = {player.id: player for player in players}

        self.turn_state = TurnState(current_player_id=players[self.current_player_index].id)


class IllegalMoveException(Exception):
    """Raised when a move is illegal"""


class FailedToScoreException(Exception):
    """Raised when a user failed to score"""


class NotActivePlayerException(Exception):
    """Raised when the submitting player is not the active player"""


HIGH_STRAIGHT = [2, 3, 4, 5, 6]
LOW_STRAIGHT = [1, 2, 3, 4, 5]


def score_selection(selected_numbers: list[int]) -> (int, bool):
    """
    Takes a list of integers that represent a valid selection and tallies the score for that selection and determines whether that score is coverd

    Returns:
        A tuple where the first element is the score for the selection and whether that selection is covered.
    """
    # Sort the selection for consistency
    sorted_selection = selected_numbers.copy()
    sorted_selection.sort()

    if sorted_selection == HIGH_STRAIGHT or sorted_selection == LOW_STRAIGHT:
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

    if sorted_selection == HIGH_STRAIGHT or sorted_selection == LOW_STRAIGHT:
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
        self.game_state = GameState(players=players)

    def _roll(self) -> Roll:
        rolls = [ri(1,6) for _ in range(self.num_dice_to_roll)]
        self.rolls = Roll(rolls)
        return self.rolls

    @property
    def current_roll(self) -> Roll:
        return self.game_state.turn_state.current_roll

    @property
    def current_player_id(self) -> str:
        return self.game_state.turn_state.current_player_id

    def choose(self, player_id: str, indices_to_keep: list[int], end_turn: bool) -> GameState:
        """
        Takes a player's choice and applies it to the game.

        Args:
            end_turn: Whether the player wants to end their turn
            indices_to_keep: A list of dice indices to keep from the roll
            player_id: The ID of the player making the move.

        Raises:
            IllegalMoveException: When a user made an illegal move.
            NotActivePlayerException: When a player made a choice when they are not hte active player.

        Returns:
            A tuple of an integer and a boolean where the integer it the score for the current turn and the boolean
            is whether the turn is covered.
        """
        if player_id != self.current_player_id:
            raise NotActivePlayerException()

        if not indices_to_keep:
            # If you don't keep any dice from your roll, it doesn't matter whether you want to end your turn
            self.reset_turn_to_default()
            self.advance_to_next_player()
        else:
            try:
                values = self.current_roll.get_values_from_indices(indices_to_keep)
            except IndexError:
                raise IllegalMoveException()

            # All dice have to be a value
            if is_legal_selection(values):
                raise IllegalMoveException()

            else:
                score, is_covered = score_selection(values)

                if end_turn and not is_covered:
                    # You can't score and end your turn if your score isn't covered
                    raise IllegalMoveException()

                self.update_is_covered(is_covered)
                self.increment_running_score(score)
                self.update_available_dice(len(indices_to_keep))

                if end_turn:
                    self.update_player_score()
                    self.advance_to_next_player()

        return self.game_state

    def update_is_covered(self, is_covered: bool):
        self.game_state.turn_state.is_covered = is_covered

    def increment_running_score(self, score):
        self.game_state.turn_state.running_score += score

    def update_available_dice(self, dice_kept: int):
        dice_remaining = self.game_state.turn_state.num_dice_to_roll - dice_kept
        # if we've kept all the dice, we get a new 5
        if dice_remaining == 0:
            dice_remaining = 5

        self.game_state.turn_state.num_dice_to_roll = dice_remaining

    def update_player_score(self):
        current_player = self.game_state.player_map[self.current_player_id]
        current_player.adjust_score(self.game_state.turn_state.running_score)

    def advance_to_next_player(self):
        self.game_state.current_player_index = (self.game_state.current_player_index + 1) % len(self.game_state.players)
        self.game_state.turn_state.current_player_id = self.game_state.players[self.game_state.current_player_index].id

    def reset_turn_to_default(self):
        self.game_state.turn_state.num_dice_to_roll = 5
        self.game_state.turn_state.running_score = 0
        self.game_state.turn_state.is_covered = False


