from Deck.DeckWrapper import DeckWrapper as DWrap
from Deck.Card import Card
from Deck.Card import Rank
from Deck.Card import Suit

class Hand:
    def __init__(self, *args):
        try:
            arg = args[0]
            self._cards = arg.cards
        except IndexError:
            self._cards = list()

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, c):
        self._cards = c

    @property
    def size(self):
        return self._cards.__len__()

    @property
    def is_empty(self):
        return self._cards.__len__() == 0

    def add(self, card):
        assert isinstance(card, Card)


h = Hand()
card = Card(Rank.ace, Suit.spade)

