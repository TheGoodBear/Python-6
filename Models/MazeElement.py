import os
import json
import pygame
import GlobalVariables

class MazeElement:
    """
        Used to manage elements compozing the maze

        Instanciable
    """

    # Class properties
    Width: int = 0
    Height: int = 0

    def __init__(self, Element):
        """
            Constructor

            :param arg1: The element
            :type arg1: Element
        """
        # Instance properties
        self.Name: str = Element["Name"]
        self.Symbol: str = Element["Symbol"]
        self.ImageNames: list(str) = Element["Images"]
        self.Images: list() = self.LoadImages(self.ImageNames)
        self.CurrentImageIndex = 0
        self.Behavior: list() = Element["Behavior"]


    @staticmethod
    def LoadElementsFromFile(Maze):
        """ 
            Load maze elements from json file and store them into list of MazeElements

            :param arg1: The maze
            :type arg1: Maze
        """

        # try/exception block to trap errors
        try:
            # Open JSON file in read mode (and automatically close it when finished)
            with open(Maze.FilePath + Maze.FileName + " Elements.json", "r", encoding='utf-8') as MyFile:
                # Load them into maze elements list of dictionary
                TempElements = json.load(MyFile)
                # Transforms list of dictionary into list of MazeElements
                for TempElement in TempElements:
                    Maze.Elements.append(MazeElement(TempElement))

            # # Code sample to write to JSON file
            # # Open JSON file in write mode (and automatically close it when finished)
            # with open("MazeElements.json", "w", encoding="utf-8") as WriteFile:
            #     # Write to file using proper ascii encoding (with accents) and indentation
            #     json.dump(MazeElements, WriteFile, ensure_ascii=False, indent=4)

        except OSError:
            # If there is an OSError exception
            print("\nLes éléments du labyrinthe demandé n'ont pas été trouvés !\n")
            # exit application
            os._exit(1)


    @staticmethod
    def LoadImages(ImageNames: str) -> list():
        """
            Load images from resources and returns them

            :param arg1: The name of the image file
            :type arg1: string

            :return: The list of all images
            :rtype: list()
        """
        # for each image in ImageNames
        for CurrentImage in ImageNames:
            try:
                if not CurrentImage.endswith("*"):
                    # Image has a specific file name
                    image = pygame.image.load(GlobalVariables.GraphicResourcePath + CurrentImage + GlobalVariables.ImageExtension)
                    GlobalVariables.Screen.blit(image, (20, 20))
                    pygame.display.update()
                else:
                    # Image is choosen randomly among all files with matching starting names
                    

            except OSError:
                # If there is an OSError exception
                print("\nL'image {} n'a pas été trouvée !\n".format(CurrentImage))

    
    @staticmethod
    def GetElement(
        Maze,
        Name: str = "",
        Symbol: str = "",
        Image: str = ""):
        """ 
            Return a maze element by its name, symbol or image or None if none matches

            :param arg1: The maze
            :type arg1: Maze
            :param arg2: The element name
            :type arg2: string
            :param arg3: The element symbol
            :type arg3: string
            :param arg4: The element image
            :type arg4: string
        """

        # # Alternative syntax with list comprehension
        # return next((ME for ME in MazeElements if ME["Symbol"] == Symbol), None)

        # Browse all elements to find the matching one
        for CurrentElement in Maze.Elements:
            if(Name != "" and CurrentElement.Name == Name):
                return CurrentElement
            elif(Symbol != "" and CurrentElement.Symbol == Symbol):
                return CurrentElement
            elif(Image != "" and CurrentElement.Image == Image):
                return CurrentElement

        # If no element matches, return none (null/nothing)
        return None
