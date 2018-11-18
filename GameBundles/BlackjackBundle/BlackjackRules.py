from Generics.ABCs import RulesABC, PhaseABC
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackPlayer, NegativeBankroll, NotPlayingError
from Generics.Menu import Menu


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


class BlackjackRules(RulesABC):
    def __init__(self):
        self.phase_dict = {"Betting Phase": BettingPhase()}

    @property
    def phases(self):
        return self.phase_dict


class BettingPhase(PhaseABC):
    def __init__(self):
        self._methods = [("Bet", self.get_bet, "Place your bet."),
                         ("Exit", self.exit, "Return to main menu.")]

    @property
    def methods(self):
        """
        :return: [("name", Function obj, "tooltip")]
        """
        return self._methods

    @staticmethod
    def take_bank(player: BlackjackPlayer, amount):
        player.bankroll -= amount
        return amount

    @classmethod
    def get_bet(cls, player: BlackjackPlayer, amount):
        try:
            return cls.take_bank(player, amount)
        except AssertionError:
            print("*Cannot bet more than exists in bankroll.*")
            return cls.get_bet(player, amount)


def get_input(up_list=None, menu=None, amount=False, player=None):
    """
    :param up_list: from BlackjackPhase.methods, [("name", Function object, "tooltip")]
    :param menu: Menu object, instantiated in BlackjackGameManager
    :param amount: Bool, amount=False: Requesting Menu selection
                         amount=True : Requesting any positive integer
    :param player: Player object, required for displaying max amount
    :return: int, amount=False: index of selected option (function) in BlackjackPhase.methods
                  amount=True : any positive integer <= player.bankroll
    """
    try:
        if amount:
            if player:
                uin = input(f"Enter amount: (max {player.bankroll})\n> ")
                assert int(uin) > 0
                assert int(uin) <= player.bankroll

            else:
                uin = input(f"Enter amount:\n> ")
                assert int(uin) > 0
        else:
            if up_list is None and menu is None:
                uin = input("> ")

            elif up_list is not None and isinstance(menu, Menu):
                uin = input(menu.generate(up_list))
                assert int(uin) <= up_list.__len__()
                assert int(uin) >= 1

            else:
                raise TypeError(f"'menu' is type: '{type(menu)}', expected object type: 'Menu'.'up_list' is type:"
                                f" '{type(up_list)}', expected object type: 'List'.")
        return int(uin)

    except (TypeError, ValueError):
        menu.clear()
        print("*Invalid input. Try again...*")
        return get_input(up_list, menu, player, amount)

    except AssertionError:
        menu.clear()
        print("*Selection out of range. Try again...*")
        return get_input(up_list, menu, player, amount)
