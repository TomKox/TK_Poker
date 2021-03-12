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
    DEUCE = 2
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
        return str(self.name).replace('_',' ').title()

class Hole_Cards:
    def __init__(self, cards):
        self._cards = list(cards)

        self._cards.sort(reverse=True)

    def generic(self):
        c1 = self._cards[0].short()[1]
        c2 = self._cards[1].short()[1]
        if self._cards[0].suit == self._cards[1].suit:
            suited = True
        else:
            suited = False
        if self._cards[0].rank == self._cards[1].rank:
            pair = True
        else:
            pair = False

        generic_string = '[' + c1 + c2

        if pair:
            generic_string += ']'
            return generic_string
        else:
            if suited:
                generic_string += 's]'
            else:
                generic_string += 'o]'
            return generic_string




class Holding:
    def __init__(self, cards):
        self._cards = list(cards)
        self._pretty = ''

    def define(self):
        cards = list(self._cards)

        hand = get_royal_flush(cards)
        if hand != None:
            self._ranking = Ranking.ROYAL_FLUSH
            suit = hand[0].suit
            self._pretty = 'a Royal Flush of ' + str(suit)

        else:
            hand = get_straight_flush(cards)
            if hand != None:
                self._ranking = Ranking.STRAIGHT_FLUSH
                suit = hand[0].suit
                self._pretty = 'a Straight Flush of {suit}, {low} to {high}'.format(suit=suit, low=str(hand[0].rank), high=str(hand[4].rank))

            else:
                hand = get_four_of_a_kind(cards)
                if hand != None:
                    self._ranking = Ranking.FOUR_OF_A_KIND
                    rank = hand[0].rank
                    kicker = hand[4].rank
                    self._pretty = 'Four of a Kind, {rank}s, with a kicker {kicker}'.format(rank=rank, kicker=kicker)

                else:
                    hand = get_full_house(cards)
                    if hand != None:
                        self._ranking = Ranking.FULL_HOUSE
                        big = hand[0].rank
                        small = hand[4].rank
                        self._pretty = 'a Full House, {big}s full of {small}s'.format(big=big, small=small)

                    else:
                        hand = get_flush(cards)
                        if hand != None:
                            self._ranking = Ranking.FLUSH
                            suit = hand[0].suit
                            rank_string = ''
                            for h in hand:
                                rank_string = rank_string + str(h.rank) + ', '
                            rank_string = rank_string.rstrip(', ')
                            self._pretty = 'a Flush of {suit}, {ranks}'.format(suit=suit, ranks=rank_string)
                        
                        else:
                            hand = get_straightcards(cards)
                            if hand != None:
                                self._ranking = Ranking.STRAIGHT
                                self._pretty = 'a Straight, {low} to {high}'.format(low=str(hand[4].rank), high=str(hand[0].rank))
                            
                            else:
                                hand = get_three_of_a_kind(cards)
                                if hand != None:
                                    self._ranking = Ranking.THREE_OF_A_KIND
                                    self._pretty = 'Three of a Kind, {threes}s, with kickers {k1} and {k2}'.format(threes=str(hand[0].rank), k1=str(hand[3].rank), k2=str(hand[4].rank))

                                else:
                                    hand = get_two_pair(cards)
                                    if hand != None:
                                        self._ranking = Ranking.TWO_PAIR
                                        self._pretty = 'Two Pair, {high}s and {low}s, with a kicker {k}'.format(high=str(hand[0].rank), low=str(hand[2].rank), k=str(hand[4].rank))
                                    
                                    else:
                                        hand = get_pair(cards)
                                        if hand != None:
                                            self._ranking = Ranking.PAIR
                                            self._pretty = 'a Pair of {pair}s, with kickers {k1}, {k2} and {k3}'.format(pair=str(hand[0].rank), k1=str(hand[2].rank), k2=str(hand[3].rank), k3=str(hand[4].rank))

                                        else:
                                            hand = get_high_card(cards)
                                            self._ranking = Ranking.HIGH_CARD
                                            hc = str(hand[0].rank)
                                            k1 = str(hand[1].rank)
                                            k2 = str(hand[2].rank)
                                            k3 = str(hand[3].rank)
                                            k4 = str(hand[4].rank)
                                            self._pretty = 'a High Card, {hc}, with kickers {k1}, {k2}, {k3} and {k4}'.format(hc=hc, k1=k1, k2=k2, k3=k3, k4=k4)
            
        self._hand = hand
        self._pretty = self._pretty.replace('Sixs', 'Sixes')    

    def pretty(self):
        return self._pretty

    # self == other
    def __eq__(self, other):
        if self._ranking != other._ranking:
            return False
        else:
            for i in range(0,5):
                if self._hand[i] != other._hand[i]:
                    return False
            
            return True
    
    # self != other
    def __ne__(self, other):
        if self._ranking != other._ranking:
            return True
        else:
            for i in range(0,5):
                if self._hand[i] != other._hand[i]:
                    return True

            return False

    # self < other
    def __lt__(self, other):
        if self._ranking < other._ranking:
            return True
        elif self._ranking > other._ranking:
            return False
        else:
            for i in range(0,5):
                if self._hand[i] < other._hand[i]:
                    return True
                if self._hand[i] > other._hand[i]:
                    return False
            
            return False

    # self > other
    def __gt__(self, other):
        if self._ranking > other._ranking:
            return True
        elif self._ranking < other._ranking:
            return False
        else:
            for i in range(0,5):
                if self._hand[i] > other._hand[i]:
                    return True
                if self._hand[i] < other._hand[i]:
                    return False

            return False



