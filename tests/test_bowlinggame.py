from unittest import TestCase
from bowlingscores import BowlingGame

class TestBowlingGame(TestCase):

    def setUp(self):
        self.game = BowlingGame()

    def test_roll_zero(self):
        self.game.roll(0)
        self.assertEqual(self.game.score(), 0)
