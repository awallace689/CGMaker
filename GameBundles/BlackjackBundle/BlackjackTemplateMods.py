"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains classes inheriting from or modelling template classes with blackjack-game specific
        functionality. Used by
====================================================================================================
"""
from Templates.DeckWrapper import DeckWrapper
from Templates.Card import Card, Suit
from enum import Enum
from random import shuffle as rshuffle


class BlackjackDeck(DeckWrapper):
    def __init__(self, other=None):
        super().__init__()

        if other is not None:
            assert isinstance(other, BlackjackDeck)
            self._deck = other.deck
            self._discard = other.discard_deck
        else:
            self._deck = BlackjackDeck.new_deck(shuffle=True)

    @staticmethod
    def new_deck(shuffle=True):
        deck = DeckWrapper.new_deck(shuffle)
        deck = deck * 6
        if shuffle:
            rshuffle(deck)
        return deck


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
    jack = 11
    queen = 12
    king = 13


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

    @property
    def rank(self):



