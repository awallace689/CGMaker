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
                {"Name String": Phase obj}
        """
        pass


class Phase(ABC):
    @property
    def methods(self):
        """ Returns array of tuples '('method obj', 'info string')' """
        pass
