from Generics.Hand import Hand


class Player:
    hand = Hand()

    def __init__(self, bank=100):
        assert bank >= 0
        self._bankroll = bank

    @property
    def bankroll(self):
        return self._bankroll

    @bankroll.setter
    def bankroll(self, bank):
        self._bankroll = bank

    def take_bank(self, amount):
        assert amount <= self._bankroll
        self._bankroll -= amount
        return amount


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self._bankroll = 1000000000

    @property
    def net_change(self):
        return self._bankroll - 1000000000

    def bankroll_reset(self):
        self._bankroll = 1000000000
