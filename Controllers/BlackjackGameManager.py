from Generics.ABCs import GameManagerABC, ExitCondition, EndTurn
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackPlayer
from GameBundles.BlackjackBundle.BlackjackRules import BlackjackRules, get_input


def make_player():
    return BlackjackPlayer(300)


def catch_exit(func):
    def wrapper(*args):
        try:
            return func(*args)

        except ExitCondition:
            if get_input(query=True, query_string="Are you sure?"):
                raise ExitCondition
    return wrapper


def catch_end_turn(func):
    def wrapper(*args):
        try:
            return func(*args)

        except EndTurn:
            pass
    return wrapper


class BlackjackManager(GameManagerABC):
    def __init__(self, phases=None, players=list()):
        super().__init__(phases, players)
        self._phases = BlackjackRules.phase_dict

    @property
    def playing(self):
        return [self._players[i] for i in range(len(self._players)) if (self._players[i].bankroll > 0)]

    def add_players(self, count):
        assert(len(self._players) + count < 8)
        assert(count > 0)
        self._players += [make_player() for _ in range(count)]

    def run_phases(self):
            self.run_on_playing(self.playing)

    @catch_exit
    def run_on_playing(self):
        for (_, phase) in self._phases:
            for player in self.playing:
                self.run_phase(phase, player)

    @catch_end_turn
    def run_phase(self, phase, player):
        phase.run_self(player)
