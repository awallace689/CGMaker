from Generics.Player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self._bankroll = 1000000000

    @property
    def net_change(self):
        return self._bankroll - 1000000000

    def bankroll_reset(self):
        self._bankroll = 1000000000
