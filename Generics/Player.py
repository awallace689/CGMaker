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
