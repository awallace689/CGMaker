from Templates.Hand import Hand


class Player():
    hand = Hand()

    def __init__(self, bank=500):
        assert bank >= 0
        self._bankroll = bank

    @property
    def bank(self):
        return self._bankroll

    @bank.setter
    def bank(self, bank):
        self._bankroll = bank

