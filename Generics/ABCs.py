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
    def allowed_actions(self):
        pass


class PhaseABC(ABC):
    @property
    @abstractmethod
    def methods(self):
        """Returns array of tuples '('method obj', 'info string')'"""
        pass


class GameManagerABC(ABC):
    @property
    @abstractmethod
    def phases(self):
        pass

    @property
    def players(self):
        pass

    def run_game(self):
        pass

    def end_game(self):
        pass
