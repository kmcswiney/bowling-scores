# Bowling Scoring System
A simple package that implements a bowling scoring system.

# Installation
Clone the repository then install with:
```python
pip install .
```

# Usage
```python
from bowlingscores import BowlingGame

game = BowlingGame()
game.roll(5)
game.roll(2)
game.score() # returns 7
```

# Running the tests
From the root of this repository run:
```
python setup.py test
```