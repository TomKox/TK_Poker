import collections
import random
from enum import Enum, unique


@unique
class Suit(Enum):
    SPADES = 1
    HEARTS = 2
    CLUBS = 3
    DIAMONDS = 4

    def __str__(self):
        return str(self.name).capitalize()

    def short(self):
        return str(self).lower()[:1]


@unique
class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __str__(self):
        return str(self.name).capitalize()

    def short(self):
        if self.value in range(2, 10):
            return str(self.value)
        else:
            return str(self.name)[:1]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return str(self.rank) + ' of ' + str(self.suit)

    # self == other
    def __eq__(self, other):
        return self.rank == other.rank

    # self != other
    def __ne__(self, other):
        return self.rank != other.rank

    # self < other
    def __lt__(self, other):
        if self.rank == Rank.ACE:
            self_rank = 14
        else:
            self_rank = self.rank.value

        if other.rank == Rank.ACE:
            other_rank = 14
        else:
            other_rank = other.rank.value

        return self_rank < other_rank

    # self <= other
    def __le__(self, other):
        if self < other:
            return True
        else:
            return self == other

    # self > other
    def __gt__(self, other):
        if self == other:
            return False
        else:
            return not self < other

    # self >= other
    def __ge__(self, other):
        if self > other:
            return True
        else:
            return self == other

    def short(self):
        return str('[' + self.rank.short() + self.suit.short() + ']')


class Deck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in Suit for rank in Rank]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self):
        return self._cards.pop(0)


@unique
class Ranking(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    # self == other
    def __eq__(self, other):
        return self.value == other.value

    # self != other
    def __ne__(self, other):
        return self.value != other.value

    # self < other
    def __lt__(self, other):
        return self.value < other.value

    # self <= other
    def __le__(self, other):
        return self.value <= other.value

    # self > other
    def __gt__(self, other):
        return self.value > other.value

    # self >= other
    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return self.name.replace('_',' ').title()


class Holding:
    def __init__(self, cards):
        self._cards = list(cards)

    def define(self):
        specifiers = dict()

        cards = self._cards


def get_most_common_suit(cards):
    cards_per_suit = dict([
        (Suit.SPADES, []),
        (Suit.HEARTS, []),
        (Suit.CLUBS, []),
        (Suit.DIAMONDS, [])
    ])
    for card in cards:
        cards_per_suit[card.suit].append(card)

    for s in cards_per_suit:
        suited_cards = cards_per_suit[s]
        print(s)
        suited_cards_string = ''
        for card in suited_cards:
            suited_cards_string = suited_cards_string + card.short()
        print(suited_cards_string)



deck = Deck()
deck.shuffle()

card1 = deck.deal()
card2 = deck.deal()
card3 = deck.deal()
card4 = deck.deal()
card5 = deck.deal()
card6 = deck.deal()
card7 = deck.deal()

seven_cards = [card1, card2, card3, card4, card5, card6, card7]
cards_string = ''
for card in seven_cards:
    cards_string = cards_string + card.short()

print(cards_string)
get_most_common_suit(seven_cards)