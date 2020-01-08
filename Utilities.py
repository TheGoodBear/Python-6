# Usefull methods for application

import pygame
import GlobalVariables

def LoadImages(ImageNames: str) -> list():
    """
        Load images from resources and returns them

        :param arg1: The name of the image file
        :type arg1: string

        :return: The list of all images
        :rtype: list()
    """
    # MyImagePath = GlobalVariables.GraphicResourcePath + "Backpack" + GlobalVariables.ImageExtension
    # MyImage = pygame.image.load(MyImagePath)
    # GlobalVariables.Screen.blit(MyImage, (20, 20))
    # pygame.display.update()

    Images = list()

    # for each image in ImageNames
    for CurrentImage in ImageNames:
        try:
            MyImagePath = GlobalVariables.GraphicResourcePath + CurrentImage + GlobalVariables.ImageExtension
            MyImage = None
            if not CurrentImage.endswith("*"):
                # Image has a specific file name
                MyImage = pygame.image.load(MyImagePath)
                GlobalVariables.Screen.blit(MyImage, (20, 20))
                pygame.display.update()
            else:
                # Image is choosen randomly among all files with matching starting names
                MyImage = pygame.image.load(GlobalVariables.GraphicResourcePath + "Scroll" + GlobalVariables.ImageExtension)
                GlobalVariables.Screen.blit(MyImage, (20, 20))
                pygame.display.update()
            
            # add image to list
            Images.append(MyImage)

        except OSError:
            # If there is an OSError exception
            print("\nL'image {} n'a pas été trouvée !\n".format(CurrentImage))

    # returns list to item's image list
    return Images
