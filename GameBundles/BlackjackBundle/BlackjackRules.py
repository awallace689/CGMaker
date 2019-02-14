from Generics.ABCs import RulesABC, PhaseABC, EndTurn, ExitCondition
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser
from Generics.Menu import Menu, check_int
from math import ceil


class BlackjackPhase(PhaseABC):
    """Superclass for all Blackjack phases.

    :attributes:
        menu: Menu object used throughout program for user-interaction
        _methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
        menu: Menu object shared by program
        name: string identifying name of phase

    :properties:
        options: return list of tuples containing unselected player options

    :methods:
        run_user(player)
            runs User implementation of phase on 'player'

        run_npc(player)
            runs NPC implementation of phase on 'player'

        end_turn()
            confirms user selection, resets self.methods and raises EndTurn exception

        exit()
            confirms user selection, raises ExitCondition exception
    """
    menu = None
    name = None

    def __init__(self, _menu: Menu):
        super().__init__()
        self._methods = list()
        self.menu = _menu

    @property
    def options(self):
        """Return list of tuples containing unselected player options (to prevent repeat selections)

        :return: List, containing tuples from self._methods with index 3 = True
        """
        return list(filter(lambda tup: tup[3], self._methods))

    def reset_methods(self):
        """Resets self._methods[3] = True for every item in self._methods

        :return: None
        """
        for tup in self._methods:
            tup[3] = True

    def run_npc(self, player):
        """Phase implementation for BlackjackNPCs

        :param player: BlackjackNPC, player to run phase on
        :return: None
        """
        pass

    def run_user(self, player):
        """Phase implementation for Users

        :param player: BlackjackUser, player to run phase on
        :return: None
        """
        pass

    def end_turn(self, *args):
        """Confirm intention with user, reset self._methods and raise EndTurn exception

        :return: None
        :raises: EndTurn, if user confirms selection
        """
        self.menu.add_frame(frame_type="end")
        u_in = self.menu.display(get_input=True)
        if u_in:
            raise EndTurn

    def exit(self, *args):
        """Confirm intention with user, reset self._methods and raise EndTurn exception

        :return: None
        :raises: ExitCondition, if user confirms selection
        """
        self.menu.add_frame(frame_type="exit")
        choice = self.menu.display(get_input=True)

        if choice:
            raise ExitCondition


class BettingPhase(BlackjackPhase):
    """First Blackjack phase, gathers bets from each player

    :attributes:
        menu: Menu object used throughout program for user-interaction
        _methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
        bets: Dictionary of {Player: int}
        name: String identifying name of phase

    :methods:
        run_user(player)
            runs User implementation of phase on 'player'

        run_npc(player)
            runs NPC implementation of phase on 'player'

        end_turn()
            confirms user selection, resets self.methods and raises EndTurn exception

        get_bet()
            asks user for bet, checks if valid
    """
    bets = dict()
    name = "Betting Phase"

    def __init__(self, _menu: Menu):
        super().__init__(_menu=_menu)
        self._methods = [["Bet",      self.get_bet,  "Place your bet.",      True],
                         ["End Turn", self.end_turn, "End your turn.",       True],
                         ["Exit",     self.exit,     "Return to main menu.", True]]
        self.menu = _menu

    def run_npc(self, player: BlackjackNPC):
        pass

    def run_user(self, player: BlackjackUser):
        """Collect valid bets from 'player'

        :param player: BlackjackNPC, player to run phase on
        :return: None
        """
        while len(self.options) > 2:
            self.menu.add_frame(frame_type="list",
                                header=self.name,
                                prompt="Choose from below:",
                                content=[opt[0] for opt in self.options])
            choice = self.menu.display(get_input=True)

            self.options[int(choice) - 1][1](player)
        self.reset_methods()

    def get_bet(self, player):
        """Take user-input amount from player.bankroll and add to self.bets

        :param player: BlackjackNPC, player to collect bet from
        :return:
        """
        self.menu.add_frame(frame_type="custom",
                            header="PLACE BET",
                            prompt=f"How much would you like to bet? (Max: {player.bankroll})\n"
                                   f"Enter '0' to go back.")

        amount = self.menu.display(get_input=True,
                                   check=lambda inp: True if (check_int(inp) and
                                                              0 <= int(inp) <= player.bankroll) else False)
        if amount != '0':
            player.take_bank(int(amount))
            self.bets[player] = int(amount)
            self._methods[0][3] = False

    def end_turn(self, player):
        """Confirm intention with user, reset self._methods and raise EndTurn exception

        :return: None
        :raises: EndTurn, if user confirms selection
        """
        warning = "Are you sure you want to end your turn?"
        if player not in self.bets.keys():
            warning += " You will sit this round out if you do not bet!"

        self.menu.add_frame(frame_type="end", prompt=warning)
        u_in = self.menu.display(get_input=True)
        if u_in:
            raise EndTurn


