from abc import abstractmethod, ABCMeta
from typing import Any


class Agent:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.score = 0

    def adjust_score(self, score_diff):
        self.score += score_diff

    @abstractmethod
    def make_decision(self, agent_score: int, other_agent_scores: list[int], die_rolls: list[int]) -> int:
        """
        Take in a game state and make a decision

        Args:
            agent_score:
            other_agent_scores:
            die_rolls:

        Returns:
            An integer representing the action to take
        """
        pass


class HumanAgent(Agent):
    def make_decision(self, agent_score: int, other_agent_scores: list[int], die_rolls: list[int]) -> int:
        action_string = "00000"
        return 0