from dataclasses import dataclass

@dataclass
class Frame:

    rolls: list

    def is_complete(self):
        return len(self.rolls) == 2 or self.all_pins_knocked_down()

    def total_pins(self):
        return sum(self.rolls)

    def is_spare(self):
        return len(self.rolls) == 2 and self.all_pins_knocked_down()

    def is_strike(self):
        return len(self.rolls) == 1 and self.all_pins_knocked_down()

    def all_pins_knocked_down(self):
        return self.total_pins() == 10

class BowlingGame:

    def __init__(self):
        self.frames = []

    def roll(self, pins):
        if self._is_first_roll() or self._previous_frame().is_complete():
            self.frames.append(Frame(rolls=[pins]))
        else:
            self._previous_frame().rolls.append(pins)

    def score(self):
        return sum(self._compute_frame_score(frame_num, frame) for frame_num, frame in enumerate(self.frames))

    def _compute_frame_score(self, frame_num, frame):
        return self._compute_completed_frame_score(frame_num, frame) if frame.is_complete() else 0

    def _compute_completed_frame_score(self, frame_num, frame):
        if frame.is_spare():
            return self._compute_spare_score(frame_num, frame)
        elif frame.is_strike():
            return self._compute_strike_score(frame_num, frame)
        else:
            return frame.total_pins()

    def _compute_spare_score(self, frame_num, frame):
        following_frame = self._get_frame(frame_num + 1)
        if following_frame:
            return frame.total_pins() + following_frame.rolls[0]
        else:
            return 0

    def _compute_strike_score(self, frame_num, frame):
        following_frames = self.frames[frame_num + 1:]
        following_rolls = [roll for frame in following_frames for roll in frame.rolls]
        if len(following_rolls) >= 2:
            return frame.total_pins() + sum(following_rolls[:2])
        else:
            return 0

    def _previous_frame(self):
        return self.frames[-1]

    def _get_frame(self, frame_num):
        try:
            return self.frames[frame_num]
        except IndexError:
            return None

    def _is_first_roll(self):
        return not self.frames