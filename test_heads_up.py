import tkpoker as pkr

win_counter = dict()
for runs in range(0,1000000):

    deck = pkr.Deck()
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

    p1_hole = pkr.Hole_Cards(player1)
    p2_hole = pkr.Hole_Cards(player2)

    board_short = pkr.get_cards_string(board)

    for card in board:
        player1.append(card)
        player2.append(card)

    holding1 = pkr.Holding(player1)
    holding2 = pkr.Holding(player2)

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

    win = None
    if holding1 > holding2:
        win = p1_hole.generic()
    if holding2 > holding1:
        win = p2_hole.generic()

    if win not in win_counter.keys():
        win_counter[win] = 0

    win_counter[win] += 1

sorted_wins = dict(sorted(win_counter.items(), key=lambda item: item[1], reverse=True))

for combo, count in sorted_wins.items():
    print(f"{combo} - {count}")

    
    
