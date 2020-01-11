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
                MyImagePath = GV.GraphicResourcePath + CurrentImage + GV.ImageExtension
                MyImage = GetImage(MyImagePath)
            else:
                # Image is choosen randomly among all files with matching starting names
                MyImagePath = GV.GraphicResourcePath + CurrentImage[:len(CurrentImage)-1] + "1" + GV.ImageExtension
                MyImage = GetImage(MyImagePath)
            
            # add image to list
            Images.append(MyImage)

        except OSError:
            # If there is an OSError exception
            print("\nL'image {} n'a pas été trouvée !\n".format(CurrentImage))

    # returns list to item's image list
    return Images


def GetImage(ImagePath: str):
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
    MyImage = GV.ImageLibrary.get(ImagePath)

    if MyImage == None:
        # if image does not exist in library
        # create generic path for all OS
        GenericPath = ImagePath.replace('/', os.sep).replace('\\', os.sep)
        # load image
        MyImage = pygame.image.load(GenericPath)
        # store it in library
        GV.ImageLibrary[ImagePath] = MyImage

    # return image
    return MyImage
