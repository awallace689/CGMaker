"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains abstract base classes to ensure consistent communication methods within project.
====================================================================================================
"""
from abc import ABC, abstractmethod


class RulesABC(ABC):
    @property
    @abstractmethod
    def phases(self):
        """
        Returns dict of Phase objects:
                {"Name String": Phase obj}
        """
        pass

    @property
    @abstractmethod
    def allowed_actions(self):
        pass


class PhaseABC(ABC):
    @property
    @abstractmethod
    def methods(self):
        """Returns array of tuples '('method obj', 'info string')'"""
        pass


class GameManagerABC(ABC):
    def __init__(self, phases=None, players=list()):
        self._phases = phases
        self._players = players

    @property
    def phases(self):
        return self._phases

    @property
    def players(self):
        return self._players

    @property
    def playing(self):
        pass

    @staticmethod
    def exit_to_menu():
        exit()

    def end_game(self):
        self.exit_to_menu()
