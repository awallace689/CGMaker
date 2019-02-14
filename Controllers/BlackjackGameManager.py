from Generics.ABCs import GameManagerABC, EndTurn, ExitCondition
from Generics.Menu import Menu, check_int
from GameBundles.BlackjackBundle.BlackjackGenericsMods import BlackjackNPC, BlackjackUser, BlackjackCard, BlackjackDeck
from GameBundles.BlackjackBundle.BlackjackRules import BlackjackRules
from random import shuffle


def make_user(bankroll=300):
    return BlackjackUser(bankroll)


def make_npc(bankroll=300):
    return BlackjackNPC(bankroll)


class BlackjackManager(GameManagerABC):
    """Handles high-level game operations, running phases on list of valid players, adding/removing of players

    (*)<- Inherited
    :attributes:
        *menu  : Generics.Menu.Menu object shared throughout program
        playing: list of BlackjackNPC and/or BlackjackPlayer in '_players' with bankroll > 0

    :methods:
        add_players(self, count: int, player_type=None, bankroll=300)
            Add 'count' BlackjackPlayer or BlackjackNPC objects to '_players' with default bankroll 300.
        remove_player(self, i: int)
            Removes player from '_players' at index 'i'

    :private:
        :variables:
            *_players: list of BlackjackUser and/or BlackjackNPC objects
            *_phases : list of game phases to run on each (playing) player, from BlackjackRules.phase_list

    """
    def __init__(self, _menu=Menu()):
        super().__init__()
        self.menu = _menu
        self._players = []
        self._dealer = BlackjackNPC()
        self._deck = BlackjackDeck()
        self._phases = [BlackjackRules.phase_list[0](self.menu),
                        BlackjackRules.phase_list[1](self.menu, self._deck, self._dealer),
                        BlackjackRules.phase_list[2](self.menu, self._dealer)]

    @property
    def playing(self):
        """Get list of players who "pass" the inner function 'check'

        :return: List of BlackjackPlayer and/or BlackjackNPC objects
        """
        def check(player):
            if player.bankroll > 0:
                return True
            else:
                return False

        return [self._players[i] for i in range(len(self._players)) if check(self._players[i])]

    def add_players(self, count, player_type, bankroll=300):
        """Add 'count' BlackjackPlayer or BlackjackNPC objects to '_players' with default bankroll 300

        :param count: Int, number of players of one type to add
        :param player_type: None, no character created
                            "npc", BlackjackNPC
                            "user", BlackjackUser

        :kwargs:
            :param bankroll: =default: sets bankroll of created players to 300
                             =int    : sets bankroll of created players to 'int'

        :return: None
        """
        assert(len(self._players) + count - 1 < 8)
        assert(count >= 0)

        if player_type.lower() == "npc":
            self._players += [make_npc(bankroll=bankroll) for _ in range(count)]

        elif player_type.lower() == "user":
            self._players += [make_user(bankroll=bankroll) for _ in range(count)]

        else:
            raise ValueError

    def remove_player(self, i):
        """Removes player from '_players' at index 'i'

        :param i: int, index
        :return: None
        """
        self._players.pop(index=i)

    def run_on_playing(self):
        """Calls each BlackjackRules.BlackjackPhase.run_X method on each valid player in self.playing

        :return: None
        """
        while len(list(filter(lambda p: isinstance(p, BlackjackUser), self.playing))) > 0:

            self._phases[0].bets = {}
            self._dealer.hand.cards = []
            for player in self._players:
                player.hand.cards = []

            # Run BettingPhase on all in self.playing to generate bets
            for player in self.playing:
                try:
                    self._phases[0].run_self(player)

                except EndTurn:
                    self._phases[0].reset_methods()
                    continue

            # Deal to all who bet and one to dealer
            for _ in range(2):
                for player in self._phases[0].bets.keys():
                    self.deal(player)
            self.deal(self._dealer)

            # Run Main Phase on each player who bet in BettingPhase
            for player in self._phases[0].bets.keys():
                try:
                    self._phases[1].run_self(player)

                except EndTurn:
                    self._phases[1].reset_methods()
                    continue

            # Dealer's Main Phase
            while min(self._dealer.hand.get_totals()) < 17:
                self.deal(self._dealer)

            # Show Results
            try:
                self._phases[2].run_self(self._phases[0].bets)

            except EndTurn:
                continue
        raise ExitCondition

    def deal(self, player):
        if self._deck.deck_size > 0:
            player.hand.add(self._deck.draw_deck())

        else:
            self._deck = self._deck.new_deck()
            player.hand.add(self._deck.draw_deck())

    def run(self):
        """Inherited method called in order to run Blackjack game.

        :return: None
        """
        self._players = [BlackjackUser()]
        self.run_on_playing()
