"""
    Class
"""

import Utilities.GlobalVariables as GV
import Utilities.Utilities as Util
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
        #cls.Player.GetPlayerData()
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
        Message = \
"""Très bien {0}, ton objectif est de sortir du labyrinthe.
Pour cela il te faudra trouver la sortie et avoir collecté les objets nécessaires à l'ouverture de la porte. 
Tu es représenté par {1} et la porte de sortie par {2}. 
À chaque tour tu peux effectuer l'une des actions suivantes :
Te déplacer grâce aux flèches ou appuyer sur ESC pour quitter le jeu (et perdre...)
Bonne chance."""
        Message = Message.format(
            cls.Player.Name,
            cls.Player.ImageNames[0],
            MazeElement.GetElement(Maze, "Sortie").ImageNames[0])
        print(Message)
        Util.WriteText(
            Message,
            GV.DialogPlaceholder.X + GV.DialogPlaceholder.TextX, 
            GV.DialogPlaceholder.Y + GV.DialogPlaceholder.TextY,
            FontName = GV.DialogPlaceholder.TextFontName,
            FontSize = GV.DialogPlaceholder.TextFontSize,
            TextColor = GV.DialogPlaceholder.TextColor)

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
