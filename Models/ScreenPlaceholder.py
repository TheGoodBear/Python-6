import json
import pygame
import GlobalVariables

class ScreenPlaceholder:
    """
        Used to manage the screen elements

        Instanciable
    """

    # Class properties
    FilePath: str 
    FileName: str 

    def __init__(self, PlaceholderData):
        """
            Constructor
        """

        ScreenWidth = GlobalVariables.ScreenFormats[
            GlobalVariables.DefaultScreenFormat][0]
        ScreenHeight = GlobalVariables.ScreenFormats[
            GlobalVariables.DefaultScreenFormat][1]

        # Instance properties
        self.Name: str = PlaceholderData["Name"]
        self.Icon: str = PlaceholderData["Icon"]
        self.Background: str = PlaceholderData["Background"]
        self.WidthPercent: int = PlaceholderData["Width"]
        self.Width: int = int(ScreenWidth * self.WidthPercent / 100)
        self.HeightPercent: int = PlaceholderData["Height"]
        self.Height: int = int(ScreenHeight * self.HeightPercent / 100)
        self.XPercent: int = PlaceholderData["X"]
        self.X: int = int(ScreenWidth * self.XPercent / 100)
        self.YPercent: int = PlaceholderData["Y"]
        self.Y: int = int(ScreenHeight * self.YPercent / 100)


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
            with open("Data/ScreenData.json", "r", encoding='utf-8') as MyFile:
                # Load data into list of dictionary
                Placeholders = json.load(MyFile)
            
            # Returns list
            return Placeholders

        except OSError:
            # If there is an OSError exception
            print("\nLes éléments de l'écran de jeu n'ont pas été trouvés !\n")
            # exit application
            os._exit(1)
