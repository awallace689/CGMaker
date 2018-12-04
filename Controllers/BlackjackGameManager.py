from Generics.ABCs import GameManagerABC, ExitCondition, EndTurn
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from GameBundles.BlackjackBundle.BlackjackRules import BlackjackRules, get_input


def make_user(bankroll=300):
    return BlackjackUser(bankroll)


def make_npc(bankroll=300):
    return BlackjackNPC(bankroll)


def catch_exit(func):
    def wrapper(*args):
        try:
            return func(*args)

        except ExitCondition:
            if get_input(query=True, query_string="Are you sure you want to exit?"):
                raise ExitCondition
    return wrapper


def catch_end_turn(func):
    def wrapper(*args):
        try:
            return func(*args)

        except EndTurn:
            if get_input(query=True, query_string="Are you sure you want to end your turn?"):
                raise EndTurn
    return wrapper


class BlackjackManager(GameManagerABC):
    def __init__(self, phases=None, players=list()):
        super().__init__(phases, players)
        self._phases = BlackjackRules.phase_list

    @property
    def playing(self):
        return [self._players[i] for i in range(len(self._players)) if (self._players[i].bankroll > 0)]

    def add_players(self, count, player_type=None, bankroll=300):
        assert(len(self._players) + count < 8)
        assert(count > 0)

        if player_type.lower() == "npc":
            self._players += [make_npc(bankroll=bankroll) for _ in range(count)]

        elif player_type.lower() == "user":
            self._players += [make_user(bankroll=bankroll) for _ in range(count)]

        elif player_type is not None:
            raise ValueError

    def remove_player(self, index):
        assert self._players[index]
        self._players.pop(index=index)

    @catch_exit
    def run_on_playing(self):
        for (_, phase) in self._phases:
            if len(self.playing) is 0:
                raise ExitCondition
            for player in self.playing:
                self.run_phase(phase, player)

    @catch_end_turn
    def run_phase(self, phase, player):
        phase.run_self(player)
