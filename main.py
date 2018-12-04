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
    menu = Menu()

    while True:
        try:
            menu.clear()
            choice = get_selection(menu)

        except (AssertionError, TypeError, ValueError):
            menu.clear()
            continue

        if choice is 1:
            from Controllers.BlackjackGameManager import BlackjackManager as GameManager

        if choice is 2:
            menu.clear()
            exit(0)

        game_manager = GameManager()
        try:
            game_manager.add_players(1, player_type="npc", bankroll=0)
            game_manager.add_players(1, player_type="user")
            try:
                game_manager.run_on_playing()

            except EndTurn:
                continue

        except ExitCondition:
            if "BlackjackManager" in modules.keys():
                del modules["BlackjackManager"]
                del game_manager
            continue
