from enum import Enum

class Suit(Enum):
    SPADE = "♠"
    HEART = "♥"
    DIAMOND = "♦"
    CLUB = "♣"

class Card:
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.points = self.get_points()  # points for order and score

    def get_points(self):
        if self.rank == 'A':
            return 14
        if self.rank == 'K':
            return 13
        if self.rank == 'Q':
            return 12
        if self.rank == 'J':
            return 11
        return int(self.rank)

    def __str__(self):
        # simple text for one card, suit first
        return f"{self.suit.value}{self.rank}"

class CardType:
    # (name, base points, multiplier)
    HIGH_CARD = ("High card", 5, 1)
    PAIR = ("Pair", 10, 2)
    TWO_PAIR = ("Two pair", 20, 2)
    THREE = ("Three of a kind", 30, 3)
    STRAIGHT = ("Straight", 40, 4)
    FLUSH = ("Flush", 45, 4)
    FULL_HOUSE = ("Full house", 50, 5)
    FOUR = ("Four of a kind", 60, 6)
    STRAIGHT_FLUSH = ("Straight flush", 100, 8)
