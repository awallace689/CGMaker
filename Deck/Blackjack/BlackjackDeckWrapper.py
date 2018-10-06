"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: A subclass of DeckWrapper meant for use with Blackjack rules set.
====================================================================================================
"""
from Deck.DeckWrapper import DeckWrapper


class BlackjackDeck(DeckWrapper):
    def __init__(self, other=None):
        super().__init__()

        if other is not None:
            assert isinstance(other, BlackjackDeck)
            self._deck = other.deck
            self._discard = other.discard_deck
        else:
            self._deck = self.new_deck(shuffle=True)

    @staticmethod
    def new_deck(shuffle=True):
        deck = []
        for i in range(6):
            deck = deck + DeckWrapper.new_deck(shuffle=shuffle)
        return deck
