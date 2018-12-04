from os import system
from os import name as os_name


class Menu:
    def __init__(self, header=""):
        self._os = os_name
        self._menu = "_UNASSIGNED_\n"
        self._header = header

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
        return self._header + self._menu

    def clear(self):
        if self._os == "posix":
            system('clear')
        elif self._os == "nt":
            system('cls')


class Frame:
    def __init__(self):
        self._header = None
        self._content = None


class AmountFrame(Frame):
    def __init__(self):
        super().__init__()
        self._prompt = None
        self._options = None


class QueryFrame(Frame):
    def __init__(self):
        super().__init__()
