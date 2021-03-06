from dataclasses import dataclass

class GameFinishedException(ValueError):
    pass

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

class BowlingGame:

    FRAMES_PER_MATCH = 10

    def __init__(self):
        self._frames = []

    def roll(self, pins):
        if self._roll_permitted():
            self._apply_roll(pins)
        else:
            raise GameFinishedException("The game is finished, you cannot make any more rolls.")

    def score(self):
        return sum(
            self._frame_score(frame_index, frame)
            for frame_index, frame in enumerate(self._frames[:self.FRAMES_PER_MATCH])
            if frame.is_complete()
        )
    
    def _roll_permitted(self):
        return (
            not self._completed_ten_frames() or
            (self._completed_ten_frames() and self._tenth_frame().is_spare() and len(self._bonus_rolls()) < 1) or
            (self._completed_ten_frames() and self._tenth_frame().is_strike() and len(self._bonus_rolls()) < 2)
        )

    def _apply_roll(self, pins):
        if self._is_first_roll() or self._last_frame().is_complete():
            self._frames.append(Frame(rolls=[pins]))
        else:
            self._last_frame().rolls.append(pins)

    def _frame_score(self, frame_index, frame):
        if frame.is_spare():
            return self._frame_pins_plus_following(frame_index, frame, 1)
        elif frame.is_strike():
            return self._frame_pins_plus_following(frame_index, frame, 2)
        else:
            return frame.total_pins()

    def _frame_pins_plus_following(self, frame_index, frame, num_following_rolls):
        """ 
        Given a frame, return the pins knocked down in that frame plus
        the number of pins knocked down in the subsequent num_following_rolls rolls.
        If the following rolls have not occurred yet, return zero.
        """
        following_rolls = self._rolls_since(frame_index)[:num_following_rolls]
        if len(following_rolls) == num_following_rolls:
            return frame.total_pins() + sum(following_rolls)
        else:
            return 0

    def _rolls_since(self, frame_index):
        """
        Returns all the rolls that have occurred since the completion of the specified frame.
        """
        following_frames = self._frames[frame_index + 1:]
        return [roll for frame in following_frames for roll in frame.rolls]

    def _bonus_rolls(self):
        """
        Return the rolls that have occurred since the tenth frame.
        """
        return self._rolls_since(9)

    def _last_frame(self):
        return self._frames[-1]

    def _tenth_frame(self):
        try:
            return self._frames[9]
        except IndexError:
            return None

    def _completed_ten_frames(self):
        return self._tenth_frame() is not None and self._tenth_frame().is_complete()

    def _is_first_roll(self):
        return not self._frames
