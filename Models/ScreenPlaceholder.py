import os
import json
import pygame
import Utilities.GlobalVariables as GV

class ScreenPlaceholder:
    """
        Used to manage the screen elements

        Instanciable
    """

    # Class properties
    FilePath: str 
    FileName: str 

    def __init__(self, PlaceholderData: dict):
        """
            Constructor
        """

        GV.ScreenWidth = GV.ScreenFormats[
            GV.DefaultScreenFormat][0]
        GV.ScreenHeight = GV.ScreenFormats[
            GV.DefaultScreenFormat][1]

        # Instance properties
        self.Name: str = PlaceholderData["Name"]
        self.Icon: str = PlaceholderData["Icon"]
        self.Background: str = PlaceholderData["Background"]
        self.WidthPercent: int = PlaceholderData["Width"]
        self.Width: int = int(GV.ScreenWidth * self.WidthPercent / 100)
        self.HeightPercent: int = PlaceholderData["Height"]
        self.Height: int = int(GV.ScreenHeight * self.HeightPercent / 100)
        self.XPercent: int = PlaceholderData["X"]
        self.X: int = int(GV.ScreenWidth * self.XPercent / 100)
        self.YPercent: int = PlaceholderData["Y"]
        self.Y: int = int(GV.ScreenHeight * self.YPercent / 100)
        self.SpriteWidth: int = 0
        self.SpriteHeight: int = 0


    @staticmethod
    def LoadPlaceholdersFromFile():
        """ 
            Load view placeholders from json file

            :param arg1: The placeholder
            :type arg1: Dictionary
        """

        # try/exception block to trap errors
        try:

            # Open JSON file in read mode (and automatically close it when finished)
            with open("Utilities/ScreenData.json", "r", encoding='utf-8') as MyFile:
                # Load data into list of dictionary
                Placeholders = json.load(MyFile)
            
            # Returns list
            return Placeholders

        except OSError:
            # If there is an OSError exception
            print("\nLes éléments de l'écran de jeu n'ont pas été trouvés !\n")
            # exit application
            os._exit(1)
