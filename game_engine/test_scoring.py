from collections import Counter
from game_engine.game_models import TenThousandEngine


class TestClassTenThousandEngineScoreCounter:
    def setup_method(self):
        self.engine = TenThousandEngine(players=[])

    def test_no_scoring_dice(self):
        # Setup
        dice = [2, 3, 4, 6, 2]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        assert 0 == score
        assert not is_covered

    def test_scoring_three_sixes_covered_with_five(self):
        # Setup
        dice = [6, 5, 6, 2, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        assert 650 == score
        assert is_covered

    def test_scoring_fewer_than_five_dice(self):
        # Setup
        dice = [1, 1, 1]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        assert 1000 == score
        assert not is_covered

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
