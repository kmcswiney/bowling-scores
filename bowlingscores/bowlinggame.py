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
        if not self.frames or self.frames[-1].is_complete():
            self.frames.append(Frame(rolls=[pins]))
        else:
            self.frames[-1].rolls.append(pins)

    def score(self):
        return sum(frame.score() for frame in self.frames if frame.is_complete())
