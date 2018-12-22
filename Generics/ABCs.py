"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains abstract base classes to ensure consistent communication methods within project.
====================================================================================================
"""
from abc import ABC, abstractmethod
from Generics.Player import User, NPC
from Generics.Menu import Menu


class ExitCondition(Exception):
    def __init__(self):
        pass


class EndTurn(Exception):
    def __init__(self):
        pass


class RulesABC(ABC):
    @property
    def phases(self):
        """
        :returns: {"Name String": Phase obj}
        """
        raise NotImplemented


class PhaseABC(ABC):
    menu = None

    def __init__(self):
        pass

    def run_self(self, arg):
        if isinstance(arg, User):
            self.run_user(arg)

        elif isinstance(arg, NPC):
            self.run_npc(arg)

        elif isinstance(arg, dict):
            self.run_user(arg)

    @abstractmethod
    def run_user(self, player):
        pass

    @abstractmethod
    def run_npc(self, player):
        pass

    def exit(self, *args):
        raise ExitCondition


class GameManagerABC(ABC):

    menu = Menu()

    def __init__(self, phases=None, players=list()):
        self._phases = phases
        self._players = players

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, phases):
        """
        :param phases: takes output from BlackjackRules.phases
        """
        self._phases = phases

    @property
    def players(self):
        return self._players

    @property
    @abstractmethod
    def run(self):
        pass
