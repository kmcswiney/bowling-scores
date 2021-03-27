from dataclasses import dataclass

@dataclass
class Frame:

    rolls: list

    def is_complete(self):
        return len(self.rolls) == 2 or self.score == 10

    def score(self):
        return sum(self.rolls)
    

class BowlingGame:

    def __init__(self):
        self.frames = []

    def roll(self, pins):
        if self._is_first_roll() or self._previous_frame().is_complete():
            self.frames.append(Frame(rolls=[pins]))
        else:
            self._previous_frame().rolls.append(pins)

    def score(self):
        return sum(frame.score() for frame in self.frames if frame.is_complete())

    def _previous_frame(self):
        return self.frames[-1]

    def _is_first_roll(self):
        return not self.frames