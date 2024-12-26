import unittest
from collections import Counter

from game_engine.game_models import TenThousandEngine


class TenThousandEngineScoreCounter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
       cls.engine = TenThousandEngine(players=[])

    def test_no_scoring_dice(self):
        # Setup
        dice = [2, 3, 4, 6, 2]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(0, score)
        self.assertFalse(is_covered)

    def test_scoring_one(self):
        # Setup
        dice = [1, 3, 4, 6, 2]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(100, score)
        self.assertTrue(is_covered)

    def test_scoring_five(self):
        # Setup
        dice = [5, 3, 4, 6, 2]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(50, score)
        self.assertTrue(is_covered)

    def test_scoring_one_and_five(self):
        # Setup
        dice = [1, 3, 5, 6, 2]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(150, score)
        self.assertTrue(is_covered)

    def test_scoring_two_ones_and_five(self):
        # Setup
        dice = [1, 3, 5, 6, 1]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(250, score)
        self.assertTrue(is_covered)

    def test_scoring_one_and_two_fives(self):
        # Setup
        dice = [1, 3, 5, 6, 5]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(200, score)
        self.assertTrue(is_covered)

    def test_scoring_three_ones(self):
        # Setup
        dice = [1, 1, 6, 1, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(1000, score)
        self.assertFalse(is_covered)

    def test_scoring_three_fives(self):
        # Setup
        dice = [5, 5, 6, 5, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(500, score)
        self.assertFalse(is_covered)

    def test_scoring_three_threes(self):
        # Setup
        dice = [3, 3, 6, 3, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(300, score)
        self.assertFalse(is_covered)

    def test_scoring_four_ones(self):
        # Setup
        dice = [1, 1, 1, 1, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(2000, score)
        self.assertFalse(is_covered)

    def test_scoring_four_fives(self):
        # Setup
        dice = [5, 5, 6, 5, 5]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(1000, score)
        self.assertFalse(is_covered)

    def test_scoring_four_threes(self):
        # Setup
        dice = [3, 3, 6, 3, 3]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(600, score)
        self.assertFalse(is_covered)

    def test_scoring_three_fours_covered_with_one(self):
        # Setup
        dice = [4, 4, 6, 1, 4]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(500, score)
        self.assertTrue(is_covered)

    def test_scoring_three_sixes_covered_with_five(self):
        # Setup
        dice = [6, 5, 6, 2, 6]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(650, score)
        self.assertTrue(is_covered)

    def test_scoring_fewer_than_five_dice(self):
        # Setup
        dice = [1, 1, 1]
        dice_counter = Counter(dice)

        # Execute
        score, is_covered = self.engine._count_score(dice_counter)

        # Assert
        self.assertEqual(1000, score)
        self.assertFalse(is_covered)

if __name__ == '__main__':
    unittest.main()
