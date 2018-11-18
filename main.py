from Generics.Menu import Menu
from Generics.ABCs import ExitCondition


def get_selection(menu: Menu):
    game_list = [("Blackjack", None, "Play Blackjack with up to 7 other NPCs!"),
                 ("Exit", None, "Exit program.")]
    string = '*' * 30 + '\n' +\
             '*' + '-' * 11 + "WELCOME" + '-' * 10 + '*' + '\n' +\
             '*' + '-' * 13 + "TO" + '-' * 13 + '*' + '\n' +\
             '*' + '-' * 11 + "CGMAKER" + '-' * 10 + '*' + '\n' +\
             '*' * 30 + '\n' +\
             "Author: Adam Wallace" + '\n'
    print(string)
    uin = input(menu.generate(game_list))

    assert int(uin) <= len(game_list)
    assert int(uin) > 0
    return int(uin)


if __name__ == "__main__":
    menu = Menu()

    while True:
        try:
            menu.clear()
            choice = get_selection(menu)

        except (AssertionError, TypeError, ValueError):
            menu.clear()
            choice = get_selection(menu)

        if choice is 1:
            from Controllers.BlackjackGameManager import BlackjackManager as GM

        if choice is 2:
            exit(0)

        game_manager = GM()
        try:
            game_manager.run_phases()

        except ExitCondition:
            del GM
            del game_manager
            continue
