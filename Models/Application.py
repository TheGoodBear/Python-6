import pygame
from Models.Game import Game

class Application:
    """
        Utility class used to manage the application

        Not instanciable
        Static methods only
    """

    # Possible screen formats (dictionary with tuples as values)
    ScreenFormats = {
        "HD": (1280, 720),
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
        screen = pygame.display.set_mode(cls.ScreenFormats["HD"])
        clock = pygame.time.Clock()
        FPS = 60

        # Initialize game
        Game.Initialize()