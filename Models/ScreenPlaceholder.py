import os
import json
import pygame
import Utilities.GlobalVariables as GV
import Utilities.Utilities as Util

class ScreenPlaceholder:
    """
        Used to manage the screen elements

        Instanciable
    """

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
        self.WidthPercent: int = PlaceholderData["Width"]
        self.Width: int = GV.ScreenWidth * self.WidthPercent // 100
        self.HeightPercent: int = PlaceholderData["Height"]
        self.Height: int = GV.ScreenHeight * self.HeightPercent // 100
        self.XPercent: int = PlaceholderData["X"]
        self.X: int = GV.ScreenWidth * self.XPercent // 100
        self.YPercent: int = PlaceholderData["Y"]
        self.Y: int = GV.ScreenHeight * self.YPercent // 100
        self.AdjustOnScreen: str = PlaceholderData["AdjustOnScreen"]

        self.Background: str = PlaceholderData["Background"]
        self.BackgroundRepeatX: int = PlaceholderData["BackgroundRepeatX"]
        self.BackgroundRepeatY: int = PlaceholderData["BackgroundRepeatY"]
        self.BackgroundWidth: int = self.Width // self.BackgroundRepeatX
        self.BackgroundHeight: int = self.Height // self.BackgroundRepeatY

        self.Icon: str = PlaceholderData["Icon"]
        self.IconWidthPercent: int = PlaceholderData["IconWidth"]
        self.IconWidth: int = self.Width * self.IconWidthPercent // 100
        self.IconHeightPercent: int = PlaceholderData["IconHeight"]
        self.IconHeight: int = self.Height * self.IconHeightPercent // 100
        self.IconXPercent: int = PlaceholderData["IconX"]
        self.IconX: int = self.X + (self.Width * self.IconXPercent // 100)
        self.IconYPercent: int = PlaceholderData["IconY"]
        self.IconY: int = self.Y + (self.Height * self.IconYPercent // 100)

        self.Legend: str = PlaceholderData["Legend"]
        self.LegendFontName: str = PlaceholderData["LegendFontName"]
        self.LegendFontSize: int = PlaceholderData["LegendFontSize"]
        self.LegendFontBold: string = PlaceholderData["LegendFontBold"]
        self.LegendFontColor: tuple = tuple(int(Number) for Number in str(PlaceholderData["LegendFontColor"]).split(","))
        self.LegendXPercent: int = PlaceholderData["LegendX"]
        self.LegendX: int = self.X + (self.Width * self.LegendXPercent // 100)
        self.LegendYPercent: int = PlaceholderData["LegendY"]
        self.LegendY: int = self.Y + (self.Height * self.LegendYPercent // 100)

        self.TextFontName: str = PlaceholderData["TextFontName"]
        self.TextFontSize: int = PlaceholderData["TextFontSize"]
        self.TextXPercent: int = PlaceholderData["TextX"]
        self.TextX: int = self.Width * self.TextXPercent // 100
        self.TextYPercent: int = PlaceholderData["TextY"]
        self.TextY: int = self.Height * self.TextYPercent // 100

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


    @staticmethod
    def DrawPlaceholdersOnScreen(Maze):
        """ 
            Draw placeholders on screen

            :param arg1: The maze
            :type arg1: Maze
        """

        # Draw each placeholder on screen
        for CurrentPH in GV.Placeholders:
            if(CurrentPH.AdjustOnScreen == "True"):
                # adjust placeholder size and position according to sprite size
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
                    (CurrentPH.BackgroundWidth, CurrentPH.BackgroundHeight))
                # draw it
                for Y in range(0, CurrentPH.BackgroundRepeatY):
                    for X in range(0, CurrentPH.BackgroundRepeatX):
                        GV.Screen.blit(
                            BackgroundImage, 
                            (CurrentPH.X + (CurrentPH.BackgroundWidth * X), 
                            CurrentPH.Y + (CurrentPH.BackgroundHeight * Y)))
            if(CurrentPH.Icon != ""):
                # if placeholder has an icon
                # get image
                IconImage = Util.GetImage(
                    GV.GraphicResourcePath + CurrentPH.Icon + GV.ImageExtension)
                # scale image
                IconImage = pygame.transform.scale(
                    IconImage, 
                    (CurrentPH.IconWidth, CurrentPH.IconHeight))
                # draw it
                GV.Screen.blit(
                    IconImage, 
                    (CurrentPH.IconX, CurrentPH.IconY))
            if(CurrentPH.Legend != ""):
                # if placeholder has a legend
                # get font
                LegendFont = pygame.font.SysFont(
                    CurrentPH.LegendFontName, CurrentPH.LegendFontSize)                
                # render font
                if(CurrentPH.LegendFontBold != ""):
                    LegendFont.set_bold(True)
                LegendText = LegendFont.render(
                    CurrentPH.Legend, True, CurrentPH.LegendFontColor)
                # draw it
                GV.Screen.blit(
                    LegendText, 
                    (CurrentPH.LegendX, CurrentPH.LegendY))
        
        # update screen to show images
        pygame.display.update()
