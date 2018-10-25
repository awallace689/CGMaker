from Generics.ABCs import RulesABC, PhaseABC
from Generics.Players import Player
from Generics.Menu import Menu


class BlackjackRules(RulesABC):
    def __init__(self):
        self.phase_dict = {"Betting Phase": BettingPhase}

    @property
    def phases(self):
        return self.phase_dict


class BettingPhase(PhaseABC):
    def __init__(self):
        self._methods = [(self.bet, "Bet doc here.")]

    @property
    def methods(self):
        """returns list of tuples "('function obj', 'info string')"""
        return self._methods

    def bet(self, player: Player, amount):
        try:
            player.take_bank(amount)

        except AssertionError:
            print("*Cannot bet more than exists in bankroll.*")
            return self.bet(player, amount)

        return amount


def get_input(up_list=None, menu=None):
    if up_list is None and menu is None:
        uin = input("> ")

    elif up_list is not None and isinstance(menu, Menu):
        try:
            uin = input(menu.generate(up_list))
            assert int(uin) <= up_list.__len__()
            assert int(uin) >= 1

        except (TypeError, ValueError):
            menu.clear()
            print("*Invalid input. Try again...*")
            return get_input(up_list, menu)

        except AssertionError:
            menu.clear()
            print("*Selection out of range. Try again...*")
            return get_input(up_list, menu)

    else:
        raise TypeError("'menu' is type: '{}', expected object type: 'Menu'. \
                         'up_list' is type: '{}', expected object type: 'List'.".format(type(menu),
                                                                                        type(list)))
    return uin
