import pygame
import Utilities.GlobalVariables as GV
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
        # pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        GV.Screen = pygame.display.set_mode(
            GV.ScreenFormats[GV.DefaultScreenFormat])
        GV.Screen.fill(GV.ColorBlack)
        GV.Clock = pygame.time.Clock()

        infoObject = pygame.display.Info()
        # pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        print(infoObject.current_w, infoObject.current_h)

        # Initialize game
        Game.Initialize()
