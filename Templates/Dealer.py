from Templates.Player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self._bankroll = 1000000000
