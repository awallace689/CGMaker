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
        """Returns new list of BlackjackCards

        :param shuffle: Bool, calls random.shuffle() on list of cards if True
        :return: List of 312 (52 * 6) BlackjackCards
        """
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
    """Extension of Card class for Blackjack Game
    :properties:
        true_rank
            Returns corresponding Rank enum attribute
        rank
            Returns corresponding BlackjackRank enum attribute
    """
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
    """Extension of Hand class for Blackjack Game

    :methods:
        get_hand_str()
            Returns BlackjackCard.__str__() for each card in self._cards, in-order
    """
    def __init__(self):
        super().__init__()

    def get_hand_str(self):
        """Returns BlackjackCard.__str__() for each card in self._cards, in-order

        :return: string, comma separated list of each BlackjackCard.__str__()
        """
        string = ""
        for i in range(len(self._cards)):
            if i != len(self._cards) - 1:
                string += f"{str(self._cards[i])}, "

            else:
                string += f"{str(self._cards[i])}"
        return string

    def get_totals(self):
        """Returns list of possible hand score totals for BlackjackGame

        :return: list, contains int values for each possible hand score total
        """
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
    """Extension of NPC class for BlackjackGame
    :attributes:
        bankroll
            int, represents money held by player
        hand
            BlackjackHand, hand of cards held by player

    :properties:
        is_playing
            Returns True if player has valid game state, else False

    :methods:
        take_bank(amount)
            Returns int of given amount after subtracting it from BlackjackNPC.bankroll
    """
    bankroll = None
    hand = BlackjackHand()

    def __init__(self, start_bank=300):
        super().__init__()
        self.bankroll = start_bank
        self._playing = True

    def take_bank(self, amount):
        """Returns int of given amount after subtracting it from self.bankroll

        :param amount: int, amount to take from self.bankroll
        :return: int
        :raises: NegativeBankroll, if (self.bankroll - amount) < 0
        """
        if self.bankroll >= amount:
            self.bankroll -= amount
            return amount

        else:
            raise NegativeBankroll

    @property
    def is_playing(self):
        """Returns value of self._playing if False, else checks if self.bankroll is <= 0

        :return: Bool
        """
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
    """Extension of the User class for BlackjackGame

    :attributes:
        bankroll
            int, represents money held by player

    :properties:
        is_playing
            Returns True if player has valid game state, else False

    :methods:
        take_bank(amount)
                Returns int of given amount after subtracting it from BlackjackNPC.bankroll


    """
    bankroll = None

    def __init__(self, start_bank=300):
        super().__init__()
        self.bankroll = start_bank
        self._playing = True
        self.hand = BlackjackHand()

    def take_bank(self, amount):
        """Returns int of given amount after subtracting it from self.bankroll

        :param amount: int, amount to take from self.bankroll
        :return: int
        :raises: NegativeBankroll, if (self.bankroll - amount) < 0
        """
        if self.bankroll >= amount:
            self.bankroll -= amount
            return amount

        else:
            raise NegativeBankroll

    @property
    def is_playing(self):
        """Returns value of self._playing if False, else checks if self.bankroll is <= 0

        :return: Bool
        """
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
