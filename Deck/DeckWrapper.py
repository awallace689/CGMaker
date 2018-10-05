"""
====================================================================================================
@Author: Adam Wallace
@Date: 9/30/2018
@About: A Deck class for use with "Card.py," made to be usable with any '52-card deck' game implementation.
        Wraps a deck, its discard pile, and several basic functions to be performed on one/both.
@Note: Modular design and minimal method complexity allows class to serve many games and rule sets.
====================================================================================================
"""
from Deck.Card import *
from random import shuffle as random_shuffle


class DeckWrapper:

    def __init__(self, *args):  # TODO: fix optional parameter implementation
        """If no parameter provided, deck will be automatically generated and shuffled."""

        if args:
            assert isinstance(args[0], DeckWrapper)
            arg = args[0]
            self._deck = arg.deck
            self._discard = arg.discard_deck
        else:
            self._deck = DeckWrapper.new_deck()
            self._discard = list()

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, d):
        assert isinstance(d, DeckWrapper)
        self._deck = d.deck

    @property
    def discard_deck(self):
        return self._discard

    @discard_deck.setter
    def discard_deck(self, d):
        assert isinstance(d, DeckWrapper)
        self._discard = d.discard_deck

    @property
    def deck_size(self):
        return self.deck.__len__()

    @property
    def discard_size(self):
        return self.discard_deck.__len__()

    @property
    def is_deck_empty(self):
        return self._deck.__len__() == 0

    @property
    def is_discard_empty(self):
        return self._discard.__len__() == 0

    @staticmethod
    def new_deck(shuffle=True):
        """Creates new deck of length 52, no Jokers, and shuffles it using random.shuffle()"""
        deck = list()
        for s in Suit:
            for r in Rank:
                new_card = Card(r, s)
                deck.append(new_card)
        if shuffle:
            random_shuffle(deck)
        return deck

    @staticmethod
    def peek(deck: list):
        return deck[0]

    @staticmethod
    def print_deck(m_deck: list):
        """Creates and returns list of 2-tuples, formatted (Rank, Suit), one tuple per card"""
        assert isinstance(m_deck, list)
        p_deck = []
        for card in m_deck:
            p_deck.append(tuple((card.rank.name, card.suit.name)))
        return ("Length: %d \n" % m_deck.__len__()) + str(p_deck)

# ===================================================================================================
#                                      **DECK-EDITING METHODS**
# ===================================================================================================

    def draw_deck(self):
        drawn = self._deck[0]
        self._deck = self._deck[1:]
        return drawn

    def draw_discard(self):
        drawn = self._discard[0]
        self._discard = self._discard[1:]
        return drawn

    def discard(self, card):
        self.discard_deck.append(card)

    def reset(self, shuffle=True):
        if shuffle:
            self._deck = DeckWrapper.new_deck()
        else:
            self._deck = DeckWrapper.new_deck(shuffle=False)
        self._discard = list()
