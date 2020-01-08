import pygame
import GlobalVariables
from Models.Game import Game

class Application:
    """
        Utility class used to manage the application

        Not instanciable
        Static methods only
    """

    # Possible screen formats (dictionary with tuples as values)
    ScreenFormats = {
        "nHD": (640, 360),
        "qHD": (960, 540),
        "HD": (1280, 720),
        "HD+": (1600, 900),
        "FullHD": (1920, 1080)}

    @classmethod
    def Start(cls):
        """ 
            Start application and initialize PyGame
        """

        # Initialize PyGame
        Successes, Failures = pygame.init()
        if(Failures > 0):
            print(
                "\n\nPyGame n'a pas pu être initialisé." +
                "\n\nMerci d'aller sur https://www.pygame.org/wiki/GettingStarted et de procéder à son installation.\n\n")
            pygame.quit()

        # PyGame was successfully initialized
        # Set screen
        GlobalVariables.Screen = pygame.display.set_mode(cls.ScreenFormats["qHD"])
        GlobalVariables.Screen.fill((255, 255, 255))
        GlobalVariables.Clock = pygame.time.Clock()

        MyImagePath = GlobalVariables.GraphicResourcePath + "Backpack" + GlobalVariables.ImageExtension
        MyImage = pygame.image.load(MyImagePath)
        GlobalVariables.Screen.blit(MyImage, (20, 20))
        pygame.display.update()

        # Initialize game
        Game.Initialize()
