from dataclasses import dataclass

@dataclass
class Frame:

    PINS_PER_FRAME = 10

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
        return self.total_pins() == self.PINS_PER_FRAME

class GameFinishedException(ValueError):
    pass

class BowlingGame:

    FRAMES_PER_MATCH = 10

    def __init__(self):
        self._frames = []

    def roll(self, pins):
        if self._roll_permitted():
            self._apply_roll(pins)
        else:
            raise GameFinishedException("The game is finished, you cannot make any more rolls.")
    
    def _roll_permitted(self):
        return (
            (not self._completed_ten_frames()) or
            (self._completed_ten_frames() and self._tenth_frame().is_spare() and len(self._bonus_rolls()) <= 1) or
            (self._completed_ten_frames() and self._tenth_frame().is_strike() and len(self._bonus_rolls()) <= 2)
        )

    def _apply_roll(self, pins):
        if self._is_first_roll() or self._last_frame().is_complete():
            self._frames.append(Frame(rolls=[pins]))
        else:
            self._last_frame().rolls.append(pins)

    def score(self):
        return sum(self._compute_frame_score(frame_index, frame) for frame_index, frame in enumerate(self._frames[:self.FRAMES_PER_MATCH]))

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
        rolls = self._rolls_since(frame_index)
        if len(rolls) >= num_rolls:
            return rolls[:num_rolls]
        else:
            return None

    def _rolls_since(self, frame_index):
        """
        Returns all the rolls that have occurred after the completion of the specified frame.
        """
        following_frames = self._frames[frame_index + 1:]
        return [roll for frame in following_frames for roll in frame.rolls]

    def _bonus_rolls(self):
        """
        Return the rolls that have occurred since the completion of the tenth frame.
        """
        return self._rolls_since(9)

    def _last_frame(self):
        return self._frames[-1]

    def _completed_ten_frames(self):
        tenth_frame = self._frame_or_none(9)
        return tenth_frame is not None and tenth_frame.is_complete()

    def _frame_or_none(self, index):
        try:
            return self._frames[index]
        except IndexError:
            return None

    def _is_first_roll(self):
        return not self._frames
