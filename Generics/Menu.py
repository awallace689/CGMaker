from os import system as sys
from os import name as os_name


class Menu:
    def __init__(self):
        self._os = os_name
        self._menu = "_UNASSIGNED_\n"

    @property
    def get_str(self):
        return self._menu

    def update(self, up_list):
        print_string = ""
        for i in range(len(up_list)):
            print_string += f"> {i + 1}) {up_list[i][0]}: {up_list[i][2]}\n"

        if print_string != "":
            self._menu = print_string

        else:
            self._menu = "_EMPTY_\n"

        if self._menu[-2] != '>':
            self._menu += '> '

        return self._menu

    def generate(self, up_list):
        self._menu = ""
        self._menu = self.update(up_list)
        return self._menu

    def clear(self):
        if self._os == "posix":
            sys('clear')
        elif self._os == "nt":
            sys('cls')
