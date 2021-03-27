from unittest import TestCase
from bowlingscores import BowlingGame

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
        self.assertEqual(self.game.score(), 0, msg="Score should not increment until frame is complete")

    def test_first_frame_complete(self):
        self.roll([5, 2])
        self.assertEqual(self.game.score(), 7, msg="Score should be incremented once frame complete")

    def test_multiple_frames(self):
        self.roll([5, 2, 1, 4, 7])
        self.assertEqual(self.game.score(), 12)

