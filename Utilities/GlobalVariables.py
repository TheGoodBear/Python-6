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
DefaultScreenFormat: str = "qHD"
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

# Game data
Clock = None
FPS: int = 60

# Resources
# image library for entire application
ImageLibrary: dict = {}
# generic image parameters
ImageExtension: str = ".png"
GraphicResourcePath: str = "Resources/Graphic/"
# generic audio parameters
AudioResourcePath: str = "Resources/Audio/"
