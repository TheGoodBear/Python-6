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
        cls.Player = Character.LoadCharactersFromFile(Maze)
        # Ask for player data
        #Player.GetPlayerData()
        # Place player in maze
        cls.Player.PlaceInMaze(Maze)

        # 2) Draw screen
        # Draw game screen
        cls.DrawGameScreen()
        # Draw maze on screen
        Maze.DrawOnScreen()


        # 3) Start game
        cls.Start(Maze)

    @classmethod
    def InitializeScreen(cls):
        """ 
            Initialize screen
        """

        # Load view placeholders from data file (as a dictionary)
        ScreenPlaceholders = ScreenPlaceholder.LoadPlaceholdersFromFile()
        # Instantiate each placeholder and add it to list of ScreenPlaceholder objects
        GV.MapPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Plan"))
        GV.Placeholders.append(GV.MapPlaceholder)
        GV.BackpackPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Sac"))
        GV.Placeholders.append(GV.BackpackPlaceholder)
        GV.DialogPlaceholder = ScreenPlaceholder(
            next(SP for SP in ScreenPlaceholders if SP["Name"] == "Légende"))
        GV.Placeholders.append(GV.DialogPlaceholder)


    @classmethod
    def DrawGameScreen(cls):
        """ 
            Draw game screen
        """

        # Draw each placeholder on screen
        for CurrentPH in GV.Placeholders:
            if(CurrentPH.Name == "Plan"):
                # adjust map placeholder size and position according to map size
                CurrentPH.SpriteWidth = Maze.MapSpriteWidth
                CurrentPH.SpriteHeight = Maze.MapSpriteHeight
                NewWidth = Maze.MapSpriteWidth * len(Maze.MapLayer[0])
                NewHeight = Maze.MapSpriteHeight * len(Maze.MapLayer)
                CurrentPH.X = int((CurrentPH.Width - NewWidth) / 2)
                CurrentPH.Y = int((CurrentPH.Height - NewHeight) / 2)
                CurrentPH.Width = min(CurrentPH.Width, NewWidth)
                CurrentPH.Height = min(CurrentPH.Height, NewHeight)
            if(CurrentPH.Background != ""):
                # if placeholder has a background image
                # get image
                BackgroundImage = Util.GetImage(
                    GV.GraphicResourcePath + CurrentPH.Background + GV.ImageExtension)
                # scale image
                BackgroundImage = pygame.transform.scale(
                    BackgroundImage, 
                    (CurrentPH.Width, CurrentPH.Height))
                # draw it
                GV.Screen.blit(
                    BackgroundImage, 
                    (CurrentPH.X, CurrentPH.Y))
        
        # update screen to show images
        pygame.display.update()


    @classmethod
    def Start(cls, Maze):
        """ 
            Give rules to player and start the game

            :param arg1: The maze
            :type arg1: Maze
        """

        # Draw screen background


        # Show initial message
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

            dt = GV.Clock.tick(GV.FPS) / 1000 

            # PyGame event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # if game exists (user click on red cross in upper right)
                    EndOfGame = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        EndOfGame = True
                    # elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    #     player.velocity[1] = -200 * dt  # 200 pixels per second
                    # elif event.key == pygame.K_x or event.key == pygame.K_DOWN:
                    #     player.velocity[1] = 200 * dt
                    # elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    #     player.velocity[0] = -200 * dt
                    # elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    #     player.velocity[0] = 200 * dt

            # # Wait for a player action
            # PlayerAction: str = Character.WaitForAction(cls.Player)
            # # Do action
            # EndOfGame = cls.Player.ExecuteAction(PlayerAction, Maze)