def get_royal_flush(cards):
    cards = list(cards)
    royal_flush = get_straight_flush(cards)
    if royal_flush != None:
        royal_flush.sort()
        if royal_flush[-1].rank == Rank.ACE and royal_flush[-5].rank == Rank.TEN:
            royal_flush.reverse()
            return royal_flush
        else:
            return None
    else:
        return None


def get_straight_flush(cards):
    cards = list(cards)
    flushcards = get_flushcards(cards)
    straight_flush = get_straightcards(flushcards)
    return straight_flush


def get_flush(cards):
    cards = list(cards)
    flush = get_flushcards(cards)
    if flush != None:
        flush.sort(key=None, reverse=True)
        flush = flush[0:5]
        return flush
    else:
        return None


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

    if cards is None:
        return None

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

# get a full house from cards, or None if not full house.
def get_full_house(cards):
    cards = list(cards)
    tripple = get_three_of_a_kind(cards)
    if tripple != None:

        # special check: if it is already a full house!  
        # See also, exceptional case in get_three_of_a_kind()
        if tripple[-1] == tripple[-2]:
            return tripple
        else:
            del tripple[-1]
            del tripple[-1]
    else:
        return None

    pair = get_highest_pair(cards)
    full_house = []
    if pair != None:
        for card in tripple:
            full_house.append(card)
        for card in pair:
            full_house.append(card)
        return full_house
    else:
        return None


# get Three of a Kind, plus kickers.
# Warning: If you want to assume kickers are correct, make sure that input cards are not Full House!!!
def get_three_of_a_kind(cards):
    cards = list(cards)
    ranks = get_by_rank(cards)

    best = []
    second_best = []
    kickers = []

    for r in ranks:
        if len(ranks[r]) == 3:
            if len(best) == 0:
                best = ranks[r]
            elif len(best) == 3:
                if ranks[r][0] > best[0]:
                    second_best = best
                    best = ranks[r]
                else:
                    second_best = ranks[r]
        
        if len(ranks[r]) == 1:
            kickers.append(ranks[r][0])

    kickers.sort()
    if len(kickers) >= 2:
        best.append(kickers[-1])
        best.append(kickers[-2])
    elif len(best) == 3:
        # THIS SHOULD ONLY HAPPEN WHEN THERE ARE 2 SETS OF THREE CARDS (So, a full house)
        # OR TWO POSSIBLE FULL HOUSES (3 + 2HIGH) (3 + 2LOW)
        if len(second_best) == 3:
            best.append(second_best[0])
            best.append(second_best[1])
            return best
        else:
            for card in best:
                cards.remove(card)
            pair = get_highest_pair(cards)
            best.append(pair[0])
            best.append(pair[1])
            return best
    else:
        return None

    if len(best) == 5:
        return best
    else:
        return None

