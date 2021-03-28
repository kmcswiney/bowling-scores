# Bowling Scoring System
A simple package that implements a bowling scoring system.

# Usage

Requires Python 3.7 or higher. There are no dependencies outside of the Python stdlib.

Can be installed as a package using:

```
pip install .
```

To use the BowlingGame functionality:

```python
from bowlingscores import BowlingGame

game = BowlingGame()
game.roll(5) # First roll knocks down 5 pins
game.roll(2) # Second roll knocks down 2 pins
game.score() # After completion of the first frame, game score returns 7
```

The score can be computed at any point in the game and will handle strikes, spares, and the special cases for additional rolls in the tenth frame.

When the game is over and no more balls can be rolled, attempting to call `game.roll()` will raise a GameFinishedException.

# Running the tests
From the root of the repository run:
```
python setup.py test
```