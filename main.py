"""
====================================================================================================
@Author: Adam Wallace
@Date: 1/30/2019
@About: Stack-based Menu class and templates provided by Frame classes provide a clean,
        multi-purpose console interface for user-interaction.
@Note: Menu.display() automatically checks for valid input on provided templates.
====================================================================================================
"""
from Generics.Menu import Menu
from Generics.ABCs import ExitCondition
from sys import modules


game_list = [("Blackjack", "Play Blackjack with up to 7 other NPCs!"),
             ("Exit",      "Exit program.")]

title_string = '*' * 30 + '\n' +\
               '*' + '-' * 11 + "WELCOME" + '-' * 10 + '*' + '\n' +\
               '*' + '-' * 13 + "TO" + '-' * 13 + '*' + '\n' +\
               '*' + '-' * 11 + "CGMAKER" + '-' * 10 + '*' + '\n' +\
               '*' * 30 + '\n' +\
               "Author: Adam Wallace" + '\n'


if __name__ == "__main__":
    choice = ""
    while choice != "2":

        if choice != "":
            del _Menu
            del _list
            del GameManager
            del GM

            if choice == "1":
                del modules["Controllers.BlackjackGameManager"]

        _Menu = Menu()
        _list = [tup[0] for tup in game_list]
        _Menu.add_frame(frame_type="list",
                        content=_list,
                        header="CGMAKER",
                        prompt=title_string + "Select one of the following:")

        choice = _Menu.display(get_input=True)
        if choice == "1":
            from Controllers.BlackjackGameManager import BlackjackManager as GM
        else:
            print(f'[END] Frame_Stack length: {len(_Menu.frame_stack)}')
            quit(-1)

        GameManager = GM()
        while True:
            try:
                GameManager.run()

            except ExitCondition:
                break
