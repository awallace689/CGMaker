from Generics.ABCs import RulesABC, PhaseABC, abstractmethod, EndTurn
from Generics.Player import Player
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from Generics.Menu import Menu

#
# def is_playing(func):
#     def wrapper(self, player: BlackjackPlayer, *args):
#         if player.is_playing:
#             return func(self, player, *args)
#
#         else:
#             raise NotPlayingError
#     return wrapper


class BlackjackPhase(PhaseABC):
    def __init__(self):
        super().__init__()
        self._methods = None

    @abstractmethod
    def run_npc(self, player):
        pass

    @abstractmethod
    def run_user(self, player):
        pass

    @property
    def methods(self):
        """
        :return: [("name", Function obj, "tooltip")]
        """
        return self._methods

    def end_turn(self, *args):
        raise EndTurn


class BettingPhase(BlackjackPhase):
    def __init__(self):
        super().__init__()
        self._methods = [("Bet", self.get_bet, "Place your bet."),
                         ("End Turn", self.end_turn, "End your turn."),
                         ("Exit", self.exit, "Return to main menu.")]

    def run_npc(self, player):
        pass

    def run_user(self, player):
        initial_bank = player.bankroll
        menu = Menu(header="[Betting Phase]\n")
        menu.clear()

        index = get_input(up_list=self._methods, menu=menu, player=player) - 1
        menu.clear()
        self._methods[index][1](player, menu)

    @staticmethod
    def take_bank(player, amount):
        player.bankroll -= amount
        return amount

    def bet(self):
        pass

    @classmethod
    def get_bet(cls, player, menu):
        amount = get_input(amount=True, player=player, menu=menu)
        return cls.take_bank(player, amount)


class BlackjackRules(RulesABC):
    phase_list = [("Betting Phase", BettingPhase())]

    def __init__(self):
        super().__init__()


def get_input(up_list=None, menu=None, amount=False, player=None, query=False, query_string=""):
    """
    :param up_list: from BlackjackPhase.methods, [("name", Function object, "tooltip")]
    :param menu: Menu object, instantiated in BlackjackGameManager
    :param amount: Bool, amount=False: Requesting Menu selection
                         amount=True : Requesting any positive integer
    :param player: Player object, required for displaying max amount when amount=True
    :param query: Bool, query=True: poses query and evaluates y/n response
    :param query_string: String, if query=True, queryString will display in addition to (y/n) tooltip
    :return: amount=False: int, index of selected option (function) in BlackjackPhase.methods
             amount=True : int, any positive integer <= player.bankroll

             query=False: int, see above
             query=True : Bool, corresponds to response of "y" or "n", amount cannot also be True
    """
    try:
        if amount:
            if query:
                raise ValueError("'query' and 'amount' cannot both be set to True.")

            if player:
                uin = input(f"Enter amount: (max {player.bankroll})\n> ")
                assert int(uin) > 0
                assert int(uin) <= player.bankroll

            else:
                uin = input(f"Enter amount:\n> ")
                assert int(uin) > 0

        else:
            if query:
                uin = input(query_string + " (y/n)\n> ")
                if uin.lower() == 'y':
                    return True

                elif uin.lower() == 'n':
                    return False

                else:
                    raise ValueError

            elif up_list is not None and isinstance(menu, Menu):
                uin = input(menu.generate(up_list))
                assert int(uin) <= len(up_list)
                assert int(uin) >= 1

            elif up_list is None and menu is None:
                uin = input("> ")

            else:
                raise TypeError(f"'menu' is type: '{type(menu)}', expected object type: 'Menu'.'up_list' is type:"
                                f" '{type(up_list)}', expected object type: 'List'.")
        return int(uin)

    except (TypeError, ValueError):
        Menu.clear(Menu())
        print("*Invalid input. Try again...*")
        return get_input(up_list, menu, amount, player, query, query_string)

    except AssertionError:
        Menu.clear(Menu())
        print("*Selection out of range. Try again...*")
        return get_input(up_list, menu, amount, player, query, query_string)