def get_two_pair(cards):
    cards = list(cards)
    high_pair = get_highest_pair(cards)

    if high_pair != None:
        for c in high_pair:
            cards.remove(c)
    else:
        return None

    low_pair = get_highest_pair(cards)
    if low_pair != None:
        for c in low_pair:
            cards.remove(c)
    else:
        return None

    kickers = []
    ranks = get_by_rank(cards)
    for r in ranks:
        if len(ranks[r]) == 1:
            kickers.append(ranks[r][0])

    hand = []
    if len(kickers) != 0:
        kickers.sort()
        hand.append(high_pair[0])
        hand.append(high_pair[1])
        hand.append(low_pair[0])
        hand.append(low_pair[1])
        hand.append(kickers[-1])
        return hand
    else:
        return None


# get the pair and 3 kickers from the cards.
# Warning: Assume it is known the cards are not two pair.
def get_pair(cards):
    cards = list(cards)
    pair = get_highest_pair(cards)
     
    kickers = []
    if pair != None:
        cards.remove(pair[0])
        cards.remove(pair[1])
        ranks = get_by_rank(cards)
        for r in ranks:
            if len(ranks[r]) == 1:
                kickers.append(ranks[r][0])
        if len(kickers) >= 3:
            kickers.sort(key=None, reverse=True)
            pair.append(kickers[0])
            pair.append(kickers[1])
            pair.append(kickers[2])
            return pair
        else:
            return None

def get_high_card(cards):
    cards = list(cards)
    ranks = get_by_rank(cards)
    hand = []
    
    for r in ranks:
        if len(ranks[r]) == 1:
            hand.append(ranks[r][0])
    
    hand.sort(key=None,reverse=True)
    if len(hand) >= 5:
        hand = hand[0:5]

        return hand
    else:
        return None


# returns a dictionary with Rank as Key, and a list of all cards of that Rank as Value
def get_by_rank(cards):
    try:
        cards = list(cards)
    except:
        cards = [cards]

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


# get the highest pair from the cards
def get_highest_pair(cards):

    try:
        cards = list(cards)
    except:
        pass

    ranks = get_by_rank(cards)
    best = []

    for r in ranks:
        if len(ranks[r]) == 2:
            if len(best) == 0:
                best = ranks[r]
            else:
                if ranks[r][0] > best[0]:
                    best = ranks[r]
        
    if len(best) == 2:
        return best
    else:
        return None

def get_cards_string(cards):
    cards = list(cards)
    cards.sort()
    print_string = ''
    for c in cards:
        print_string += c.short()

    return print_string

# TESTCODE HERE:
hc_results = dict()
for runs in range(0,100):

    deck = Deck()
    deck.shuffle()

    player1 = []
    player2 = []
    board = []

    for i in range(0,2):
        player1.append(deck.deal())

    for i in range(0,2):
        player2.append(deck.deal())

    for i in range(0,5):
        board.append(deck.deal())

    hole1 = player1[0].short() + player1[1].short()
    hole2 = player2[0].short() + player2[1].short()

    p1_hole = Hole_Cards(player1)
    p2_hole = Hole_Cards(player2)

    board_short = get_cards_string(board)

    for card in board:
        player1.append(card)
        player2.append(card)

    holding1 = Holding(player1)
    holding2 = Holding(player2)

    holding1.define()
    holding2.define()

    print('')
    print('P1:{}     {}     P2:{}'.format(hole1, board_short, hole2))
    print('P1:' + p1_hole.generic()+'                                 P2:' + p2_hole.generic())
    print()

    print('')
    print('P1: ' + holding1.pretty())
    print('P2: ' + holding2.pretty())

    print('P1 < P2 (P2 WINS): ' + str(holding1 < holding2))
    print('P1 > P2 (P1 WINS): ' + str(holding1 > holding2))
    print('P1 == P2 (SPLIT) : ' + str(holding1 == holding2))
    print('P1 != P2         : ' + str(holding1 != holding2))
    print('')
    p1_short = 'P1: '
    p2_short = 'P2: '

    for card in holding1._hand:
        p1_short += card.short()

    for card in holding2._hand:
        p2_short += card.short()    

    print(p1_short)
    print(p2_short)
    print('')

    if holding1 > holding2:
        if p1_hole.generic() in hc_results:
            hc_results[p1_hole.generic()] += 1
        else:
            hc_results[p1_hole.generic()] = 0

    if holding1 < holding2:
        if p2_hole.generic() in hc_results:
            hc_results[p2_hole.generic()] += 1
        else:
            hc_results[p2_hole.generic()] = 0

# for hc in hc_results:
#     if hc_results[hc] > 0:
#         print(hc + ': ' + str(hc_results[hc]))
