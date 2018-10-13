from GameBundles.BlackjackBundle.BlackjackTemplateMods import BlackjackDeck
from Templates.Hand import Hand


def draw_two(d: BlackjackDeck):
    hand1 = Hand()
    hand2 = Hand()
    hand1.add(b.draw_deck())
    hand2.add(b.draw_deck())

    if hand1.cards[0] > hand2.cards[0]:
        print('Card 1: {} beats Card 2: {}'.format(str(card1), str(card2)))
    else:
        print('Card 2: {} beats Card 1: {}'.format(str(card2), str(card1)))


b = BlackjackDeck()

d = input('> How many times would you like to compare two cards from the deck? \n> ')
for i in range(int(d)):
    draw_two(b)
print('Deck Size: {}, Discard Size: {}'.format(b.deck_size, b.discard_size))
