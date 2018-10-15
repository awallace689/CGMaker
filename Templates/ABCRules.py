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
        pass

    @property
    def methods(self):
        pass

