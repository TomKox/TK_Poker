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

class Hole_Cards:
    pass

class Holding:
    def __init__(self, cards):
        self._cards = list(cards)

    def define(self):
        specifiers = dict()

        cards = self._cards


# get all the cards of the same suit, if there are 5 or more
def get_flushcards(cards):
    cards_per_suit = dict([
        (Suit.SPADES, []),
        (Suit.HEARTS, []),
        (Suit.CLUBS, []),
        (Suit.DIAMONDS, [])
    ])
    for card in cards:
        cards_per_suit[card.suit].append(card)

    flush = []
    for s in cards_per_suit:
        suited_cards = cards_per_suit[s]

        if len(suited_cards) >= 5:
            flush = suited_cards

    if len(flush) >= 5:
        return flush
    else:
        return None

# get the highest straight out of the cards, or None if there is no straight
def get_straightcards(cards):
    straight = []
    cards = list(cards)
    ranks = get_by_rank(cards)
    
    # get all single unique cards
    uniques = []
    for r in ranks:
        uniques.append(ranks[r][0])
    
    # can't be straight, if there's less than 5 cards
    if len(uniques) < 5:
        return None

    # sort the uniques from low to high 
    # (careful later on: Ace can be high or low!)
    uniques.sort()

    ace = False
    if uniques[-1].rank == Rank.ACE:
        ace = True

    # check ace-high straight
    if ace:
        if uniques[-2].rank == Rank.KING and \
            uniques[-3].rank == Rank.QUEEN and \
            uniques[-4].rank == Rank.JACK and \
            uniques[-5].rank == Rank.TEN:
                straight.append(uniques[-1])
                straight.append(uniques[-2])
                straight.append(uniques[-3])
                straight.append(uniques[-4])
                straight.append(uniques[-5])
                return straight
        # no ace-high straight, so let the ace be low: 
        # the uniques list is sorted and we move the ace to the front
        else:
            a = uniques[-1]
            uniques.insert(0,a)
            del uniques[-1]

    n = len(uniques)
    for i in range(n-1, 3, -1):
        # print('checking ' + uniques[i].short())
        if uniques[i].rank.value - uniques[i-4].rank.value == 4:
            # print('straight found')
            straight.append(uniques[i])
            straight.append(uniques[i-1])
            straight.append(uniques[i-2])
            straight.append(uniques[i-3])
            straight.append(uniques[i-4])
            return straight
    
    return None

# get four of a kind, plus a kicker.  
# None is returned if not four of a kind.
def get_four_of_a_kind(cards):
    hand = []
    cards = list(cards)
    ranks = get_by_rank(cards)
    
    kicker = None
    for r in ranks:
        if len(ranks[r]) == 4:
            for card in ranks[r]:
                hand.append(card)
        else:
            if kicker is None:
                kicker = ranks[r][0]
            else:
                if ranks[r][0] > kicker:
                    kicker = ranks[r][0]
    hand.append(kicker)

    if len(hand) == 5:
        return hand
    else:
        return None

def get_full_house(cards):
    pass

# get Three of a Kind, plus kickers.
# Warning: If you want to assume kickers are correct, make sure that input cards are not Full House!!!
def get_three_of_a_kind(cards):
    cards = list(cards)
    ranks = get_by_rank(cards)

    best = []
    kickers = []

    for r in ranks:
        if len(ranks[r]) == 3:
            if len(best) == 0:
                best = ranks[r]
            else:
                if ranks[r][0].rank > best[0].rank:
                    best = ranks[r]
        
        if len(ranks[r]) == 1:
            kickers.append(ranks[r][0])

    kickers.sort()
    if len(kickers) >= 2:
        best.append(kickers[-1])
        best.append(kickers[-2])
    else:
        return None

    if len(best) == 5:
        return best
    else:
        return None

def get_two_pair(cards):
    pass

def get_pair(cards):
    pass

def get_high_card(cards):
    pass


# returns a dictionary with Rank as Key, and a list of all cards of that Rank as Value
def get_by_rank(cards):
    cards = list(cards)
    cards.sort()
    ranks = dict()

    # Create dictionary with all ranks as keys
    for r in Rank:
        ranks[r]=[]

    # Add cards to the dictionary
    for card in cards:
        ranks[card.rank].append(card)

    # Remove empty dictionary entries
    for r in Rank:
        if len(ranks[r]) == 0:
            del ranks[r]

    return ranks


# TESTCODE HERE:
continue_loop = True
while continue_loop:
    print('------------------------------------------')
    deck = Deck()
    deck.shuffle()
    
    card1 = deck.deal()
    card2 = deck.deal()
    card3 = deck.deal()
    card4 = deck.deal()
    card5 = deck.deal()
    card6 = deck.deal()
    card7 = deck.deal()

    # card1 = Card(Rank.ACE, Suit.SPADES)
    # card2 = Card(Rank.QUEEN, Suit.SPADES)
    # card3 = Card(Rank.KING, Suit.DIAMONDS)
    # card4 = Card(Rank.TEN, Suit.CLUBS)
    # card5 = Card(Rank.JACK, Suit.SPADES)
    # card6 = Card(Rank.FIVE, Suit.HEARTS)
    # card7 = Card(Rank.ACE, Suit.HEARTS)

    # card1 = Card(Rank.NINE, Suit.SPADES)
    # card2 = Card(Rank.FOUR, Suit.SPADES)
    # card3 = Card(Rank.NINE, Suit.HEARTS)
    # card4 = Card(Rank.THREE, Suit.CLUBS)
    # card5 = Card(Rank.NINE, Suit.DIAMONDS)
    # card6 = Card(Rank.NINE, Suit.CLUBS)
    # card7 = Card(Rank.QUEEN, Suit.HEARTS)
    
    seven_cards = [card1, card2, card3, card4, card5, card6, card7]
    cards_string = ''
    for card in seven_cards:
        cards_string = cards_string + card.short()
    
    print(cards_string)
    
    # flush = get_flushcards(seven_cards)
    # if flush != None:
    #     continue_loop = False
    #     for card in flush:
    #         # print(card)
    #         pass

    # s = get_straightcards(seven_cards)
    # if s != None:
    #     continue_loop = False
    #     for card in s:
    #         print(card)

    # foak = get_four_of_a_kind(seven_cards)
    # if foak != None:
    #     for card in foak:
    #         print(card)
    #         continue_loop = False

    toak = get_three_of_a_kind(seven_cards)
    if toak != None:
        for card in toak:
            print(card)
            continue_loop = False

    