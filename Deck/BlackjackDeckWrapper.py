"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: A subclass of DeckWrapper meant for use with Blackjack game.
====================================================================================================
"""
from Deck.DeckWrapper import DeckWrapper


class BlackjackDeck(DeckWrapper):
    def __init__(self, *args):
        super().__init__()

        if args:
            assert isinstance(args[0], BlackjackDeck)
            arg = args[0]
            self._deck = arg.deck
            self._discard = arg.discard_deck
        else:
            self._deck = self.new_deck(shuffle=True)

    @classmethod
    def new_deck(cls, shuffle=True):
        deck = list()
        for i in range(6):
            deck.append(DeckWrapper.new_deck(DeckWrapper, shuffle=shuffle))
        return deck


bj_deck = BlackjackDeck()
print_deck = bj_deck.deck
print(bj_deck.format(print_deck))
