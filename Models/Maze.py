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
    # stores the maze structure (2 dimensional list)
    Map = list()
    # stores the elements composing the maze
    Elements = list()


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
                    # Define temporary list to store every character in a line
                    LineCharacters = list()
                    # For each Character in Line
                    for Character in Line:
                        # Store Character in LineCharacters list (except new line \n)
                        if (Character != "\n"):
                            # Search in maze elements for matching symbol
                            CurrentElement = MazeElement.GetElement(cls, Symbol=Character)
                            if(CurrentElement != None):
                                # If an element was found, append element's image
                                LineCharacters.append(CurrentElement.Image)
                            else:
                                # If no element was found append character
                                LineCharacters.append(Character)
                    # Store LineCharacters list in Map list (2 dimensional list)
                    cls.Map.append(LineCharacters)

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
            if("Pick" in CurrentObject.Behavior):
                # the current object is pickable
                # draw random coordinates in maze limits
                ObjectX: int = random.randint(0, len(cls.Map)-1)
                ObjectY: int = random.randint(0, len(cls.Map[0])-1)
                while(cls.Map[ObjectY][ObjectX] != MazeElement.GetElement(cls, "Sol").Image):
                    # do it again until random position is ground
                    ObjectX = random.randint(0, len(cls.Map)-1)
                    ObjectY = random.randint(0, len(cls.Map[0])-1)
                # place current object at this position (replace the ground with it)
                cls.Map[ObjectY][ObjectX] = CurrentObject.Image


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
        for Line in cls.Map:
            # For each character (X) in line
            for Column in Line:
                # Print current maze element at Y, X without jumping a line
                print(Column, end="")
            # Jump a line for new Y
            print()
