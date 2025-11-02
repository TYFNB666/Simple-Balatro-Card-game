

### How to run

* Make sure you have Python 3.9+.
* Open a terminal in this folder.
* Run:

  * Windows: `py main.py`  or `python main.py`
  * macOS/Linux: `python3 main.py`

### Files

* `main.py` – program entry (start the game)
* `game.py` – game loop and actions (play, discard, draw, show)
* `cards.py` – card, suit, and hand types
* `scoring.py` – hand check and score logic

### Basic rules (quick)

* Start hand: **7 cards**
* Each play: choose **1–5** cards to play
* You have **4 plays** and **4 discards** in total


### Change settings (optional)

Open `game.py`:

* `HAND_SIZE = 7`  // hand size
* `plays_left = 4`
* `discards_left = 4`

