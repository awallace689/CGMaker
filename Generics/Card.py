"""
=====================================================================================================
@Author: Adam Wallace
@Date: 9/30/2018
@About: Contains enums of possible card Ranks (King-high) and Suits, as well as a Card class for use
        with DeckWrapper.py
=====================================================================================================
"""
from enum import Enum


class Rank(Enum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13


class Suit(Enum):
    club = 1
    heart = 2
    diamond = 3
    spade = 4


class Card:
    def __init__(self, rank=None, suit=None):
        if rank is not None or suit is not None:
            self._rank = rank
            self._suit = suit

        else:
            self._rank = rank
            self._suit = suit

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, r):
        self._rank = r

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, s):
        self._suit = s

    def __str__(self):
        return "%s of %ss" % (self._rank.name, self._suit.name)

    def __lt__(self, other):
        return self.rank.value < other.rank.value

    def __le__(self, other):
        return self.rank.value <= other.rank.value

    def __gt__(self, other):
        return self.rank.value > other.rank.value

    def __ge__(self, other):
        return self.rank.value >= other.rank.value

    def __eq__(self, other):
        return self.rank.value == other.rank.value

    def __ne__(self, other):
        return not (self == other)
