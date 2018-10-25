from Generics.Hand import Hand
from GameBundles.BlackjackBundle.BlackjackRules import *
from Generics.Menu import Menu


# def draw_two(d: BlackjackDeck):
#     hand1 = Hand()
#     hand2 = Hand()
#     hand1.add(d.draw_deck())
#     hand2.add(d.draw_deck())
#
#     if hand1.peek() > hand2.peek():
#         print('Card 1: {} beats Card 2: {}'.format(hand1.peek(), hand2.peek()))
#         d.add_discard(hand1.take(), hand2.take())
#     elif hand1.peek() == hand2.peek():
#         print('Card 1: {} ties Card 2: {}'.format(hand1.peek(), hand2.peek()))
#         d.add_discard(hand1.take(), hand2.take())
#     else:
#         print('Card 2: {} beats Card 1: {}'.format(hand2.peek(), hand1.peek()))
#         d.add_discard(hand1.take(), hand2.take())


m = Menu()
b = BettingPhase()
m.clear()
inp = get_input(b.methods, m)
