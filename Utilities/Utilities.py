# Usefull methods for application

import os
import pygame
import Utilities.GlobalVariables as GV


def LoadImages(ImageNames: str) -> list:
    """
        Load images from resources and returns them

        :param arg1: The name of the image file
        :type arg1: string

        :return: The list of all images
        :rtype: list()
    """

    Images: list = []

    # for each image in ImageNames
    for CurrentImage in ImageNames:
        try:
            MyImage = None
            if not CurrentImage.endswith("*"):
                # Image has a specific file name
                MyImage = GetImage(CurrentImage)
            else:
                # Image is choosen randomly among all files with matching starting names
                MyImageName = CurrentImage[:len(CurrentImage)-1] + "1"
                MyImage = GetImage(MyImageName)
            
            # add image to list
            Images.append(MyImage)

        except OSError:
            # If there is an OSError exception
            print("\nL'image {} n'a pas été trouvée !\n".format(CurrentImage))

    # returns list to item's image list
    return Images


def GetImage(ImageName: str):
    """
        Get an image from the application's library
            if the image exists in the library simply return it
            else load it into library from specified path (generic to work in all OS)

        :param arg1: Image path
        :type arg1: string

        :return: The image
        :rtype: pygame.image
    """

    # Get from library
    MyImage = GV.ImageLibrary.get(ImageName)

    if MyImage == None:
        # if image does not exist in library
        # create generic path for all OS
        ImagePath = GV.GraphicResourcePath + ImageName + GV.ImageExtension
        ImagePath = ImagePath.replace('/', os.sep).replace('\\', os.sep)
        # load image
        MyImage = pygame.image.load(ImagePath)
        # store it in library
        GV.ImageLibrary[ImageName] = MyImage

    # return image
    return MyImage


def WriteText(
    Message: str = "",
    X: int = 0,
    Y: int = 0,
    Width: int = 100,
    Height: int = 50,
    FontName: str = "Arial",
    FontSize: int = 32,
    TextColor = (255, 255, 255),
    UpdateScreen = True):
    """
        Write text with PyGame

        :param arg1: The text
        :type arg1: string
        :param arg2: Text X position in pixels
        :type arg2: int
        :param arg3: Text Y position in pixels
        :type arg3: int
        :param arg4: Text rectangle width in pixels
        :type arg4: int
        :param arg5: Text rectangle height in pixels
        :type arg5: int
        :param arg6: Font name
        :type arg6: string
        :param arg7: Font size in pixels
        :type arg7: int
        :param arg8: Color of text
        :type arg8: tuple (int, int, int) - RGB
        :param arg9: If screen needs to be updated immediately to show text
        :type arg9: bool
    """

    # Create font object
    FontObject = pygame.font.SysFont(FontName, FontSize)
    
    # Render font object
    for LineNumber, LineText in enumerate(Message.split("\n")):
        Text = FontObject.render(LineText, True, TextColor)
        GV.Screen.blit(
            Text, 
            (X, Y + (LineNumber * FontSize)))

    if UpdateScreen:        
        # update screen to show text
        pygame.display.update()
