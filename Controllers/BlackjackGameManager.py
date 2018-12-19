from Generics.ABCs import GameManagerABC, EndTurn, ExitCondition
from Generics.Menu import Menu, check_int
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from GameBundles.BlackjackBundle.BlackjackRules import BlackjackRules
from random import shuffle


def make_user(bankroll=300):
    return BlackjackUser(bankroll)


def make_npc(bankroll=300):
    return BlackjackNPC(bankroll)


def catch_end(func):
    """Catches ExitCondition exception and safely ignores it to begin next loop iteration

    :param func: function capable of throwing exception Generics.ABCs.ExitCondition
    :return: Return-type of 'func'
    """
    def wrapper(*args):
        try:
            return func(*args)

        except EndTurn:
            pass
    return wrapper


class BlackjackManager(GameManagerABC):
    """Handles high-level game operations, running phases on list of valid players, adding/removing of players

    (*)<- Inherited
    :attributes:
        *menu  : return Generics.Menu.Menu object, created in main.py, used throughout program
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
    def __init__(self, _menu=Menu()):
        super().__init__()
        self.menu = _menu
        self._phases = [Phase(_menu=self.menu) for Phase in BlackjackRules.phase_list]
        self._players = []

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
                            "npc", BlackjackNPC
                            "user", BlackjackUser

        :kwargs:
            :param bankroll: =default: sets bankroll of created players to 300
                             =int    : sets bankroll of created players to 'int'

        :return: None
        """
        assert(len(self._players) + count - 1 < 8)
        assert(count >= 0)

        if player_type.lower() == "npc":
            self._players += [make_npc(bankroll=bankroll) for _ in range(count)]

        elif player_type.lower() == "user":
            self._players += [make_user(bankroll=bankroll) for _ in range(count)]

        else:
            raise ValueError

    def remove_player(self, i):
        """Removes player from '_players' at index 'i'

        :param i: int, index
        :return: None
        """
        assert self._players[i]
        self._players.pop(index=i)

    @catch_end
    def run_on_playing(self):
        """Calls the appropriate BlackjackRules.BlackjackPhase.run_X method on each player in self.playing

        :return: None
        """
        for phase in self._phases:
            if len(self.playing) is 0:
                raise ExitCondition

            for player in self.playing:
                if isinstance(player, BlackjackUser):
                    phase.run_user(player)

                elif isinstance(player, BlackjackNPC):
                    phase.run_npc(player)

                else:
                    raise ValueError

    def run(self):
        """Inherited method called in order to run Blackjack game.

        :return: None
        """
        self._players = [BlackjackUser()]

        self.menu.add_frame(frame_type="custom",
                            header="SETUP",
                            prompt="How many other NPC's? (Max: 8)",
                            content="Enter number:")
        number_npc = self.menu.display(get_input=True,
                                       check=lambda inp: True if check_int(inp) and int(inp) < 8 else False)

        self.add_players(int(number_npc), player_type="npc")
        shuffle(self._players)

        self.run_on_playing()
