from Generics.ABCs import GameManagerABC
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackPlayer
from GameBundles.BlackjackBundle.BlackjackGenericsMods import NegativeBankroll, NotPlayingError
from GameBundles.BlackjackBundle.BlackjackRules import BettingPhase


def is_playing(func):
    def wrapper(self, player: BlackjackPlayer, *args):
        if player.is_playing:
            return func(self, player, args)
        else:
            raise NotPlayingError

    return wrapper


def check_amount(func):
    def wrapper(self, player: BlackjackPlayer, amount, *args):
        if player.bankroll - amount >= 0:
            return func(self, player, amount, args)
        else:
            raise NegativeBankroll

    return wrapper


def make_player():
    return BlackjackPlayer(300)


class BlackjackManager(GameManagerABC):
    def __init__(self, phases=None, players=list()):
        super().__init__(phases, players)

    def add_players(self, count):
        assert(self._players.__len__() + count < 8)
        assert(count > 0)
        self._players += [make_player() for _ in range(count)]


GM = BlackjackManager(BettingPhase)
GM.add_players(3)
print(GM.players)
