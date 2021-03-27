from unittest import TestCase
from bowlingscores import BowlingGame

class TestBowlingGame(TestCase):

    def setUp(self):
        self.game = BowlingGame()

    def test_roll_zero(self):
        self.game.roll(0)
        self.assertEqual(self.game.score(), 0)

    def test_first_frame_incomplete(self):
        self.game.roll(5)
        self.assertEqual(self.game.score(), 0, msg="Score should not increment until frame is complete")

    def test_first_frame_complete(self):
        self.game.roll(5)
        self.game.roll(2)
        self.assertEqual(self.game.score(), 7, msg="Score should be incremented once frame complete")