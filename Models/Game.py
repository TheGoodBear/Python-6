"""
    Class
"""

import time
import pygame
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
"""\nBonjour {0}.
\nTu viens de pénétrer dans une grotte
mais l'entrée s'est effondrée derrière toi.
\nTu dois maintenant sortir du labyrinthe...
\nIl te faudra pour cela avoir collecté les
objets nécessaires à l'ouverture de la porte. 
\nDéplace toi grâce aux flèches du clavier
ou appuie sur ESC pour quitter le jeu,
et mourrir de fin dans le labyrinthe...
\nBonne chance."""
        Message = Message.format(cls.Player.Name)
        # print(Message)
        Util.Write(Message, FontSize = 14)
        # play sounds
        Util.ManageSound("CaveIn", Repeat = 3)
        time.sleep(1)
        Util.ManageSound("Ready")

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

        # game ended, go to final loop
        cls.FinalLoop()


    @staticmethod
    def FinalLoop():
        """
            Wait for application end
        """

        EndOfApplication: bool = False
        while not EndOfApplication:
            for Event in pygame.event.get():
                # get player input
                if (Event.type == pygame.QUIT):
                    # if game exits (user click on red cross in upper right)
                    EndOfApplication = True
                elif (Event.type == pygame.KEYDOWN):
                    if (Event.key == pygame.K_ESCAPE):
                        EndOfApplication = True
