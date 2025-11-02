import random
from typing import List
from cards import Card, Suit
from scoring import evaluate_hand

HAND_SIZE = 7

SUIT_ORDER = {
    Suit.SPADE: 0,
    Suit.HEART: 1,
    Suit.DIAMOND: 2,
    Suit.CLUB: 3,
}

class Game:
    def __init__(self):
        self.total_score = 0
        self.hand: List[Card] = []  # cards in hand
        self.plays_left = 5  # how many times to play
        self.discards_left = 4  # how many times to discard
        self.deck = self.create_deck()

    def create_deck(self) -> List[Card]:
        # build a full deck then shuffle
        ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        deck = []
        for suit in Suit:
            for r in ranks:
                deck.append(Card(r, suit))
        random.shuffle(deck)
        return deck

    #reorder the cards
    def reorder_hand(self) -> None:
        self.hand.sort(key=lambda c: (SUIT_ORDER[c.suit], c.points))

    def draw_cards(self, num = 5):
        # draw num cards from the deck into hand
        for _ in range(num):
            if self.deck:
                self.hand.append(self.deck.pop())

    def play_cards(self, indices: List[int]):
        # play selected cards by indices then score and refill
        if self.plays_left <= 0:
            print("Your card-drawing turns have been exhausted!")
            return 0
        if not indices:
            print("No cards have been selected to be played.")
            return 0

        cards = [self.hand[i] for i in indices]
        cards_detail = [str(c) for c in cards]

        # use scoring_cards only
        card_type, base_points, base_mult, scoring_cards = evaluate_hand(cards)
        scoring_detail = [str(c) for c in scoring_cards]

        sum_points = sum(c.points for c in scoring_cards)
        total_points = base_points + sum_points
        final_score = total_points * base_mult

        # remove played cards
        for i in sorted(indices, reverse=True):
            self.hand.pop(i)

        # refill to 7
        need = HAND_SIZE - len(self.hand)
        if need > 0:
            self.draw_cards(need)

        self.plays_left -= 1
        self.total_score += final_score

        # show result
        print(f"The cards you played: {cards_detail}")
        print(f"Cards used for score: {scoring_detail}")
        print(f"Cards Type: {card_type}")
        print(f"Counting: ({base_points} + {sum_points}) × {base_mult} = {final_score}")
        print(f"Your score: {final_score}")
        print(f"Total score: {self.total_score}")
        print(f"{'='*50}")
        return final_score

    def discard_cards(self, indices: List[int]) -> None:
        # discard selected cards then refill to 7
        if self.discards_left <= 0:
            print("The number of card discards has been exhausted!")
            return
        if not indices:
            print("Cards not selected for discard")
            return

        discarded = [str(self.hand[i]) for i in indices]
        for i in sorted(indices, reverse=True):
            self.hand.pop(i)

        need = HAND_SIZE - len(self.hand)
        if need > 0:
            self.draw_cards(need)
        self.discards_left -= 1
        print(f"\nDiscard: {discarded}")
        print(f"Remaining discard card attempts: {self.discards_left}")

    def display_hand(self) -> None:
        self.reorder_hand()
        print("Cards in hand:", " ".join(f"[{i}]{c}" for i, c in enumerate(self.hand)))
        print(f"Remaining number of cards to be played: {self.plays_left}, Remaining discard card attempts: {self.discards_left}")
        print(f"Total score: {self.total_score}")
        print(f"{'='*50}")

    def show_final_result(self) -> None:
        print(f"\n{'='*60}")
        print("Game Over！")
        print(f"\nTotal score: {self.total_score}\n")
