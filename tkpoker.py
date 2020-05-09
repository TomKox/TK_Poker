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

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


class Holding:
    def __init__(self, cards):
        self._cards = list(cards)

    def define(self):
        specifiers = dict()

        cards = self._cards

        if check_royal_flush(cards):
            self._ranking = Ranking.ROYAL_FLUSH

        elif check_straight_flush(cards):
            self._ranking = Ranking.STRAIGHT_FLUSH
            flushcards = get_flushcards_from(cards)

        elif check_four_of_a_kind(cards):
            self._ranking = Ranking.FOUR_OF_A_KIND

        elif check_full_house(cards):
            self._ranking = Ranking.FULL_HOUSE

        elif check_flush(cards):
            self._ranking = Ranking.FLUSH

        elif check_straight(cards):
            self._ranking = Ranking.STRAIGHT

        elif check_three_of_a_kind(cards):
            self._ranking = Ranking.THREE_OF_A_KIND

        elif check_two_pair(cards):
            self._ranking = Ranking.TWO_PAIR

        elif check_pair(cards):
            self._ranking = Ranking.PAIR

        else:
            self._ranking = Ranking.HIGH_CARD


def count_by_ranks(cards):
    rank_counter = collections.Counter()
    for card in cards:
        rank_counter[card.rank] += 1
    return rank_counter


def check_pair(cards):
    counter = count_by_ranks(cards)
    for card in cards:
        if counter[card.rank] == 2:
            return True
    return False


def check_two_pair(cards):
    counter_most_common = count_by_ranks(cards).most_common(2)
    if counter_most_common[1][1] == 2:
        return True
    else:
        return False


def check_three_of_a_kind(cards):
    counter_most_common = count_by_ranks(cards).most_common(1)
    if counter_most_common[0][1] == 3:
        return True
    else:
        return False


def get_sequence_string(cards):
    # build a string from all ranks
    cards = list(cards)
    cards.sort(key=None, reverse=True)
    cards_seq_string = ''
    for card in cards:
        cards_seq_string += card.short()[1:2]

    # remove duplicates
    cards_seq_string = ''.join(
        sorted(set(cards_seq_string), key=cards_seq_string.index))

    return cards_seq_string


def check_straight(cards):
    cards_seq_string = get_sequence_string(cards)
    seq_length = len(cards_seq_string)
    if seq_length < 5:
        return False

    # Ace can be high or low!
    if cards_seq_string[0:1] == 'A':
        cards_seq_string += 'A'
        seq_length += 1

    for i in range(5, seq_length + 1):
        all_ranks = 'AKQJT98765432A'
        search_string = cards_seq_string[i - 5:i]
        found = all_ranks.find(search_string)
        if found != -1:
            return True

    return False


def get_most_common_suit(cards):
    suit_counter = collections.Counter()
    for card in cards:
        suit_counter[card.suit] += 1

    return suit_counter.most_common(1)[0]


def check_flush(cards):
    if len(cards) < 5:
        return False

    most_suit = get_most_common_suit(cards)
    if most_suit[1] >= 5:
        return True
    else:
        return False


def get_flushcards_from(cards):
    if len(cards) < 5:
        return None
    cards = list(cards)
    cards.sort(key=None, reverse=True)
    flushsuit = get_most_common_suit(cards)[0]
    flushcards = []
    for card in cards:
        if card.suit == flushsuit:
            flushcards.append(card)
    if len(flushcards) < 5:
        return None
    else:
        return flushcards


def check_full_house(cards):
    counter_most_common = count_by_ranks(cards).most_common(2)
    if counter_most_common[0][1] == 3 and counter_most_common[1][1] == 2:
        return True
    else:
        return False


def check_four_of_a_kind(cards):
    counter_most_common = count_by_ranks(cards).most_common(1)
    if counter_most_common[0][1] == 4:
        return True
    else:
        return False


def check_straight_flush(cards):
    if check_flush(cards):
        flushcards = get_flushcards_from(cards)
        return check_straight(flushcards)
    else:
        return False


def check_royal_flush(cards):
    if check_straight_flush(cards):
        flushcards = get_flushcards_from(cards)
        seq_string = get_sequence_string(flushcards)
        if seq_string.find('AKQJT') != -1:
            return True
        else:
            return False
    else:
        return False


deck = Deck()
deck.shuffle()

# for card in deck:
#    print(card.short() + " " + str(card))

# card1 = deck.deal()
# card2 = deck.deal()
# card3 = deck.deal()
# card4 = deck.deal()
# card5 = deck.deal()
# card6 = deck.deal()
# card7 = deck.deal()

card1 = Card(Rank.ACE, Suit.SPADES)
card2 = Card(Rank.KING, Suit.SPADES)
card3 = Card(Rank.QUEEN, Suit.SPADES)
card4 = Card(Rank.TEN, Suit.SPADES)
card5 = Card(Rank.JACK, Suit.SPADES)
card6 = Card(Rank.TWO, Suit.SPADES)
card7 = Card(Rank.THREE, Suit.SPADES)

# comp_eq = card1 == card2
# print(card1.short() + " == " + card2.short() + ": " + str(comp_eq))

# comp_ne = card1 != card2
# print(card1.short() + " != " + card2.short() + ": " + str(comp_ne))

# comp_lt = card1 < card2
# print(card1.short() + " <  " + card2.short() + ": " + str(comp_lt))

# comp_le = card1 <= card2
# print(card1.short() + " <= " + card2.short() + ": " + str(comp_le))

# comp_gt = card1 > card2
# print(card1.short() + " >  " + card2.short() + ": " + str(comp_gt))

# comp_ge = card1 >= card2
# print(card1.short() + " >= " + card2.short() + ": " + str(comp_ge))

seven_cards = [card1, card2, card3, card4, card5, card6, card7]
cards_string = ''
for card in seven_cards:
    cards_string = cards_string + card.short()

print(cards_string)
print('Pair: ' + str(check_pair(seven_cards)))
print('Two Pair: ' + str(check_two_pair(seven_cards)))
print('Three of a Kind: ' + str(check_three_of_a_kind(seven_cards)))
print('Straight: ' + str(check_straight(seven_cards)))
print('Flush: ' + str(check_flush(seven_cards)))
print('Full House: ' + str(check_full_house(seven_cards)))
print('Straight Flush: ' + str(check_straight_flush(seven_cards)))
print('Royal Flush: ' + str(check_royal_flush(seven_cards)))
