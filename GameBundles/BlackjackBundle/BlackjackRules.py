from Templates.ABCRules import ABCRules, Phase
from Templates.Player import Player
from GameBundles.BlackjackBundle.BlackjackTemplateMods import BlackjackDeck, BlackjackCard


class BlackjackRules(ABCRules):
    def __init__(self):
        pass

    @property
    def phases(self):
        phase_dict = {"Betting Phase": BettingPhase,
                      "end": "func3, func4"}
        return phase_dict


class BettingPhase(Phase):
    @property
    def methods(self):
        return self._methods

    # returns list of tuples "('function obj', 'info string')"
    _methods = []

    def bet(self, player: Player, amount):
        player.take_bank(amount)


class Menu:
    def __init__(self):
        self._menu = "_UNASSIGNED_\n"

    @property
    def get_str(self):
        return self._menu

    def update(self, up_list):
        print_string = ""
        option_num = 1

        for i in range(up_list):
            print_string += "> {}) {}: {}\n".format(i + 1, str(up_list[i][0]), up_list[i][1])
            option_num += 1

        if print_string != "":
            self._menu = print_string

        if self._menu[-2] != '>':
            self._menu += '> '

        return self._menu

    def generate(self, up_dict):
        self._menu = ""
        self._menu = self.update(up_dict)
        return self._menu


def get_input(up_list, info_list, menu=None):
    if menu is None:
        uin = input("> ")

    elif isinstance(menu, Menu):
        try:
            uin = int(input(menu.generate(up_list, info_list)))
            assert uin <= up_list.__len__()
            assert uin >= 1

        except ValueError:
            print("*Invalid input. Try again...*")
            return get_input(menu)

        except AssertionError:
            print("*Selection out of range. Try again...*")
            return get_input(menu)

    else:
        raise TypeError("'menu' is type: '{}', expected object type: 'Menu'.".format(type(menu)))

    return uin


m = Menu()
inp = get_input(BettingPhase.methods, m)
