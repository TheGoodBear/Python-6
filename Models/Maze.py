import os
import random
from Models.MazeElement import MazeElement

class Maze:
    """
        Used to manage the maze

        Not instanciable
    """

    # Class properties
    FilePath: str 
    FileName: str 
    # stores the maze structure in 3 layers (2 dimensional lists)
    # MapLayer for fixed elements (walls, stairs, doors, ...)
    MapLayer: list = []
    # ObjectLayer for items (pickable objects)
    ObjectLayer: list = []
    # CharacterLayer for characters (player, ennemies, ...)
    CharacterLayer: list = []    # Elements composing the maze
    Elements: list = []
    # Characters acting in the maze
    Characters: list = []


    @classmethod
    def Initialize(cls, 
        FilePath: str = "Mazes/", 
        FileName: str = "Maze 1"):
        """
            Initialize the maze
    
            :param arg1: Maze file path
            :type arg1: string
            :param arg2: Maze file name
            :type arg2: string

            :return: the player
            :rtype: Character
        """
        cls.FilePath = FilePath
        cls.FileName = FileName

        # Load maze elements from json file
        MazeElement.LoadElementsFromFile(Maze)
        # Load maze from text file
        Maze.LoadMapFromFile()

        # Put objects at random positions
        Maze.PlaceObjectsAtRandomPositions()


    @classmethod
    def LoadMapFromFile(cls):
        """ 
            Load maze map from text file and store it into a 2 dimensional list
        """

        # try/exception block to trap errors
        try:
            # Open file in read mode (and automatically close it when finished)
            with open(cls.FilePath + cls.FileName + ".maz", "r") as MyFile:
                for Line in MyFile:
                    # Ignore blank lines and comments
                    if(Line[0] == "\n" or Line[0] == "#"):
                        continue
                    # Define temporary list to store every character in line
                    LineData = list()
                    OtherLayerData = list()
                    # For each character in Line
                    for Char in Line:
                        # Store character in LineData list (except new line \n)
                        if (Char != "\n"):
                            # Search in maze elements for matching symbol
                            CurrentElement = MazeElement.GetElement(cls, Symbol=Char)
                            if(CurrentElement != None):
                                # If an element was found
                                    # append element
                                    LineData.append(CurrentElement)
                                    OtherLayerData.append(None)
                    # Store LineData list in MapLayer list
                    cls.MapLayer.append(LineData)
                    # Store blank data list in Object and Character Layers lists
                    cls.ObjectLayer.append(OtherLayerData)
                    cls.CharacterLayer.append(OtherLayerData)

        except OSError:
            # If there is an OSError exception
            print("\nLe labyrinthe demandé n'a pas été trouvé !\n")
            # exit application
            os._exit(1)


    @classmethod
    def PlaceObjectsAtRandomPositions(cls):
        """ 
            Place all objects from dictionary at random positions in maze
        """

        # Browse every maze element
        for CurrentObject in cls.Elements:
            if("Pick" in CurrentObject.Behaviors):
                # the current object is pickable
                # draw random coordinates in maze limits
                ObjectX: int = random.randint(0, len(cls.MapLayer)-1)
                ObjectY: int = random.randint(0, len(cls.MapLayer[0])-1)
                while(cls.MapLayer[ObjectY][ObjectX].Name != "Sol"):
                    # do it again until random position is ground
                    ObjectX = random.randint(0, len(cls.MapLayer)-1)
                    ObjectY = random.randint(0, len(cls.MapLayer[0])-1)
                # place current object at this position (replace the ground with it)
                cls.ObjectLayer[ObjectY][ObjectX] = CurrentObject


    @classmethod
    def DrawOnScreen(cls):
        """ 
            Draw maze in console
            Including player
        """

        # Prints a blank line
        print()

        # With simple loop (gives only the content)
        # For each line (Y) in Maze
        for Line in cls.MapLayer:
            # For each character (X) in line
            for Column in Line:
                # Print current maze element at Y, X without jumping a line
                print(Column, end="")
            # Jump a line for new Y
            print()
