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
from Generics.Player import NPC, User, Hand
from enum import Enum
from random import shuffle as rshuffle


class BlackjackDeck(DeckWrapper):
    """Decks consist of BlackjackCard objects, which use BlackjackRanks when comparing two cards."""
    def __init__(self, other=None):
        super().__init__()

        if other is not None:
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
    def true_rank(self):
        """Returns value of self._rank (from Rank class)

        :return: Rank enum attribute
        """
        return self._rank

    @property
    def rank(self):
        """Takes advantage of identical naming scheme to return self._rank's corresponding BlackjackRank enum

        :return: BlackjackRank enum attribute
        """
        return BlackjackRank[self._rank.name]


class BlackjackHand(Hand):
    def __init__(self):
        super().__init__()

    def get_hand_str(self):
        string = ""
        for i in range(len(self._cards)):
            if i != len(self._cards) - 1:
                string += f"{str(self._cards[i])}, "

            else:
                string += f"{str(self._cards[i])}"
        return string

    def get_totals(self):
        totals = []
        aces = 0

        for card in self._cards:
            if card.true_rank == Rank.ace:
                aces += 1
        totals.append(sum([card.rank.value for card in self._cards]))

        for i in range(aces):
            totals.append(sum([card.rank.value for card in self._cards]) + 10 + (10 * i))

        return totals


class BlackjackNPC(NPC):
    bankroll = None
    hand = BlackjackHand()

    def __init__(self, start_bank=300):
        super().__init__()
        self.bankroll = start_bank
        self._playing = True

    def take_bank(self, amount):
        if self.bankroll >= amount:
            self.bankroll -= amount
            return amount

        else:
            raise NegativeBankroll

    @property
    def is_playing(self):
        if self._playing is False:
            return False

        elif self.bankroll <= 0:
            return False

        else:
            return True

    @is_playing.setter
    def is_playing(self, b: bool):
        self._playing = b


class BlackjackUser(User):
    bankroll = None

    def __init__(self, start_bank=300):
        super().__init__()
        self.bankroll = start_bank
        self._playing = True
        self.hand = BlackjackHand()

    def take_bank(self, amount):
        if self.bankroll >= amount:
            self.bankroll -= amount
            return amount

        else:
            raise NegativeBankroll

    @property
    def is_playing(self):
        if self._playing is False:
            return False

        elif self.bankroll <= 0:
            return False

        else:
            return True

    @is_playing.setter
    def is_playing(self, b: bool):
        self._playing = b


class NegativeBankroll(Exception):
    def __init__(self):
        pass
