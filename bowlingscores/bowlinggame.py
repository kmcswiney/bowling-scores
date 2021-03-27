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
        self._frames = []

    def roll(self, pins):
        if self._is_first_roll() or self._previous_frame().is_complete():
            self._frames.append(Frame(rolls=[pins]))
        else:
            self._previous_frame().rolls.append(pins)

    def score(self):
        return sum(self._compute_frame_score(frame_index, frame) for frame_index, frame in enumerate(self._frames))

    def _compute_frame_score(self, frame_index, frame):
        return self._compute_completed_frame_score(frame_index, frame) if frame.is_complete() else 0

    def _compute_completed_frame_score(self, frame_index, frame):
        if frame.is_spare():
            return self._compute_spare_score(frame_index, frame)
        elif frame.is_strike():
            return self._compute_strike_score(frame_index, frame)
        else:
            return frame.total_pins()

    def _compute_spare_score(self, frame_index, frame):
        following_roll = self._next_rolls(frame_index, 1)
        if following_roll:
            return frame.total_pins() + sum(following_roll)
        else:
            return 0

    def _compute_strike_score(self, frame_index, frame):
        following_2_rolls = self._next_rolls(frame_index, 2)
        if following_2_rolls:
            return frame.total_pins() + sum(following_2_rolls)
        else:
            return 0

    def _next_rolls(self, frame_index, num_rolls):
        """ 
        Given a frame index number, return the following num_rolls rolls that occurred after the given frame.
        If the specified number of rolls have not occurred yet, return None.
        """
        following_frames = self._frames[frame_index + 1:]
        rolls = [roll for frame in following_frames for roll in frame.rolls]
        if len(rolls) >= num_rolls:
            return rolls[:num_rolls]
        else:
            return None

    def _previous_frame(self):
        return self._frames[-1]

    def _is_first_roll(self):
        return not self._frames
