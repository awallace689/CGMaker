"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: An Abstract Base Class for card game rules sets.
====================================================================================================
"""
from abc import ABC


class ABCRules(ABC):
    @property
    def phases(self):
        """
        Returns dict of Phase objects:
                {#:Phase}
        """
        pass


class Phase(ABC):
    _methods = []

    @property
    def methods(self):
        """Returns array of methods to be run in phase."""
        pass
