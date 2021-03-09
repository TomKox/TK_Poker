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

        cards = list(self._cards)

        hand = get_royal_flush(cards)
        if hand != None:
            self._ranking = Ranking.ROYAL_FLUSH

        else:
            hand = get_straight_flush(cards)
            if hand != None:
                self._ranking = Ranking.STRAIGHT_FLUSH

            else:
                hand = get_four_of_a_kind(cards)
                if hand != None:
                    self._ranking = Ranking.FOUR_OF_A_KIND

                else:
                    hand = get_full_house(cards)
                    if hand != None:
                        self._ranking = Ranking.FULL_HOUSE

                    else:
                        hand = get_flush(cards)
                        if hand != None:
                            self._ranking = Ranking.FLUSH
                        
                        else:
                            hand = get_straightcards(cards)
                            if hand != None:
                                self._ranking = Ranking.STRAIGHT
                            
                            else:
                                hand = get_three_of_a_kind(cards)
                                if hand != None:
                                    self._ranking = Ranking.THREE_OF_A_KIND

                                else:
                                    hand = get_two_pair(cards)
                                    if hand != None:
                                        self._ranking = Ranking.TWO_PAIR

                                    else:
                                        hand = get_pair(cards)
                                        if hand != None:
                                            self._ranking = Ranking.PAIR

                                        else:
                                            hand = get_high_card(cards)
                                            self._ranking = Ranking.HIGH_CARD
            
        self._hand = hand    


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
    
    if len(hand) >= 5:
        hand = hand[0:5]
        hand.sort(key=None,reverse=True)
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

def print_cards_sorted(cards):
    cards = list(cards)
    cards.sort()
    print_string = 'SORTED: '
    for c in cards:
        print_string += c.short()

    print(print_string)

# TESTCODE HERE:
i = 0
continue_loop = True

results = dict()

for rnk in Ranking:
    results[str(rnk)] = []

while continue_loop:
    # print('------------------------------------------')
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
    # card2 = Card(Rank.KING, Suit.SPADES)
    # card3 = Card(Rank.QUEEN, Suit.SPADES)
    # card4 = Card(Rank.JACK, Suit.SPADES)
    # card5 = Card(Rank.TEN, Suit.SPADES)
    # card6 = Card(Rank.NINE, Suit.SPADES)
    # card7 = Card(Rank.EIGHT, Suit.SPADES)
   
    seven_cards = [card1, card2, card3, card4, card5, card6, card7]
    cards_string = ''
    for card in seven_cards:
        cards_string = cards_string + card.short()
    
    # print(cards_string)

    holding = Holding(seven_cards)
    try:
        holding.define()
    except:
        print('Define failed for cards:')
        print(cards_string)

    hr = str(holding._ranking)

    results[hr].append(seven_cards)
    # hand_spec = str(holding._ranking) + ": "
    # for card in holding._hand:
    #     hand_spec += card.short()
    # print(hand_spec)

    # continue_loop = False

    i = i + 1
    if i == 100000:
         continue_loop = False
 
print('RESULTS:')
for r in results:
    ranking_name = str(r)
    ranking_count = str(len(results[r]))
    print(ranking_name + ': ' + ranking_count)

print('--------------------------------------')
for r in results:
    print(str(r).capitalize())
    
    if len(results[r]) < 10:
        max = len(results[r])
    else:
        max = 10

    for i in range(0, max):
        print_cards_sorted(results[r][i])

    print('--------------------------------------')
