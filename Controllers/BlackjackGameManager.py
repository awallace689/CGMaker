from Generics.ABCs import GameManagerABC, ExitCondition, EndTurn
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from GameBundles.BlackjackBundle.BlackjackRules import BlackjackRules, get_input


def make_user(bankroll=300):
    return BlackjackUser(bankroll)


def make_npc(bankroll=300):
    return BlackjackNPC(bankroll)


def catch_exit(func):
    """Catches ExitCondition exception and displays exit-check frame

    :param func: function capable of throwing exception Generics.ABCs.ExitCondition
    :return: None
    :raise: Generics.ABCs.ExitCondition, if user confirms desire to exit
    """
    def wrapper(*args):
        try:
            return func(*args)

        except ExitCondition:
            if get_input(query=True, query_string="Are you sure you want to exit?"):
                raise ExitCondition
    return wrapper


def catch_end_turn(func):
    """Catches EndTurn exception and displays end-check frame

    :param func: function capable of throwing exception Generics.ABCs.EndTurn
    :return: None
    :raise: Generics.ABCs.EndTurn, if user confirms desire to exit
    """
    def wrapper(*args):
        try:
            return func(*args)

        except EndTurn:
            if get_input(query=True, query_string="Are you sure you want to end your turn?"):
                raise EndTurn
    return wrapper


class BlackjackManager(GameManagerABC):
    """Handles high-level game operations, running phases on list of valid players, adding/removing of players

    (*)<- Inherited
    :attributes:
        playing: return list of BlackjackNPC and/or BlackjackPlayer in '_players' with bankroll > 0

    :methods:
        add_players(self, count: int, player_type=None, bankroll=300)
            Add 'count' BlackjackPlayer or BlackjackNPC objects to '_players' with default bankroll 300.
        remove_player(self, i: int)
            Removes player from '_players' at index 'i'

    :private:
        :variables:
            *_players: list of BlackjackUser and/or BlackjackNPC objects
            *_phases : list of game phases to run on each (playing) player, from BlackjackRules.phase_list

    """
    def __init__(self, players=list()):
        super().__init__()
        self._phases = BlackjackRules.phase_list
        self._players = players

    @property
    def playing(self):
        """Get list of players who "pass" the inner function 'check'

        :return: List of BlackjackPlayer and/or BlackjackNPC objects
        """
        def check(player):
            if player.bankroll > 0:
                return True
            else:
                return False

        return [self._players[i] for i in range(len(self._players)) if check(self._players[i])]

    def add_players(self, count, player_type, bankroll=300):
        """Add 'count' BlackjackPlayer or BlackjackNPC objects to '_players' with default bankroll 300

        :param count: Int, number of players of one type to add
        :param player_type: None, no character created

        :kwargs:
            bankroll=default: sets bankroll of created players to 300
                    =int    : sets bankroll of created players to 'int'

        :return: None
        """
        assert(len(self._players) + count < 8)
        assert(count > 0)

        if player_type.lower() == "npc":
            self._players += [make_npc(bankroll=bankroll) for _ in range(count)]

        elif player_type.lower() == "user":
            self._players += [make_user(bankroll=bankroll) for _ in range(count)]

        else:
            raise ValueError

    def remove_player(self, i):
        """Removes player from '_players' at index 'i'

        :param i:
        :return:
        """
        assert self._players[i]
        self._players.pop(index=i)

    @catch_exit
    def run_on_playing(self):
        """Calls 'run_phase' for each phase in order on each player, in order.

        :return: None
        """
        for (_, phase) in self._phases:
            if len(self.playing) is 0:
                raise ExitCondition
            for player in self.playing:
                self.run_phase(phase, player)

    @catch_end_turn
    def run_phase(self, phase, player):
        """Runs appropriate phase_run method based on player type.

        :param phase: Phase object, to run with 'player'
        :param player: Player object, player to run phase on
        :return: None
        """
        phase.run_self(player)
