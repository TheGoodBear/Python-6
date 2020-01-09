import GlobalVariables
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

        # 1) Initialize screen
        ScreenPlaceholders = ScreenPlaceholder.LoadPlaceholdersFromFile()
        GlobalVariables.MapPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Plan"))
        GlobalVariables.BackpackPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Sac"))
        GlobalVariables.DialogPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Légende"))


        # 2) Initialize data

        # Initialize maze
        Maze.Initialize()
        # Load characters from json file
        cls.Player = Character.LoadCharactersFromFile(Maze)
        # Ask for player data
        #Player.GetPlayerData()
        # Place player in maze
        cls.Player.PlaceInMaze(Maze)
        # Draw maze on screen
        Maze.DrawOnScreen()


        # 3) Start game
        cls.Start(Maze)


    @classmethod
    def Start(cls, Maze):
        """ 
            Give rules to player and start the game

            :param arg1: The maze
            :type arg1: Maze
        """

        print(
            "\nTrès bien {0}, ton objectif est de sortir du labyrinthe.".format(cls.Player.Name) + 
            "\nPour cela il te faudra trouver la sortie et avoir collecté les objets nécessaires à l'ouverture de la porte." + 
            "\nTu es représenté par {0} et la porte de sortie par {1}.".format(cls.Player.ImageNames[0], MazeElement.GetElement(Maze, "Sortie").ImageNames[0]) + 
            "\nÀ chaque tour tu peux effectuer l'une des actions suivantes :" + 
            "\nTe déplacer vers le (H)aut, le (B)as, la (G)auche, la (D)roite ou (Q)uitter le jeu (et perdre...)" + 
            "\nBonne chance.")

        # Game loop

        # Variable for end of game
        EndOfGame: bool = False
        
        # Do this until end of game is triggered
        while not EndOfGame:
            # Wait for a player action
            PlayerAction: str = Character.WaitForAction(cls.Player)
            # Do action
            EndOfGame = cls.Player.ExecuteAction(PlayerAction, Maze)

