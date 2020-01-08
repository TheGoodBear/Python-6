from Models.Character import Character
from Models.Maze import Maze

class Game:
    """
        Utility class used to manage the game

        Not instanciable
        Static methods only
    """

    # Class properties
    Player = None

    @staticmethod
    def Initialize():
        """ 
            Initialize game and show initial message
        """

        # 1) Interact with player

        print("\nBonjour humain, merci de t'identifier afin que je puisse interagir avec toi.")
        # Ask for player data
        Character.GetPlayerData()

        # 2) Initialize data

        # Initialize maze
        Maze.Initialize()
        # Place player in maze
        Player.PlaceInMaze(Maze)
        # Draw maze on screen
        Maze.DrawOnScreen()
        
        # 3) Start game
        Start(Maze)


    @staticmethod
    def Start(Maze):
        """ 
            Give rules to player and start the game

            :param arg1: The maze
            :type arg1: Maze
        """

        print(
            "\nTrès bien {0}, ton objectif est de sortir du labyrinthe.".format(Player.Name) + 
            "\nPour cela il te faudra trouver la sortie et avoir collecté les objets nécessaires à l'ouverture de la porte." + 
            "\nTu es représenté par {0} et la porte de sortie par {1}.".format(Player.Image, MazeElement.GetElement(Maze, "Sortie").Image) + 
            "\nÀ chaque tour tu peux effectuer l'une des actions suivantes :" + 
            "\nTe déplacer vers le (H)aut, le (B)as, la (G)auche, la (D)roite ou (Q)uitter le jeu (et perdre...)" + 
            "\nBonne chance.")

        # Game loop

        # Variable for end of game
        EndOfGame: bool = False
        
        # Do this until end of game is triggered
        while not EndOfGame:
            # Wait for a player action
            PlayerAction: str = Player.WaitForAction()
            # Do action
            EndOfGame = Player.ExecuteAction(PlayerAction)

