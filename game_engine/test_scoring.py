from agents.agents import Agent
from game_engine.game_models import TenThousandEngine, PlayChoices, score_selection, is_legal_selection
from pytest import mark

class TestAgent(Agent):

    def make_decision(self, agent_score: int, other_agent_scores: list[int], die_rolls: list[int]) -> int:
        pass


THREE_OF_A_KINDS = [[i]*3 for i in range(1, 7)]
FOUR_OF_A_KINDS = [[i]*4 for i in range(1, 7)]
FIVE_OF_A_KINDS = [[i]*5 for i in range(1, 7)]
STRAIGHTS = [list(range(1, 6)), list(range(2, 7))]

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
    @mark.parametrize("dice", [[2, 3, 4, 6, 2], [6, 3, 4], [2], [4]])
    def test_no_scoring_dice(self, dice):
        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 0 == score
        assert not is_covered

    @mark.parametrize("dice,expected_score,expected_is_covered", [
        ([6, 5, 6, 2, 6], 650, True),
        ([3, 3, 3, 3, 1], 700, True),
        ([1, 1, 1, 5], 1050, True),
        ([5, 5, 1], 200, True),
        ([4, 5, 4, 4], 450, True)
    ])
    def test_mixed_scoring_states(self, dice, expected_score, expected_is_covered):
        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert expected_score == score
        assert expected_is_covered == is_covered

    @mark.parametrize("dice", STRAIGHTS)
    def test_straights_worth_1000_uncovered(self, dice):
        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert 1000 == score
        assert not is_covered

    @mark.parametrize("dice", THREE_OF_A_KINDS)
    def test_3_of_a_kind_score_and_are_uncovered(self, dice):
        # Setup
        if dice[0] == 1:
            expected_score = 1000
        else:
            expected_score = dice[0] * 100

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert expected_score == score
        assert not is_covered

    @mark.parametrize("dice", FOUR_OF_A_KINDS)
    def test_4_of_a_kind_score_and_are_uncovered(self, dice):
        # Setup
        if dice[0] == 1:
            expected_score = 1000 * 2
        else:
            expected_score = dice[0] * 100 * 2

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert expected_score == score
        assert not is_covered

    @mark.parametrize("dice", FIVE_OF_A_KINDS)
    def test_5_of_a_kind_score_and_are_uncovered(self, dice):
        # Setup
        if dice[0] == 1:
            expected_score = 1000 * 4
        else:
            expected_score = dice[0] * 100 * 4

        # Execute
        score, is_covered = score_selection(dice)

        # Assert
        assert expected_score == score
        assert not is_covered

class TestSelectionLegality:
    def test_no_dice_is_legal_move(self):
        assert is_legal_selection([])

    @mark.parametrize("dice", [[1], [5], [1,1], [5,5], [1,5]])
    def test_all_selection_covers_are_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", THREE_OF_A_KINDS)
    def test_three_of_a_kind_is_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", FOUR_OF_A_KINDS)
    def test_four_of_a_kind_is_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", FIVE_OF_A_KINDS)
    def test_five_of_a_kind_is_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", STRAIGHTS)
    def test_straights_are_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", [[1, 1, 1, 5], [4, 4, 1, 4, 4]])
    def test_covered_sets_are_legal(self, dice):
        assert is_legal_selection(dice)

    @mark.parametrize("dice", [[1, 1, 1, 2], [4, 6, 1, 4, 4], [2], [1, 2, 3, 4], [6, 6, 5, 5]])
    def test_selecting_non_scoring_dice_is_illegal(self, dice):
        assert not is_legal_selection(dice)

    @mark.parametrize("dice", [[7], [3, 4, 5, 6, 7], [9, 10326], [1, 1, 1, 9], [8, 8, 8]])
    def test_numbers_higher_than_6_are_illegal(self, dice):
        assert not is_legal_selection(dice)

    @mark.parametrize("dice", [[0], [0, 1, 2, 3, 4], [-1, -10326], [1, 1, 1, -6], [0, 0, 0]])
    def test_numbers_lower_than_1_are_illegal(self, dice):
        assert not is_legal_selection(dice)

    @mark.parametrize("dice", [[1, 2, 3, 4, 5, 6], [3, 3, 3, 3, 3, 3], [1, 1, 1, 5, 5, 5]])
    def test_more_that_6_dice_are_illegal(self, dice):
        assert not is_legal_selection(dice)


class TestClassTenThousandEngineScoreCounter:
    def setup_method(self):
        self.engine = TenThousandEngine(players=[])


class TestTenThousandEngine:
    def setup_method(self):
        self.players = [TestAgent()]
        self.engine = TenThousandEngine(players=self.players)

    def test_illegal_move(self):
        # Setup
        pass