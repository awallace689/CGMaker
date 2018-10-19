from Templates.ABCRules import ABCRules, Phase
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
    _methods = []

    @property
    def methods(self):
        return self._methods


class Menu:
    def __init__(self):
        self._menu = "_UNASSIGNED_\n"

    def update(self, up_dict):
        print_string = ""
        for key, val in up_dict.items():
            print_string += "> {}) {}: {}\n".format(int(key) + 1, val.__name__(), str(key))

        if print_string != "":
            self._menu = print_string

        if self._menu[-2] != '>':
            self._menu += '> '

        return self._menu

    def generate(self, up_dict):
        self._menu = self.update(up_dict)
        return self._menu


def get_input(menu=None, **kwargs):
    if menu is None:
        uin = input("> ")

    elif isinstance(menu, Menu):
        try:
            uin = int(input(menu.generate(kwargs)))
            assert uin <= kwargs.__len__()
            assert uin >= 1

        except ValueError:
            print("*Invalid input. Try again...*")
            return get_input(menu)

        except AssertionError:
            print("*Selection out of range. Try again...")
            return get_input(menu)

    else:
        raise TypeError("'menu' is type: '{}', expected type: 'Menu'.".format(type(menu)))

    return uin


m = Menu()
inp = get_input(m)
print(inp)
