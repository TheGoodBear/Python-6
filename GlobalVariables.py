# Global variables for application

# Screen
Screen = None
# possible screen formats (dictionary with tuples as values)
ScreenFormats = {
    "nHD": (640, 360),
    "qHD": (960, 540),
    "HD": (1280, 720),
    "HD+": (1600, 900),
    "FullHD": (1920, 1080)}
DefaultScreenFormat = "qHD"
# some colors
ColorWhite = (255, 255, 255)
ColorBlack = (0, 0, 0)
# view placeholders
MapPlaceholder = None
BackpackPlaceholder = None
DialogPlaceholder = None

# Game data
Clock = None
FPS = 60

# Resources
ImageExtension = ".png"
GraphicResourcePath = "Resources/Graphic/"
AudioResourcePath = "Resources/Audio/"
