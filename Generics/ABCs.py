"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: Contains abstract base classes to ensure consistent communication methods within project.
====================================================================================================
"""
from abc import ABC, abstractmethod


class ExitCondition(Exception):
    def __init__(self):
        pass


class RulesABC(ABC):
    @property
    @abstractmethod
    def phases(self):
        """
        Returns dict of Phase objects:
                {"Name String": Phase obj}
        """
        pass

class PhaseABC(ABC):
    @property
    @abstractmethod
    def methods(self):
        """Returns array of tuples '("name", Function object, "tooltip")'"""
        pass

    def exit(self):
        raise ExitCondition


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
    @abstractmethod
    def playing(self):
        pass

    @staticmethod
    def exit_to_menu():
        raise ExitCondition()

    def end_game(self):
        self.exit_to_menu()
