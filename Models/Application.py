import pygame
import GlobalVariables
from Models.Game import Game

class Application:
    """
        Utility class used to manage the application

        Not instanciable
        Class and Static methods only
    """

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
        GlobalVariables.Screen = pygame.display.set_mode(
            GlobalVariables.ScreenFormats[GlobalVariables.DefaultScreenFormat])
        GlobalVariables.Screen.fill(GlobalVariables.ColorBlack)
        GlobalVariables.Clock = pygame.time.Clock()

        # Initialize game
        Game.Initialize()
