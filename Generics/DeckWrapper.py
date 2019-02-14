"""
====================================================================================================
@Author: Adam Wallace
@Date: 9/30/2018
@About: A Generics class for use with "Card.py," made to be usable with any '52-card deck' game implementation.
        Wraps a deck, its played pile ('played_deck'), and several basic functions to be performed on one/both.
@Note: Modular design and minimal method complexity allows class to serve as superclass for a variety
       of game decks.
====================================================================================================
"""
from Generics.Card import *
from random import shuffle as rshuffle


class DeckWrapper:
    """

    """

    def __init__(self, other=None):
        """If no DeckWrapper 'other' provided, deck will be automatically generated and shuffled."""
        if other is not None:
            assert isinstance(other, DeckWrapper)
            self._deck = other.deck
            self._played = other.played

        else:
            self._deck = DeckWrapper.new_deck()
            self._played = []

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, d):
        self._deck = d.deck

    @property
    def played(self):
        return self._played

    @played.setter
    def played(self, d):
        self._played = d.played

    @property
    def deck_size(self):
        return len(self._deck)

    @property
    def played_size(self):
        return len(self._played)

    @property
    def is_deck_empty(self):
        return len(self._deck) == 0

    @property
    def is_played_empty(self):
        return len(self._played) == 0

    @staticmethod
    def new_deck(shuffle=True):
        """Creates new deck of length 52, no Jokers, and shuffles it using random.shuffle()"""
        deck = []
        for s in Suit:
            for r in Rank:
                arr_new_card = [Card(r, s)]
                deck = deck + arr_new_card

        if shuffle:
            rshuffle(deck)  # random.shuffle
        return deck

    @staticmethod
    def peek(deck: list):
        return deck[0]

    @staticmethod
    def format(deck: list):
        """Creates and returns list of 2-tuples, formatted (Rank, Suit), one tuple per card"""
        p_deck = []
        for card in deck:
            p_deck.append((card.rank.name, card.suit.name))
        return ("Length: %d \n" % len(deck)) + str(p_deck)

# ===================================================================================================
#                                      **DECK-ALTERING METHODS**
# ===================================================================================================

    def draw_deck(self):
        drawn = self._deck[0]
        self._deck = self._deck[1:]
        return drawn

    def draw_played(self):
        drawn = self._played[0]
        self._played = self._played[1:]
        return drawn

    def add_deck(self, card: Card, index):
        self.deck.insert(index, card)

    def add_played(self, *args):
        for card in args:
            assert isinstance(card, Card)
            self.played.append(card)

    def reset(self, shuffle=True):
        if shuffle:
            self._deck = DeckWrapper.new_deck()
        else:
            self._deck = DeckWrapper.new_deck(shuffle=False)
        self._played = []
