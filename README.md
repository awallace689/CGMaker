# CardGame
A Python Project

What is CardGame?

    CardGame houses a framework through which one can quickly implement different card games, collected into a
    "GameBundle," which can then be run and played in any terminal/bash.

Why make CardGame?

    CardGame is my first python project, created for the purpose of familiarizing myself with concepts
    including but not limited to: 

    duck-typing, 

    polymorphism, 

    abstract base classes, 

    pythonic class design, 

    but most of all -- modular code design. Using these concepts in practice will allow me to develop various
    GameBundles with ease, all-the-while keeping my code understandable and easy to work with.

CardGame's Goal

    The large amount of inherited functionality by design allows for rapid GameBundle development. It's 
    benefits so far are best exemplified by the Blackjack implementation. 
    
    CardGame/GameBundle/BlackjackBundle/ only needs to slightly extend the functionality of some generic 
    objects before all that's left to do is implement the game-specific rules and phases.
    
CardGame's Future
    
    Once a working console/terminal prototype is built, I plan on developing either a web application or
    desktop application that can be used instead to run the game.

CardGame's Implementation

    Contents:
     Generics: Generic classes which provide common functionality. Extended by GameBundles/GameRules.py.
        
     GameBundles: Contains a GameBundle subdirectory containing /Generic/ extensions and a GameRules.py file.
        
     Controllers: Contains files which interact with a GameRules.py file and the user through the Menu class. 
                      Receives a list of Phases from file, the order in which to run them, and each Phase
                      provides a list of member functions. Controllers may be extended by a GameRules.py file.
        
     main.py: Handles GameBundle selection, as well as the creation of any Controllers necessary to run game.
                    
