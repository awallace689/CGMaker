"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains abstract base classes to ensure consistent communication methods within project.
====================================================================================================
"""
from abc import ABC, abstractmethod
from Generics.Player import User, NPC


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
    @property
    @abstractmethod
    def methods(self):
        """Returns array of tuples '("name", Function object, "tooltip")'"""
        pass

    def run_self(self, player):
        if isinstance(player, User):
            self.run_user(player)

        if isinstance(player, NPC):
            self.run_npc(player)

    @abstractmethod
    def run_user(self, player):
        pass

    @abstractmethod
    def run_npc(self, player):
        pass

    def exit(self, *args):
        raise ExitCondition


class GameManagerABC(ABC):
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
    def playing(self):
        pass
