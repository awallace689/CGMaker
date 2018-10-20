from Generics.ABCRules import ABCRules, Phase
from Generics.Player import Player
from Generics.Menu import Menu


class BlackjackRules(ABCRules):
    def __init__(self):
        pass

    @property
    def phases(self):
        phase_dict = {"Betting Phase": BettingPhase,
                      "end": "func3, func4"}
        return phase_dict


class BettingPhase(Phase):
    def __init__(self):
        self._methods = [(self.bet, "Bet doc here.")]

    @property
    def methods(self):
        return self._methods

    # returns list of tuples "('function obj', 'info string')"
    _methods = []

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
