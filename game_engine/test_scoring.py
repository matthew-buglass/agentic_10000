from collections import Counter

from agents.agents import Agent
from game_engine.game_models import TenThousandEngine, PlayChoices, score_selection


class TestAgent(Agent):

    def make_decision(self, agent_score: int, other_agent_scores: list[int], die_rolls: list[int]) -> int:
        pass


class TestPlayChoices:
    def test_zero_move_works(self):
        # Setup
        play = 0
        expected_indices = []

        # Execute
        actual_indices = PlayChoices().get_indexes_from_play(play)

        # Assert
        assert expected_indices == actual_indices

    def test_middle_move_works(self):
        # Setup
        play = 13
        expected_indices = [1, 2, 4]

        # Execute
        actual_indices = PlayChoices().get_indexes_from_play(play)

        # Assert
        assert expected_indices == actual_indices

    def test_max_move_works(self):
        # Setup
        play = 31
        expected_indices = [0, 1, 2, 3, 4]

        # Execute
        actual_indices = PlayChoices().get_indexes_from_play(play)

        # Assert
        assert expected_indices == actual_indices


class TestScoringFunction:
    def test_no_scoring_dice(self):
        # Setup
        dice = [2, 3, 4, 6, 2]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 0 == score
        assert not is_covered

    def test_scoring_three_sixes_covered_with_five(self):
        # Setup
        dice = [6, 5, 6, 2, 6]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 650 == score
        assert is_covered

    def test_scoring_fewer_than_five_dice(self):
        # Setup
        dice = [1, 1, 1]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 1000 == score
        assert not is_covered

    def test_high_straight(self):
        # Setup
        dice = [2, 3, 4, 5, 6]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 1000 == score
        assert not is_covered

    def test_low_straight(self):
        # Setup
        dice = [1, 2, 3, 4, 5]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 1000 == score
        assert not is_covered

    def test_4_of_a_kind(self):
        # Setup
        dice = [2, 2, 2, 2]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 400 == score
        assert not is_covered

    def test_5_of_a_kind(self):
        # Setup
        dice = [5, 5, 5, 5, 5]

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 2000 == score
        assert not is_covered

class TestClassTenThousandEngineScoreCounter:
    def setup_method(self):
        self.engine = TenThousandEngine(players=[])

    def test_no_dice_is_legal_move(self):
        # Setup
        dice = []
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_one_one_is_legal_move(self):
        # Setup
        dice = [1]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_one_five_is_legal_move(self):
        # Setup
        dice = [5]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_three_ones_is_legal_move(self):
        # Setup
        dice = [1, 1, 1]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_three_fives_is_legal_move(self):
        # Setup
        dice = [5, 5, 5]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_one_three_is_illegal_move(self):
        # Setup
        dice = [3]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert not is_legal

    def test_three_threes_is_legal_move(self):
        # Setup
        dice = [3, 3, 3]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal

    def test_five_fours_is_legal_move(self):
        # Setup
        dice = [5, 5, 5, 5, 5]
        dice_counter = Counter(dice)

        # Execute
        is_legal = self.engine._is_legal_move(dice_counter)

        # Assert
        assert is_legal


class TestTenThousandEngine:
    def setup_method(self):
        self.players = [TestAgent()]
        self.engine = TenThousandEngine(players=self.players)

    def test_illegal_move(self):
        # Setup
        pass