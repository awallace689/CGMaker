from Generics.ABCs import RulesABC, PhaseABC, abstractmethod, EndTurn
from Generics.Player import Player
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from Generics.Menu import Menu


class BlackjackPhase(PhaseABC):
    """Superclass for all Blackjack phases. Contains abstract methods required for

    :attributes:
        methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
        options: return list of tuples containing unselected player options (to prevent repeat selections)

    :abstractmethods:
        run_npc(player)
            runs NPC implementation of phase on 'player'
        run_user(player)
            runs User implementation of phase on 'player'

    :methods:
        end_turn()
            resets self.methods and raises EndTurn exception, use as "EndTurn" option in (subclass).methods
    """
    def __init__(self):
        super().__init__()
        self._methods = list()

    @abstractmethod
    def run_npc(self, player):
        pass

    @abstractmethod
    def run_user(self, player):
        pass

    @property
    def methods(self):
        """Return list of tuples containing Phase methods and information about them

        :return: [("name", Function obj, "tooltip", is_valid_option)]
        :rtype:  [(String, Function object, String, Bool)]
        """
        return self._methods

    @property
    def options(self):
        return list(filter((lambda tup: tup[3] is True), self._methods))

    def end_turn(self):
        for tup in self._methods:
            self._methods[3] = True

        raise EndTurn


class BettingPhase(BlackjackPhase):
    """
    attri
    """
    Menu = None

    def __init__(self, _menu: Menu):
        super().__init__()
        self._methods = [("Bet", self.get_bet, "Place your bet.", True),
                         ("End Turn", self.end_turn, "End your turn.", True),
                         ("Exit", self.exit, "Return to main menu."), True]
        self.Menu = _menu

    def run_npc(self, player):
        pass

    def run_user(self, player): # TODO: next
        pass

    @staticmethod
    def take_bank(player, amount):
        player.bankroll -= amount
        return amount


class BlackjackRules(RulesABC):
    phase_list = [("Betting Phase", BettingPhase)]

    def __init__(self):
        super().__init__()
