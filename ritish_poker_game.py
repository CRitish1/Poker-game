import random
import unittest
from collections import Counter

class PokerHand:
    RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
    SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    HAND_RANKS = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
        "Royal Flush"
    ]

    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("Exactly 5 cards are required to form a poker hand.")
        self.cards = cards

    def get_rank(self):
        counts = Counter()
        suits = Counter()
        for rank, suit in self.cards:
            counts[rank] += 1
            suits[suit] += 1

        is_straight = self.is_straight(list(counts.keys()))
        is_flush = any(count == 5 for count in suits.values())
        has_ace = self.RANKS[-1] in counts

        if is_straight and is_flush and has_ace:
            return "Royal Flush"
        elif is_straight and is_flush:
            return "Straight Flush"
        elif 4 in counts.values():
            return "Four of a Kind"
        elif 3 in counts.values() and 2 in counts.values():
            return "Full House"
        elif is_flush:
            return "Flush"
        elif is_straight:
            return "Straight"
        elif 3 in counts.values():
            return "Three of a Kind"
        elif list(counts.values()).count(2) == 2:
            return "Two Pair"
        elif 2 in counts.values():
            return "One Pair"
        return "High Card"

    def is_straight(self, ranks):
        rank_indices = sorted(self.RANKS.index(rank) for rank in ranks)
        return all(rank_indices[i] - rank_indices[i - 1] == 1 for i in range(1, len(rank_indices)))

    def __lt__(self, other):
        return self.HAND_RANKS.index(self.get_rank()) < self.HAND_RANKS.index(other.get_rank())

    def __repr__(self):
        return f'{" ".join(f"{rank} of {suit}" for rank, suit in self.cards)}: {self.get_rank()}'

def create_deck():
    return [(rank, suit) for suit in PokerHand.SUITS for rank in PokerHand.RANKS]

def deal_cards(deck, num_hands):
    random.shuffle(deck)
    return [PokerHand([deck.pop() for _ in range(5)]) for _ in range(num_hands)]

def poker_game(num_players):
    print("Welcome to RITISH's Poker Game!")
    deck = create_deck()
    hands = deal_cards(deck, num_players)
    for index, hand in enumerate(hands, start=1):
        print(f"Player {index}: {hand}")
    winning_hand = max(hands)
    print(f"The winning hand is: {winning_hand}")

# Test cases for PokerHand
class TestPokerHand(unittest.TestCase):
    def test_royal_flush(self):
        hand = PokerHand([('Ace', 'Hearts'), ('King', 'Hearts'), ('Queen', 'Hearts'), ('Jack', 'Hearts'), ('10', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Royal Flush")

    def test_straight_flush(self):
        hand = PokerHand([('9', 'Clubs'), ('8', 'Clubs'), ('7', 'Clubs'), ('6', 'Clubs'), ('5', 'Clubs')])
        self.assertEqual(hand.get_rank(), "Straight Flush")

    def test_four_of_a_kind(self):
        hand = PokerHand([('Ace', 'Hearts'), ('Ace', 'Diamonds'), ('Ace', 'Clubs'), ('Ace', 'Spades'), ('2', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Four of a Kind")

    def test_full_house(self):
        hand = PokerHand([('Ace', 'Hearts'), ('Ace', 'Diamonds'), ('Ace', 'Clubs'), ('King', 'Spades'), ('King', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Full House")

    def test_flush(self):
        hand = PokerHand([('2', 'Hearts'), ('4', 'Hearts'), ('6', 'Hearts'), ('8', 'Hearts'), ('10', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Flush")

    def test_straight(self):
        hand = PokerHand([('Ace', 'Hearts'), ('King', 'Diamonds'), ('Queen', 'Clubs'), ('Jack', 'Spades'), ('10', 'Clubs')])
        self.assertEqual(hand.get_rank(), "Straight")

    def test_three_of_a_kind(self):
        hand = PokerHand([('Ace', 'Hearts'), ('Ace', 'Diamonds'), ('Ace', 'Clubs'), ('King', 'Spades'), ('2', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Three of a Kind")

    def test_two_pair(self):
        hand = PokerHand([('Ace', 'Hearts'), ('Ace', 'Diamonds'), ('King', 'Clubs'), ('King', 'Spades'), ('2', 'Hearts')])
        self.assertEqual(hand.get_rank(), "Two Pair")

    def test_one_pair(self):
        hand = PokerHand([('Ace', 'Hearts'), ('Ace', 'Diamonds'), ('King', 'Clubs'), ('Queen', 'Spades'), ('2', 'Hearts')])
        self.assertEqual(hand.get_rank(), "One Pair")

    def test_high_card(self):
        hand = PokerHand([('Ace', 'Hearts'), ('2', 'Diamonds'), ('3', 'Clubs'), ('5', 'Spades'), ('7', 'Hearts')])
        self.assertEqual(hand.get_rank(), "High Card")

# Running the tests
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
    # Uncomment the next line to play the game with 4 players
    # poker_game(4)
