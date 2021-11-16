# coding: utf-8

"""
    Class
"""

# imports
import sys
import json
import pygame
import Utilities.GlobalVariables as GV
import Utilities.Utilities as Util
from Models.Maze import Maze

# code
class Character:
    """
        Used to manage the characters

        Instanciable
    """

    # Class properties
    # None

    def __init__(self, CharacterData):
        """
            Constructor

            :param arg1: The character
            :type arg1: Dictionary
        """
        # Instance properties
        self.Name: str = CharacterData["Name"]
        self.ImageNames: list = CharacterData["Images"]
        self.Images: list = Util.LoadImages(self.ImageNames)
        self.CurrentImageIndex: int = 0
        self.Behaviors: list = CharacterData["Behaviors"]
        self.Backpack: list = CharacterData["Backpack"]
        self.BackpackCapacity: int = CharacterData["BackpackCapacity"]
        self.X: int = CharacterData["X"]
        self.Y: int = CharacterData["Y"]
        self.Status: list = CharacterData["Status"]


    @staticmethod
    def LoadCharactersFromFile():
        """
            Load maze characters from json file and store them into list of Maze Characters

            :param arg1: The maze
            :type arg1: Maze

            :return: the player
            :rtype: Character
        """

        # try/exception block to trap errors
        try:
            # Used to store player
            Player = None

            # Open JSON file in read mode (and automatically close it when finished)
            with open(Maze.FilePath + Maze.FileName + " Characters.json", "r", encoding='utf-8') as MyFile:
                # Load them into maze characters list of dictionary
                TempCharacters = json.load(MyFile)
                # Transforms list of dictionary into list of Maze Characters
                for TempCharacter in TempCharacters:
                    CurrentCharacter = Character(TempCharacter)
                    Maze.Characters.append(CurrentCharacter)
                    # if current character is player, save it
                    if (CurrentCharacter.Behaviors[0].lower() == "player"):
                        Player = CurrentCharacter

            # Returns Player
            return Player

        except OSError:
            # If there is an OSError exception
            print("\nLes personnages du labyrinthe demandé n'ont pas été trouvés !\n")
            # exit application
            sys.exit(1)


    # def GetPlayerData(self):
    #     """
    #         Get player data
    #     """

    #     Name: str = ""

    #     print("\nBonjour humain, merci de t'identifier afin que je puisse interagir avec toi.")

    #     # Ask for name until it is filled
    #     while (Name == ""):
    #         Name = input("\nComment dois-je t'appeller : ")

    #     # Update name
    #     self.Name = Name


    # def SayWelcome(self):
    #     """
    #         Say Welcome to player
    #     """

    #     print(
    #         "\nEnchanté {0}, j'espère que tu vas bien t'amuser." 
    #         .format(self.Name))


    def MoveInMaze(
        self,
        CharacterNewX: int = 0,
        CharacterNewY: int = 0):
        """
            Move character in maze (or place him if not already done)

            :param arg1: The maze
            :type arg1: Maze
            :param arg2: The new X position of character
            :type arg2: integer
            :param arg3: The new Y position of character
            :type arg3: integer
        """

        # Local variables for maze coordinates
        X: int = 0
        Y: int = 0

        # Check if character is not already in the maze (coordinates set to 0)
        if (self.X == 0 and self.Y == 0):
            # in that case put him at the entrance
            # find it by browsing maze list
            for Y, Line in enumerate(Maze.MapLayer):
                # new line, set X coordinate to 0
                X = 0
                for X, CurrentElement in enumerate(Line):
                    # if position contains entrance (E)
                    if (CurrentElement.Name == "Entrée"):
                        # push character from entrance
                        if (X >= 0 and Maze.MapLayer[Y][X-1].Name == "Sol"):
                            self.X -= 1
                            self.Y = Y
                        elif (X <= len(Maze.MapLayer[0]) and Maze.MapLayer[Y][X+1].Name == "Sol"):
                            self.X += 1
                            self.Y = Y
                        elif (Y >= 0 and Maze.MapLayer[Y-1][X].Name == "Sol"):
                            self.X = X
                            self.Y -= 1
                        elif (Y <= len(Maze.MapLayer) and Maze.MapLayer[Y+1][X].Name == "Sol"):
                            self.X = X
                            self.Y += 1
                        # put him in the maze
                        Maze.CharacterLayer[self.Y][self.X] = self
                        # exit loops (and method)
                        return
                    # increment X coordinate
                    X += 1
                # increment Y coordinate
                Y += 1

        else:
            # Character is already in maze
            # play sound
            Util.ManageSound("Move")

            # replace actual character position with nothing
            Maze.CharacterLayer[self.Y][self.X] = None
            # redraw maze at old character position
            Maze.DrawElementsAtPosition(self.X, self.Y)

            # assign new coordinates to character
            self.X = CharacterNewX
            self.Y = CharacterNewY
            # place character to new position
            Maze.CharacterLayer[self.Y][self.X] = self
            # redraw maze at new character position
            Maze.DrawElementsAtPosition(self.X, self.Y)


    @staticmethod
    def GetAction() -> str:
        """
            Wait player to make an action

            :param arg1: The character
            :type arg1: Character

            :return: The name of the action if it is valid
            :rtype: string
        """

        Action: str = ""

        # PyGame event loop
        for Event in pygame.event.get():
            # get player input
            if (Event.type == pygame.QUIT):
                # if game exits (user click on red cross in upper right)
                Action = "QuitGame"
            elif (Event.type == pygame.KEYDOWN):
                if (Event.key == pygame.K_ESCAPE):
                    Action = "QuitGame"
                elif (Event.key == pygame.K_w or Event.key == pygame.K_UP):
                    Action = "MoveUp"
                elif (Event.key == pygame.K_s or Event.key == pygame.K_DOWN):
                    Action = "MoveDown"
                elif (Event.key == pygame.K_a or Event.key == pygame.K_LEFT):
                    Action = "MoveLeft"
                elif (Event.key == pygame.K_d or Event.key == pygame.K_RIGHT):
                    Action = "MoveRight"

        # No action done
        return Action


    def ExecuteAction(self,
        Action: str) -> bool:
        """
            Execute character action and returns new position

            :param arg1: The action
            :type arg1: string
            :param arg2: The maze
            :type arg2: Maze

            :return: If this is the end of the game
            :rtype: boolean
        """

        # Message to be written
        Message: str = ""

        # Local variables for character new coordinates
        CharacterNewX: int = self.X
        CharacterNewY: int = self.Y

        # Calculate character new coordinates
        if (Action == "MoveUp"):
            Message = "Tu te déplaces vers le haut..."
            CharacterNewY -= 1
        elif (Action == "MoveDown"):
            Message = "Tu te déplaces vers le bas..."
            CharacterNewY += 1
        elif (Action == "MoveLeft"):
            Message = "Tu te déplaces vers la gauche..."
            CharacterNewX -= 1
        elif (Action == "MoveRight"):
            Message = "Tu te déplaces vers la droite..."
            CharacterNewX += 1
        elif (Action == "QuitGame"):
            # if action is QuitGame then return game end
            Util.Write("Tu choisis de quitter le labyrinthe,\ntu as perdu !\n\nAppuie sur Echap pour quitter l'application.")
            return True


        # Check if new coordinates are valid (into maze limits)
        if (CharacterNewX < 0 or
            CharacterNewX > len(Maze.MapLayer[0]) or
            CharacterNewY < 0 or
            CharacterNewY > len(Maze.MapLayer)):
            # if character is out of maze limits
            Message += "\n\nTu es en dehors des limites, tu ne peux pas aller par là !"
            # play sound
            Util.ManageSound("Collision")
            return False

        # Get current maze elements at coordinates
        CurrentMapElement = Maze.MapLayer[CharacterNewY][CharacterNewX]
        CurrentObject = Maze.ObjectLayer[CharacterNewY][CharacterNewX]
        #CurrentCharacter = Maze.CharacterLayer[CharacterNewY][CharacterNewX]

        # Check current map/object/character behavior or name
        if (CurrentMapElement.Name.lower() == "sortie"):
            # if exit is reached
            # check door status
            if (CurrentMapElement.Behaviors[CurrentMapElement.CurrentBehaviorIndex] == "close"):
                # door is closed
                # check if player has all needed objects
                MissingObjects: int = 0
                # for each element in maze
                for Element in Maze.Elements:
                    if ("combine" in Element.Behaviors
                        and not Element in self.Backpack):
                        # this element can be combined but is not in player backpack
                        MissingObjects += 1
                if (MissingObjects == 0):
                    # player has all objects
                    # change exit image and behavior
                    CurrentMapElement.CurrentImageIndex = 1
                    CurrentMapElement.CurrentBehaviorIndex = 1
                    # redraw maze at new character position but without moving him
                    Maze.DrawElementsAtPosition(CharacterNewX, CharacterNewY)
                    # say door opens
                    Message += "\n\nOuiiii, tu as trouvé la sortie\net tu as tous les objets nécessaires.\n\nLa porte s'ouvre !"
                    # play sound
                    Util.ManageSound("DoorOpen")

                else:
                    # some objects are missing
                    # say how many
                    Message += "\n\nHa, tu as bien trouvé la sortie\nmais il te manque encore\n{0} objet(s) pour ouvrir la porte...".format(MissingObjects)
                    # play sound
                    Util.ManageSound("LevelIncomplete")
            else:
                # door is opened
                # move character in maze
                self.MoveInMaze(CharacterNewX, CharacterNewY)
                # say victory
                Message += "\n\nBravo {0},\n\ntu es sorti victorieux du labyrinthe :-)\n\nAppuie sur Echap pour quitter l'application.".format(self.Name)
                Util.Write(Message)
                # play sound
                Util.ManageSound("LevelComplete")
               # and return game end
                return True

        elif ("block" in CurrentMapElement.Behaviors):
            # if there is an obstacle, say it
            Message += "\n\nOups un mur,\ntu ne peux pas bouger !"
            # play sound
            Util.ManageSound("Collision")

        elif (CurrentObject is not None and "pick" in CurrentObject.Behaviors):
            # if there is an object
            # move character in maze
            self.MoveInMaze(CharacterNewX, CharacterNewY)
            # open chest and get object image in place
            CurrentObject.CurrentImageIndex = 1
            if (len(self.Backpack) < self.BackpackCapacity):
                # if backpack is not full
                # say it
                Message += "\n\nChouette !\n\nTu as trouvé un(e) {0}.".format(CurrentObject.Name)
                # remove it from maze
                Maze.ObjectLayer[CharacterNewY][CharacterNewX] = None
                # put it in backpack
                self.Backpack.append(CurrentObject)
                # play sound
                if ("combine" in CurrentObject.Behaviors):
                    Util.ManageSound("PickupTreasure")
                else:
                    Util.ManageSound("PickupCasual")
                # redraw backpack
                self.DrawBackpack()
            else:
                # if backpack is full
                # say it
                Message += "\n\nTu as trouvé un(e) {0}\nmais ton sac est déjà plein...".format(CurrentObject.Name)
                # play sound
                Util.ManageSound("BackpackFull")

        else:
            # if nothing special
            # move character in maze
            self.MoveInMaze(CharacterNewX, CharacterNewY)

        # Write message
        Util.Write(Message)

        # Game is not yet ended
        return False


    def DrawBackpack(self):
        """
            Draw backpack items
        """

        # for each item in backpack
        for ElementIndex, Element in enumerate(self.Backpack):
            # get image
            ElementImage = Element.Images[Element.CurrentImageIndex]
            # special cases to manage backpack icon
            VisualElementIndex = ElementIndex
            if (ElementIndex < 2):
                VisualElementIndex += 2
            else:
                VisualElementIndex += 4
            # scale image
            ElementImage = pygame.transform.scale(
                ElementImage,
                (int(GV.BackpackPlaceholder.BackgroundWidth * GV.ObjectSpriteScaleInBackpack),
                 int(GV.BackpackPlaceholder.BackgroundHeight * GV.ObjectSpriteScaleInBackpack)))
            # get image position
            Y = VisualElementIndex // GV.BackpackPlaceholder.BackgroundRepeatX
            X = VisualElementIndex % GV.BackpackPlaceholder.BackgroundRepeatX
            # draw image
            GV.Screen.blit(
                ElementImage,
                (GV.BackpackPlaceholder.X + (GV.BackpackPlaceholder.BackgroundWidth * X)
                 + int(GV.BackpackPlaceholder.BackgroundWidth * (1 - GV.ObjectSpriteScaleInBackpack) // 2),
                 GV.BackpackPlaceholder.Y + (GV.BackpackPlaceholder.BackgroundHeight * Y)
                 + int(GV.BackpackPlaceholder.BackgroundHeight * (1 - GV.ObjectSpriteScaleInBackpack) // 2)))

        # update screen to show images
        pygame.display.update()
