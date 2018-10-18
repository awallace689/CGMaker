from GameBundles.BlackjackBundle.BlackjackTemplateMods import BlackjackDeck
from Templates.Hand import Hand


def draw_two(d: BlackjackDeck):
    hand1 = Hand()
    hand2 = Hand()
    hand1.add(d.draw_deck())
    hand2.add(d.draw_deck())

    if hand1.peek() > hand2.peek():
        print('Card 1: {} beats Card 2: {}'.format(hand1.peek(), hand2.peek()))
        d.add_discard(hand1.take(), hand2.take())
    elif hand1.peek() == hand2.peek():
        print('Card 1: {} ties Card 2: {}'.format(hand1.peek(), hand2.peek()))
        d.add_discard(hand1.take(), hand2.take())
    else:
        print('Card 2: {} beats Card 1: {}'.format(hand2.peek(), hand1.peek()))
        d.add_discard(hand1.take(), hand2.take())


b = BlackjackDeck()

inp = input('> How many times would you like to compare two cards from the deck? \n> ')
for i in range(int(inp)):
    draw_two(b)
print('Deck Size: {}, Discard Size: {}'.format(b.deck_size, b.discard_size))
