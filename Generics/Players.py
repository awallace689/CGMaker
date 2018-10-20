from Generics.Hand import Hand


class Player:
    hand = Hand()

    def __init__(self, bank=100):
        assert bank >= 0
        self._bankroll = bank

    @property
    def bank(self):
        return self._bankroll

    @bank.setter
    def bank(self, bank):
        self._bankroll = bank

    def take_bank(self, amount):
        assert amount <= self.bank
        self.bank -= amount
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
