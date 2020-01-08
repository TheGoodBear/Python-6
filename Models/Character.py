from Models.Maze import *
from Models.MazeElement import *

class Character:
    """
        Used to manage the characters

        Instanciable
    """

    # Class properties
    # None

    def __init__(self, CurrentCharacter):
        """
            Constructor

            :param arg1: The character
            :type arg1: Character
        """
        # Instance properties
        self.Name: str = CurrentCharacter["Name"]
        self.ImageNames: list(str) = CurrentCharacter["Images"]
        self.Images: list() = self.LoadImages(self.ImageNames)
        self.CurrentImageIndex = 0
        self.Behaviors: list() = CurrentCharacter["Behaviors"]
        self.Backpack: list() = CurrentCharacter["Backpack"]
        self.X: int = 0
        self.Y: int = 0


    def GetPlayerData(self):
        """ 
            Get player data
        """

        Name: str = ""

        # Ask for name until it is filled
        while(Name == ""):
            Name = input("\nMerci d'entrer ton nom : ")

        # Update name
        self.Name = Name


    def SayWelcome(self):
        """ 
            Say Welcome to player
        """

        print(
            "\nEnchanté {0}, j'espère que tu vas bien t'amuser." 
            .format(self.Name))


    def PlaceInMaze(self,
        Maze,
        CharacterNewX: int = 0,
        CharacterNewY: int = 0):
        """ 
            Place character in maze

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
            # In that case put him at the entrance
            # find it by browsing maze list
            for Line in Maze.Map:
                # New line, set X coordinate to 0
                X = 0
                for Character in Line:
                    # If position contains entrance (E)
                    if (Maze.Map[Y][X].Name == "Entrée"):
                        # Save coordinates for character
                        self.X = X
                        self.Y = Y
                        # put him in the maze
                        Maze.CharacterLayer[Y][X] = self
                        # Exit loops (and method)
                        return
                    # Increment X coordinate
                    X += 1
                # Increment Y coordinate
                Y += 1

        else:
            # Character is already in maze
            # replace actual character position with nothing
            Maze.CharacterLayer[self.Y][self.X] = None
            # and place character to new position
            Maze.CharacterLayer[CharacterNewY][CharacterNewX] = self


    @staticmethod
    def WaitForAction(Character) -> str:
        """ 
            Wait player to make an action

            :param arg1: The character
            :type arg1: Character

            :return: The name of the action if it is valid
            :rtype: string
        """

        # Show player backpack content
        print("\nContenu du sac à dos : ", end="")
        if (len(Character.Backpack) == 0):
            # if backpack is empty (nothing in list)
            print("vide")
        else:
            # if backpack contains at least 1 object (* means every item in list)
            print(*Character.Backpack, sep=', ')

        # Ask player input until it is a valid action
        while True:
            PlayerInput = input("\nQuelle est ta prochaine action ? ")

            # check if this is a valid action
            # show a message saying what player is doing
            # and return action name if valid
            if (PlayerInput.upper() == "H"):
                print("Tu te déplaces vers le haut...")
                return "MoveUp"
            elif (PlayerInput.upper() == "B"):
                print("Tu te déplaces vers le bas...")
                return "MoveDown"
            elif (PlayerInput.upper() == "G"):
                print("Tu te déplaces vers la gauche...")
                return "MoveLeft"
            elif (PlayerInput.upper() == "D"):
                print("Tu te déplaces vers la droite...")
                return "MoveRight"
            elif (PlayerInput.upper() == "Q"):
                print("Tu choisis de quitter le labyrinthe, tu as perdu !\n")
                return "QuitGame"
            else:
                print("Cette action n'est pas reconnue.")


    def ExecuteAction(self,     
        Action: str,
        Maze) -> bool:
        """ 
            Execute character action and returns new position

            :param arg1: The action
            :type arg1: string
            :param arg2: The maze
            :type arg2: Maze

            :return: If this is the end of the game
            :rtype: boolean
        """

        # Local variables for character new coordinates
        CharacterNewX: int = self.X
        CharacterNewY: int = self.Y

        # Calculate character new coordinates
        if (Action == "MoveUp"):
            CharacterNewY -= 1
        elif (Action == "MoveDown"):
            CharacterNewY += 1
        elif (Action == "MoveLeft"):
            CharacterNewX -= 1
        elif (Action == "MoveRight"):
            CharacterNewX += 1
        elif (Action == "QuitGame"):
            # if action is QuitGame then return game end
            return True


        # Check if new coordinates are valid (into maze limits)
        if (CharacterNewX<0 or 
            CharacterNewX>len(Maze.Map[0]) or 
            CharacterNewY<0 or 
            CharacterNewY>len(Maze.Map)):
            # if character is out of maze limits
            print("Tu es en dehors des limites, tu ne peux pas aller par là !")
            # redraw maze
            Maze.DrawOnScreen()
            return False

        # Get current maze elements at coordinates
        CurrentMapElement = Maze.MapLayer[CharacterNewY][CharacterNewX]
        CurrentObject = Maze.ObjectLayer[CharacterNewY][CharacterNewX]
        CurrentCharacter = Maze.CharacterLayer[CharacterNewY][CharacterNewX]

        # Check current map/object/character behavior or name
        if (CurrentMapElement.Name == "Sortie"):
            # if exit is reached
            # check if player has all needed objects
            MissingObjects: int = 0
            # for each element in maze
            for Element in Maze.Elements:
                if ("Combine" in Element.Behavior
                    and not Element.Name in self.Backpack):
                    # this element can be combined but is not in player backpack
                    MissingObjects += 1
            if (MissingObjects == 0):
                # character has all objects
                # replace character in maze
                self.PlaceInMaze(Maze,CharacterNewX,CharacterNewY)
                # assign new coordinates to character
                self.X = CharacterNewX
                self.Y = CharacterNewY
                # redraw maze with new character position
                Maze.DrawOnScreen()
                # say victory
                print(
                    "\nOuiiii, bravo {0}, tu as trouvé la sortie et tu avais tous les objets nécessaires !\n"
                    .format(self.Name))
                # and return game end
                return True
            else:
                # some objects are missing
                # say how many
                print(
                    "\nHa, tu as bien trouvé la sortie mais il te manque encore {0} objet(s) pour ouvrir la porte..."
                    .format(MissingObjects))
        
        elif ("Block" in CurrentMapElement.Behavior):
            # if there is an obstacle, say it
            print("Oups un mur, tu ne peux pas bouger !")
            # and redraw maze
            Maze.DrawOnScreen()
        
        elif ("Pick" in CurrentObject.Behavior):
            # if there is an object, put it in backpack
            self.Backpack.append(CurrentObject)
            # say it
            print(
                "Chouette, tu as trouvé un(e) {0}\n"
                .format(CurrentObject.Name))
            # remove it from maze 
            Maze.ObjectLayer[CharacterNewY][CharacterNewX] = None
            # replace character in maze
            self.PlaceInMaze(Maze,CharacterNewX,CharacterNewY)
            # assign new coordinates to character
            self.X = CharacterNewX
            self.Y = CharacterNewY
            # and redraw maze with new character position
            Maze.DrawOnScreen()
            
        else:
            # if nothing special
            # replace character in maze
            self.PlaceInMaze(Maze,CharacterNewX,CharacterNewY)
            # assign new coordinates to character
            self.X = CharacterNewX
            self.Y = CharacterNewY
            # and redraw maze with new character position
            Maze.DrawOnScreen()

        # Game is not yet ended    
        return False
