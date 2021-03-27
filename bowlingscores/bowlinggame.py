from dataclasses import dataclass

@dataclass
class Frame:

    rolls: list

    def is_complete(self):
        return len(self.rolls) == 2 or self.total_pins == 10

    def total_pins(self):
        return sum(self.rolls)

    def is_spare(self):
        return sum(self.rolls) == 10

class BowlingGame:

    def __init__(self):
        self.frames = []

    def roll(self, pins):
        if self._is_first_roll() or self._previous_frame().is_complete():
            self.frames.append(Frame(rolls=[pins]))
        else:
            self._previous_frame().rolls.append(pins)

    def score(self):
        score = 0
        for index, frame in enumerate(self.frames):
            if frame.is_complete():
                if frame.is_spare():
                    following_frame = self._get_frame(index + 1)
                    if following_frame:
                        frame_score = frame.total_pins() + following_frame.rolls[0]
                else:
                    frame_score = frame.total_pins()
                score += frame_score
        return score

    def _previous_frame(self):
        return self.frames[-1]

    def _get_frame(self, index):
        try:
            return self.frames[index]
        except IndexError:
            return None

    def _is_first_roll(self):
        return not self.frames