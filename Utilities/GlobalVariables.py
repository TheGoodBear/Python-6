# Global variables for application

# Screen
Screen = None
# possible screen formats (dictionary with tuples as values)
ScreenFormats: dict = {
    "Current": (0, 0),
    "nHD": (640, 360),
    "qHD": (960, 540),
    "HD": (1280, 720),
    "HD+": (1600, 900),
    "FullHD": (1920, 1080)}
DefaultScreenFormat: str = "HD"
ScreenWidth: int = 0
ScreenHeight: int = 0
# some colors
ColorWhite: tuple = (255, 255, 255)
ColorBlack: tuple = (0, 0, 0)
# view placeholders
Placeholders: list = []
MapPlaceholder = None
BackpackPlaceholder = None
DialogPlaceholder = None
MapSpriteScaleInMaze = 1.00
CharacterSpriteScaleInMaze = 0.80
ObjectSpriteScaleInMaze = 0.60
ObjectSpriteScaleInBackpack = 0.70

# Game data
Clock = None
FPS: int = 60

# Resources
# media library for entire application
ImageLibrary: dict = {}
SoundLibrary: dict = {}
# generic image parameters
ImageExtension: str = ".png"
GraphicResourcePath: str = "Resources/Graphic/"
# generic audio parameters
SoundExtension: str = ".wav"
AudioResourcePath: str = "Resources/Audio/"
# generic font parameters
FontResourcePath: str = "Resources/Font/"
