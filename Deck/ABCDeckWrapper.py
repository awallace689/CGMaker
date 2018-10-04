"""
====================================================================================================
@Author: Adam Wallace
@Date: 10/4/2018
@About: An interface for 'DeckWrapper' providing a deck, a discard pile (deck), and several
        methods for use with either
====================================================================================================
"""
from abc import ABC, abstractmethod, abstractstaticmethod, abstractproperty

class ABCDeckWrapper(ABC):
