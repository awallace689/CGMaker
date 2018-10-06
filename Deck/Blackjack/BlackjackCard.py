"""
=====================================================================================================
@Author: Adam Wallace
@Date: 9/30/2018
@About: Contains enums for possible card Ranks (King-high) and Suits, as well as Card class for use with DeckWrapper.py
=====================================================================================================
"""
from Deck.Card import Card, Suit
from enum import Enum


class BlackjackRank(Enum):
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
    jack = 10
    queen = 10
    king = 10


class BlackjackCard(Card):
    def __init__(self, rank=None, suit=None):
        super().__init__()

        if rank is None and suit is None:
            self._rank = rank
            self._suit = suit
        else:
            assert isinstance(rank, BlackjackRank)
            assert isinstance(suit, Suit)
            self._rank = rank
            self._suit = suit
