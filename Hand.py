"""
#====================================================================================================
@Author: Adam Wallace
@Date: 10/3/2018
@About: A Hand class for use with "Card.py," made to be usable with any '52-card deck' game implementation.
#====================================================================================================
"""
from Deck.Card import Card


class Hand:
    def __init__(self, *args):
        try:
            arg: Hand = args[0]
            self._cards = arg.cards
        except IndexError:
            self._cards = list()

    def __str__(self):
        string = ""
        for card in self.cards:
            string = ", " + string + str(card)

        string = string[2:]
        return ("Length: %d\n" % self._cards.__len__()) + string

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, c: list):
        self._cards = c

    @property
    def size(self):
        return self._cards.__len__()

    @property
    def is_empty(self):
        return self._cards.__len__() == 0

    def add(self, card, index=None):
        assert isinstance(card, Card)
        if index is not None:
            self.cards.insert(index, card)
        else:
            self.cards.append(card)

    def discard(self, index):
        assert (index < self.size)
        assert (index >= 0)
        discarded = self.cards[index]
        self._cards.remove(index)
        return discarded

    def swap(self, i, j):
        temp = self.cards[i]
        self.cards[i] = self.cards[j]
        self.cards[j] = temp
