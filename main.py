from Generics.Menu import Menu
from Generics.ABCs import ExitCondition, EndTurn
from sys import modules


def get_selection(_menu: Menu):
    game_list = [("Blackjack", None, "Play Blackjack with up to 7 other NPCs!"),
                 ("Exit", None, "Exit program.")]
    string = '*' * 30 + '\n' +\
             '*' + '-' * 11 + "WELCOME" + '-' * 10 + '*' + '\n' +\
             '*' + '-' * 13 + "TO" + '-' * 13 + '*' + '\n' +\
             '*' + '-' * 11 + "CGMAKER" + '-' * 10 + '*' + '\n' +\
             '*' * 30 + '\n' +\
             "Author: Adam Wallace" + '\n'
    print(string)
    uin = input(_menu.generate(game_list))

    assert int(uin) <= len(game_list)
    assert int(uin) > 0
    return int(uin)


if __name__ == "__main__":
    Menu = Menu()
    _list = ["option 1", "option 2", "option 3"]
    Menu.add_frame(frame_type="list", content=_list, header="OPTIONS", prompt="Select one of the following:")
    print(Menu.display(get_input=True, check=lambda inp: True if check_digit(inp) and int(inp) > 1 else False))
