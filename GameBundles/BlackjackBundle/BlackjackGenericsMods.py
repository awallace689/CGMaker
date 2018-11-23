"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains classes inheriting from or modelling template classes with blackjack-game specific
        functionality. Used by
====================================================================================================
"""
from Generics.DeckWrapper import DeckWrapper
from Generics.Card import Card, Suit, Rank
from Generics.Player import Player, NPC, User
from enum import Enum
from random import shuffle as rshuffle


class BlackjackDeck(DeckWrapper):
    """Decks consist of BlackjackCard objects, which use BlackjackRanks when comparing two cards."""
    def __init__(self, other=None):
        super().__init__()

        if other is not None:
            assert isinstance(other, BlackjackDeck)
            self._deck = other.deck
            self._played = other.played

        else:
            self._deck = BlackjackDeck.new_deck(shuffle=True)

    @staticmethod
    def new_deck(shuffle=True):
        deck = []
        for s in Suit:
            for r in Rank:
                deck += [BlackjackCard(r, s)]
        deck = deck * 6

        if shuffle:
            rshuffle(deck)

        return deck


class BlackjackRank(Enum):
    """Referred to by BlackjackCard.rank property."""
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
    """self._rank is object type Rank, self.rank returns object type BlackjackRank"""
    def __init__(self, rank=None, suit=None):
        super().__init__()
        self._rank = rank
        self._suit = suit

    @property
    def rank(self):
        return BlackjackRank[self._rank.name]


class BlackjackUser(User):
    bankroll = None
    playing = None

    def __init__(self, start_bank=300):
        super().__init__()
        self.bankroll = start_bank
        self.playing = True


class BlackjackNPC(NPC):
    bankroll = None
    playing = None

    def __init__(self, start_bank=300):
        super().__init__()
        self._bankroll = start_bank
        self._playing = True

    @property
    def bankroll(self):
        return self._bankroll

    @bankroll.setter
    def bankroll(self, bank):
        self._bankroll = bank

    @property
    def is_playing(self):
        if self._playing is False:
            return False
        elif self._bankroll <= 0:
            return False
        else:
            return True

    @is_playing.setter
    def is_playing(self, b: bool):
        self._playing = b


class NotPlayingError(Exception):
    def __init__(self):
        pass


class NegativeBankroll(Exception):
    def __init__(self):
        pass