class MainPhase(BlackjackPhase):
    """Second Blackjack phase, allows user to hit until they choose to stand

        :attributes:
            menu: Menu class used throughout program for user-interaction
            _methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
            deck: BlackjackDeck class for use with phase methods
            dealer: Dealer class for use with phase methods
            name: String identifying name of phase

        :methods:
            run_user(player)
                runs User implementation of phase on 'player'

            run_npc(player)
                runs NPC implementation of phase on 'player'

            end_turn()
                confirms user selection, resets self.methods and raises EndTurn exception

            get_bet()
                asks user for bet, checks if valid

            hit(player)
                add card to player hand

            stand()
                raise EndTurn exception
        """

    name = "Main Phase"

    def __init__(self, _menu: Menu, _deck, dealer: BlackjackNPC):
        super().__init__(_menu=_menu)
        self._methods = [["Hit",      self.hit,      "Add a card to your hand.", True],
                         ["Stand",    self.stand,    "End your turn.",           True],
                         ["End Turn", self.stand,    "End your turn.",           False],
                         ["Exit",     self.exit,     "Return to main menu.",     True]]
        self.deck = _deck
        self.dealer = dealer

    def run_user(self, player):
        """Keep track of hand total while allowing player to hit/stand

        :param player: BlackjackUser, player to run phase on
        :return: None
        """
        while len(self.options):
            # if hand total is > 20, disable hit/stand option
            if min(player.hand.get_totals()) > 20:
                self._methods[0][3] = False
                self._methods[1][3] = False
                self._methods[2][3] = True

            # calculate hand totals
            d_hand_string = self.dealer.hand.get_hand_str()
            d_totals_string = str(self.dealer.hand.get_totals())[1:-1]

            hand_string = player.hand.get_hand_str()
            totals_string = str(player.hand.get_totals())[1:-1]

            # user selects option
            self.menu.add_frame(frame_type="list",
                                header=self.name,
                                prompt=f"Dealer hand: {d_hand_string}\nDealer Total(s): {d_totals_string}\n\n"
                                       f"Hand: {hand_string}\nTotal(s): {totals_string}\n\nChoose from below:",
                                content=[opt[0] for opt in self.options])
            choice = self.menu.display(get_input=True)
            self.options[int(choice) - 1][1](player)
        self.reset_methods()

    def hit(self, player):
        """Add card to player.hand

        :param player: BlackjackUser or BlackjackNPC
        :return: None
        """
        if self.deck.deck_size > 0:
            player.hand.add(self.deck.draw_deck())

        else:
            self.deck = self.deck.new_deck()
            player.hand.add(self.deck.draw_deck())

    def stand(self, *args):
        """End current turn

        :return: None
        :raises: EndTurn
        """
        raise EndTurn

    def reset_methods(self):
        """Resets

        :return:
        """
        for i in range(len(self._methods)):
            if i == 2:
                self._methods[i][3] = False

            else:
                self._methods[i][3] = True


class EndPhase(BlackjackPhase):
    """First Blackjack phase, gathers bets from each player

        :attributes:
            menu: Menu object used throughout program for user-interaction
            _methods: return list of tuples containing player options [("name", Function object, "tooltip", Bool)]
            bets: Dictionary of {Player: int}
            name: String identifying name of phase

        :methods:
            run_user(player)
                runs User implementation of phase on 'player'

            run_npc(player)
                runs NPC implementation of phase on 'player'

            end_turn()
                confirms user selection, resets self.methods and raises EndTurn exception

            get_bet()
                asks user for bet, checks if valid
        """
    name = "Results"

    def __init__(self, _menu: Menu, dealer: BlackjackNPC):
        super().__init__(_menu=_menu)
        self._methods = [["Next Round", self.end_turn, "End your turn.",       True],
                         ["Exit",       self.exit,     "Return to main menu.", True]]
        self.dealer = dealer

    def run_user(self, bet_dict):
        """Display results screen to User, change bankroll accordingly

        :param bet_dict: dict, collection of bets made by each user
        :return: None
        """
        results_string = ""

        def get_value(player):
            """Determine if user busts, else return max in player.hand.get_totals()

            :param player: BlackjackUser
            :return: string, best value of hand to display to user
            """
            totals = player.hand.get_totals()
            if min(totals) > 21:
                return str(min(totals)) + ", Bust!"

            else:
                return str(max([totals[_i] for _i in range(len(totals)) if totals[_i] < 22]))

        def get_result(player):
            """Compare dealer hand value to user hand value, return int for change in player.bankroll

            :param player: BlackjackUser or BlackjackNPC
            :return: int, change to apply to player.bankroll
            """
            try:
                result = int(get_value(player))

            except ValueError:
                return 0

            try:
                d_result = int(get_value(self.dealer))

            except ValueError:
                return ceil(bet_dict[player] * 1.5)

            if d_result == result:
                return bet_dict[player]

            elif d_result > result:
                return 0

            elif d_result < result:
                return ceil(bet_dict[player] * 1.5)

        # display result of round
        results_string += f"DEALER:\n\tHand: {str(self.dealer.hand)}\tHand Total: {str(get_value(self.dealer))}\n"

        for i in range(len(bet_dict.keys())):
            player_list = list(bet_dict.keys())
            if isinstance(player_list[i], BlackjackNPC):
                results_string += f"Player {i + 1}:\n"

            else:
                results_string += "YOU:\n"

            results_string += f"\tHand: {str(player_list[i].hand)}" +               \
                              f"\tHand Total: {str(get_value(player_list[i]))}\n" + \
                              f"\tBet: {str(bet_dict[player_list[i]])}\n" +         \
                              f"\tWinnings: {str(get_result(player_list[i]))}\n"

            # edit player.bankroll for each player
            player_list[i].bankroll += bet_dict[player_list[i]]

            player_list[i].bankroll += get_result(player_list[i]) - bet_dict[player_list[i]]

            results_string += f"\tNew Bankroll: {str(player_list[i].bankroll)}\n" + \
                              f"\tNet Change: {str(player_list[i].bankroll - 300)}"

        self.menu.add_frame(frame_type="list",
                            header=self.name,
                            prompt=results_string + "\n\nChoose from below:",
                            content=[opt[0] for opt in self.options])
        choice = self.menu.display(get_input=True)
        self.options[int(choice) - 1][1]()

    def end_turn(self, *args):
            raise EndTurn


class BlackjackRules(RulesABC):
    """List of phases to run, in-order

    :attributes:
        phase_list: List containing each phase to run in BlackjackGameManager, in-order
    """
    phase_list = [BettingPhase, MainPhase, EndPhase]

    def __init__(self):
        super().__init__()
