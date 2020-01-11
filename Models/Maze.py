import os
import random
import pygame
import Utilities.GlobalVariables as GV
from Models.MazeElement import MazeElement

class Maze:
    """
        Used to manage the maze

        Not instanciable
    """

    # Class properties
    # file data
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
    # Image data
    MapSpriteWidth: int = 0
    MapSpriteHeight: int = 0
    ObjectSpriteWidth: int = 0
    ObjectSpriteHeight: int = 0
    CharacterSpriteWidth: int = 0
    CharacterSpriteHeight: int = 0


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

        # Define sprite sizes
        cls.MapSpriteWidth = int(GV.MapPlaceholder.Width / len(cls.MapLayer[0])) 
        cls.MapSpriteHeight = int(GV.MapPlaceholder.Height / len(cls.MapLayer)) 
        cls.ObjectSpriteWidth = int(GV.MapPlaceholder.Width / len(cls.MapLayer[0]) * .6)
        cls.ObjectSpriteHeight = int(GV.MapPlaceholder.Height / len(cls.MapLayer) * .6)
        cls.CharacterSpriteWidth = int(GV.MapPlaceholder.Width / len(cls.MapLayer[0]) * .8)
        cls.CharacterSpriteHeight = int(GV.MapPlaceholder.Height / len(cls.MapLayer) * .8)

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
            Place all objects at random positions in maze
        """

        # Browse every maze element
        for CurrentObject in cls.Elements:
            if("Pick" in CurrentObject.Behaviors):
                # the current object is pickable
                # draw random coordinates in maze limits
                ObjectX: int = random.randint(0, len(cls.MapLayer) - 1)
                ObjectY: int = random.randint(0, len(cls.MapLayer[0]) - 1)
                while("Block" in cls.MapLayer[ObjectY][ObjectX].Behaviors
                    or cls.ObjectLayer[ObjectY][ObjectX] != None):
                    # do it again until random position is ground
                    ObjectX = random.randint(0, len(cls.MapLayer) - 1)
                    ObjectY = random.randint(0, len(cls.MapLayer[0]) - 1)
                # place current object at this position (replace the ground with it)
                cls.ObjectLayer[ObjectY][ObjectX] = CurrentObject


    @classmethod
    def DrawOnScreen(cls):
        """ 
            Draw maze in console
            Including player
        """

        for Y in range(0, len(cls.MapLayer)):
            for X in range(0, len(cls.MapLayer[0])):
                # draw map sprite
                MapImage = cls.MapLayer[Y][X].Images[cls.MapLayer[Y][X].CurrentImageIndex]
                MapImage = pygame.transform.scale(
                    MapImage, 
                    (cls.MapSpriteWidth, cls.MapSpriteHeight))
                GV.Screen.blit(
                    MapImage, 
                    (GV.MapPlaceholder.X + X * cls.MapSpriteWidth, 
                    GV.MapPlaceholder.Y + Y * cls.MapSpriteHeight))
                # draw object sprite
                if(cls.ObjectLayer[Y][X] != None):
                    ObjectImage = cls.ObjectLayer[Y][X].Images[cls.ObjectLayer[Y][X].CurrentImageIndex]
                    ObjectImage = pygame.transform.scale(
                        ObjectImage, 
                        (cls.ObjectSpriteWidth, cls.ObjectSpriteHeight))
                    GV.Screen.blit(
                        ObjectImage, 
                        (GV.MapPlaceholder.X + X * cls.MapSpriteWidth + int((cls.MapSpriteWidth - cls.ObjectSpriteWidth) / 2), 
                        GV.MapPlaceholder.Y + Y * cls.MapSpriteHeight + int((cls.MapSpriteHeight - cls.ObjectSpriteHeight) / 2))) 
                # draw character sprite
                if(cls.CharacterLayer[Y][X] != None):
                    CharacterImage = cls.CharacterLayer[Y][X].Images[cls.CharacterLayer[Y][X].CurrentImageIndex]
                    CharacterImage = pygame.transform.scale(
                        CharacterImage, 
                        (cls.CharacterSpriteWidth, cls.CharacterSpriteHeight))
                    GV.Screen.blit(
                        CharacterImage, 
                        (GV.MapPlaceholder.X + X * cls.MapSpriteWidth + int((cls.MapSpriteWidth - cls.CharacterSpriteWidth) / 2), 
                        GV.MapPlaceholder.Y + Y * cls.MapSpriteHeight + int((cls.MapSpriteHeight - cls.CharacterSpriteHeight) / 2))) 

        # update screen
        pygame.display.update()

        # print("Taille de la carte en pixels : {} x {}".format(GV.MapPlaceholder.Width, GV.MapPlaceholder.Height))
        # print("Taille d'un sprite en pixels : {} x {}".format(cls.MapSpriteWidth, cls.MapSpriteHeight))
        # print("Taille de la carte en cases : {} x {}".format(len(cls.MapLayer[0]), len(cls.MapLayer)))
