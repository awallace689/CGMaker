from Generics.ABCs import GameManagerABC, ExitCondition
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackPlayer
from GameBundles.BlackjackBundle.BlackjackRules import BettingPhase


def make_player():
    return BlackjackPlayer(300)


def catch_exit(func):
    def wrapper(self, *args):
        try:
            f = func(self, args)
            return f

        except ExitCondition:
            self.exit_to_menu()
    return wrapper


class BlackjackManager(GameManagerABC):
    def __init__(self, phases=None, players=list()):
        super().__init__(phases, players)

    @property
    def playing(self):
        return [self.players[i] for i in range(len(self.players)) if (self.players[i].bankroll > 0)]

    def add_players(self, count):
        assert(self._players.__len__() + count < 8)
        assert(count > 0)
        self._players += [make_player() for _ in range(count)]

    def run_phases(self):
            self.run_on_playing(self.playing)

    @catch_exit
    def run_on_playing(self, playing: list):
        for phase in self.phases:
            for player in playing:
                phase.run(player)


GM = BlackjackManager(BettingPhase)
GM.add_players(3)
GM.playing[1].bankroll = 0
