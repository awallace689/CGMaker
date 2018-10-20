"""
#====================================================================================================
@Author: Adam Wallace
@Date: 10/3/2018
@About: A Hand class for use with "Card.py," made to be usable with any '52-card deck' game implementation.
#====================================================================================================
"""
from Templates.Card import Card


class Hand:
    def __init__(self, other=None):
        if other is not None:
            assert isinstance(other, Hand)
            self._cards = other.cards
        else:
            self._cards = []

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

    def take(self, index=0):
        assert (index < self.size)
        assert (index >= 0)
        selected = self._cards[index]
        self._cards.remove(self._cards[index])
        return selected

    def swap(self, i, j):
        assert (i < self.size, i >= 0, j < self.size, j >= 0)

        temp = self.cards[i]
        self.cards[i] = self.cards[j]
        self.cards[j] = temp

    def peek(self, index=0):
        return self.cards[index]



