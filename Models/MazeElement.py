import os
import json
import Utilities.Utilities as Util

class MazeElement:
    """
        Used to manage elements compozing the maze

        Instanciable
    """

    # Class properties
    Width: int = 0
    Height: int = 0

    def __init__(self, ElementData):
        """
            Constructor

            :param arg1: The element
            :type arg1: Dictionary
        """
        # Instance properties
        self.Name: str = ElementData["Name"]
        self.Symbol: str = ElementData["Symbol"]
        self.ImageNames: list = ElementData["Images"]
        self.Images: list = Util.LoadImages(self.ImageNames)
        self.CurrentImageIndex: int = 0
        self.Behaviors: list = ElementData["Behaviors"]


    @staticmethod
    def LoadElementsFromFile(Maze):
        """ 
            Load maze elements from json file and store them into list of Maze Elements

            :param arg1: The maze
            :type arg1: Maze
        """

        # try/exception block to trap errors
        try:
            # Open JSON file in read mode (and automatically close it when finished)
            with open(Maze.FilePath + Maze.FileName + " Elements.json", "r", encoding='utf-8') as MyFile:
                # Load them into maze elements list of dictionary
                TempElements = json.load(MyFile)
                # Transforms list of dictionary into list of Maze Elements
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
