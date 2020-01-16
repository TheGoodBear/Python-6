"""
    Class
"""

import Utilities.GlobalVariables as GV
from Models.Character import Character
from Models.Maze import Maze
from Models.MazeElement import MazeElement
from Models.ScreenPlaceholder import ScreenPlaceholder

class Game:
    """
        Utility class used to manage the game

        Not instanciable
        Static methods only
    """

    # Class properties
    Player = None

    @classmethod
    def Initialize(cls):
        """
            Initialize game and show initial message
        """

        # 1) Initialize data
        # Initialize screen
        cls.InitializeScreen()
        # Initialize maze
        Maze.Initialize()
        # Load characters from json file
        cls.Player = Character.LoadCharactersFromFile()
        # Ask for player data
        cls.Player.GetPlayerData()
        # Place player in maze
        cls.Player.MoveInMaze()

        # 2) Draw screen
        # Draw game screen
        ScreenPlaceholder.DrawPlaceholdersOnScreen(Maze)
        # Draw maze on screen
        Maze.DrawOnScreen()

        # 3) Start game
        cls.Start()

    @classmethod
    def InitializeScreen(cls):
        """
            Initialize screen
        """

        # Load view placeholders from data file (as a dictionary)
        ScreenPlaceholders = ScreenPlaceholder.LoadPlaceholdersFromFile()
        # Instantiate each placeholder and add it to list of ScreenPlaceholder objects
        GV.MapPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Map"))
        GV.Placeholders.append(GV.MapPlaceholder)
        GV.BackpackPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Backpack"))
        GV.Placeholders.append(GV.BackpackPlaceholder)
        GV.DialogPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Dialog"))
        GV.Placeholders.append(GV.DialogPlaceholder)


    @classmethod
    def Start(cls):
        """
            Give rules to player and start the game

            :param arg1: The maze
            :type arg1: Maze
        """

        # Show initial message
        print(
            "\nTrès bien {0}, ton objectif est de sortir du labyrinthe.".format(cls.Player.Name) +
            "\nPour cela il te faudra trouver la sortie et avoir collecté les objets nécessaires à l'ouverture de la porte." + 
            "\nTu es représenté par {0} et la porte de sortie par {1}.".format(cls.Player.ImageNames[0], MazeElement.GetElement(Maze, "Sortie").ImageNames[0]) + 
            "\nÀ chaque tour tu peux effectuer l'une des actions suivantes :" + 
            "\nTe déplacer vers le (H)aut, le (B)as, la (G)auche, la (D)roite ou (Q)uitter le jeu (et perdre...)" + 
            "\nBonne chance.")

        # Game loop

        # define action speed (interval between 2 loops)
        #ActionSpeed: int = GV.Clock.tick(GV.FPS) // 1000 
        # variable for end of game
        EndOfGame: bool = False
        
        # do this until end of game is triggered
        while not EndOfGame:

            # get a player action
            PlayerAction: str = Character.GetAction()

            if(PlayerAction != ""):
                # Do action
                EndOfGame = cls.Player.ExecuteAction(PlayerAction)
