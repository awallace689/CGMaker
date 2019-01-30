"""
====================================================================================================
@Author: Adam Wallace
@Date: 1/30/2019
@About: Player class wraps a Hand class from Generics.Hand. User and NPC classes derive from Player,
        for use when distinction between each is needed.
====================================================================================================
"""

from Generics.Hand import Hand


class Player:
    hand = Hand()

    def __init__(self):
        pass


class User(Player):
    def __init__(self):
        super().__init__()


class NPC(Player):
    def __init__(self):
        super().__init__()
