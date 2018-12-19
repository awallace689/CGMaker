from Generics.ABCs import RulesABC, PhaseABC, abstractmethod, EndTurn, ExitCondition
from Generics.Player import Player
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from Generics.Menu import Menu


def check_int(_input: str):
    try:
        int(_input)
        return True

    except (ValueError, TypeError):
        return False


class BlackjackPhase(PhaseABC):
    """Superclass for all Blackjack phases. Contains abstract methods required for

    :attributes:
        methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
        options: return list of tuples containing unselected player options (to prevent repeat selections)
        menu   : Menu object shared by program

    :methods:
        run_user(player)
            runs User implementation of phase on 'player'

    :abstractmethods:
        run_npc(player)
            runs NPC implementation of phase on 'player'

    :methods:
        end_turn()
            resets self.methods and raises EndTurn exception, use as "EndTurn" option in (subclass).methods
    """
    menu = None
    name = None

    def __init__(self, _menu: Menu):
        super().__init__()
        self._methods = list()
        self.menu = _menu

    def reset_methods(self):
        for tup in self._methods:
            tup[3] = True

    def run_npc(self, player):
        pass

    def run_user(self, player):
        self.menu.add_frame(frame_type="list", header=self.name,
                            prompt="Choose # from below:",
                            content=self.options)
        while True:
            choice = self.menu.display(get_input=True)
            self.options[choice][1](player)

    @property
    def methods(self):
        """Return list of tuples containing Phase methods and information about them

        :return: [("name", Function obj, "tooltip", is_valid_option)]
        :rtype:  [(String, Function object, String, Bool)]
        """
        return self._methods

    @property
    def options(self):
        pass

    def end_turn(self, *args):
        raise EndTurn

    def exit(self, *args):
        self.menu.add_frame(frame_type="exit")
        choice = self.menu.display(get_input=True)

        print(choice)
        if choice:
            raise ExitCondition


class BettingPhase(BlackjackPhase):
    """First Blackjack phase, gathers bets from each player

    (*)<- Inherited
    :attributes:
        *menu: Menu object shared throughout program objects
        *bets: Dictionary of {player:bet}
    """
    bets = dict()
    name = "Betting Phase"

    def __init__(self, _menu: Menu):
        super().__init__(_menu=_menu)
        self._methods = [["Bet",      self.get_bet,  "Place your bet.",      True],
                         ["End Turn", self.end_turn, "End your turn.",       True],
                         ["Exit",     self.exit,     "Return to main menu.", True]]
        self.menu = _menu

    def run_npc(self, player: BlackjackNPC):
        pass

    def run_user(self, player: BlackjackUser):
        while len(self.options) > 2:
            self.menu.add_frame(frame_type="list",
                                header=self.name,
                                prompt="Choose from below:",
                                content=[opt[0] for opt in self.options])
            choice = self.menu.display(get_input=True)

            self.options[int(choice) - 1][1](player)
        self.reset_methods()

    def get_bet(self, player):
        self.menu.add_frame(frame_type="custom",
                            header="PLACE BET",
                            prompt=f"How much would you like to bet? (Max: {player.bankroll})\n"
                                   f"Enter '0' to go back.")

        amount = self.menu.display(get_input=True,
                                   check=lambda inp: True if (check_int(inp) and
                                                              0 <= int(inp) <= player.bankroll) else False)
        if amount != '0':
            player.take_bank(int(amount))
            self.bets[player] = int(amount)
            self._methods[0][3] = False

    def end_turn(self, player):
        warning = "Are you sure you want to end your turn?"
        if player not in self.bets.keys():
            warning += " You will sit this round out if you do not bet!"

        self.menu.add_frame(frame_type="end", prompt=warning)
        u_in = self.menu.display(get_input=True)
        if u_in:
            raise EndTurn


    @property
    def options(self):
        valid_options = list(filter(lambda tup: True if tup[3] is True else False, self._methods))
        return [valid_options[i] for i in range(len(valid_options))]


class BlackjackRules(RulesABC):
    phase_list = [BettingPhase]

    def __init__(self):
        super().__init__()
