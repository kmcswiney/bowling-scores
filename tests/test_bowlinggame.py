from unittest import TestCase
from bowlingscores import BowlingGame, GameFinishedException

class TestBowlingGame(TestCase):

    def setUp(self):
        self.game = BowlingGame()

    def roll(self, rolls):
        for pins in rolls:
            self.game.roll(pins)

    def test_roll_zero(self):
        self.game.roll(0)
        self.assertEqual(self.game.score(), 0)

    def test_first_frame_incomplete(self):
        self.game.roll(5)
        self.assertEqual(self.game.score(), 0, msg="Score should not update until frame is complete")

    def test_first_frame_complete(self):
        self.roll([4, 4])
        self.assertEqual(self.game.score(), 8, msg="Score should be updated once frame complete")

    def test_multiple_frames(self):
        self.roll([5, 2, 1, 4, 7])
        self.assertEqual(self.game.score(), 12)

    def test_spare(self):
        self.roll([4, 6, 5, 0])
        self.assertEqual(
            self.game.score(),
            20,
            msg="The score for a spare should be the number of pins knocked down in the spare frame "
                "plus the number of pins knocked down in the following roll"
        )

    def test_spare_score_not_applied_until_following_roll(self):
        self.roll([3, 5, 4, 6])
        self.assertEqual(
            self.game.score(),
            8,
            msg="Score should not take in to account the spare frame as the following roll has not happened yet"
        )

    def test_strike(self):
        self.roll([10, 5, 4])
        self.assertEqual(
            self.game.score(),
            28,
            msg="The score for a strike should be the number of pins knocked down in the strike frame "
                "plus the number of pins knocked down in the next two rolls"
        )

    def test_strike_score_not_applied_until_following_2_rolls(self):
        self.roll([3, 5, 10, 5])
        self.assertEqual(
            self.game.score(),
            8,
            msg="Score should not take in to account the strike frame as the following 2 rolls have not happened yet"
        )

    def test_multiple_spares(self):
        self.roll([6, 4, 7, 3, 3, 2])
        self.assertEqual(self.game.score(), (6 + 4 + 7) + (7 + 3 + 3) + 3 + 2)

    def test_multiple_strikes(self):
        self.roll([10, 10, 7, 2])
        self.assertEqual(self.game.score(), (10 + 10 + 7) + (10 + 7 + 2) + (7 + 2))

    def test_full_game(self):
        self.roll(
            [
                5, 3,
                10,
                4, 4,
                7, 3,
                2, 5,
                8, 1,
                6, 3,
                3, 5,
                2, 6,
                6, 3
            ]
        )
        self.assertEqual(
            self.game.score(),
            (
                (5 + 3) +
                (10 + 4 + 4) +
                (4 + 4) + 
                (7 + 3 + 2) +
                (2 + 5) +
                (8 + 1) +
                (6 + 3) +
                (3 + 5) +
                (2 + 6) +
                (6 + 3)
            )
        )

    def test_ensure_no_rolls_after_game_finished(self):
        self.roll([4] * 20)
        with self.assertRaises(GameFinishedException):
            self.roll([5])

    def test_bonus_roll_after_last_frame_spare(self):
        eighteen_ones = [1] * 18
        self.roll(eighteen_ones)
        self.roll([7, 3])
        self.roll([5])
        self.assertEqual(self.game.score(), 18 + (7 + 3 + 5))
        with self.assertRaises(GameFinishedException):
            self.roll([7])

    def test_bonus_roll_after_last_frame_strike(self):
        eighteen_ones = [1] * 18
        self.roll(eighteen_ones)
        self.roll([10])
        self.roll([5, 2])
        self.assertEqual(self.game.score(), 18 + (10 + 5 + 2))
        with self.assertRaises(GameFinishedException):
            self.roll([7])

    def test_all_strikes(self):
        twelve_strikes = [10] * 12
        self.roll(twelve_strikes)
        self.assertEqual(self.game.score(), 300)
        with self.assertRaises(GameFinishedException):
            self.roll([7])



        