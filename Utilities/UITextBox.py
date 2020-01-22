"""
    Inspired from :

    Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.
    Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.

    Note : for PyGame 1.9.x
"""

import sys
import os.path

import pygame
import pygame.locals as pl

pygame.font.init()


class TextInput:
    """
        This class let's the user input a short, one-lines piece of text at a blinking cursor
        that can be moved using the arrow-keys. 
        Delete, backspace, home and end are functional.
        Return returns 
    """
    def __init__(
            self,
            InitialString="",
            FontFamily="",
            FontSize=20,
            Antialias=True,
            TextColor=(0, 0, 0),
            CursorColor=(0, 0, 1),
            RepeatKeysInitialDelay=400,
            RepeatKeysInterval=35,
            MaxStringLength=-1):
        """
            :param InitialString: Initial text to be displayed
            :param FontFamily: name or list of names for font (see pygame.font.match_font for precise format)
            :param FontSize:  Size of font in pixels
            :param Antialias: Determines if antialias is applied to font (uses more processing power)
            :param TextColor: Color of text (duh)
            :param CursorColor: Color of cursor
            :param RepeatKeysInitialDelay: Time in ms before keys are repeated when held
            :param RepeatKeysInterval: Interval between key press repetition when held
            :param MaxStringLength: Allowed length of text (-1 = no limit)
        """

        # Text variables
        self.Antialias = Antialias
        self.TextColor = TextColor
        self.FontSize = FontSize
        self.MaxStringLength = MaxStringLength
        self.InputString = InitialString  # Input text

        # Get font
        if not os.path.isfile(FontFamily):
            FontFamily = pygame.font.match_font(FontFamily)
        self.FontObject = pygame.font.Font(FontFamily, FontSize)

        # Text-surface will be created during the first update call:
        self.Surface = pygame.Surface((1, 1))
        self.Surface.set_alpha(0)

        # Variables to manage key repeat after specified delay
        self.KeyRepeatCounters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.KeyRepeatIntialDelay = RepeatKeysInitialDelay
        self.KeyRepeatInterval = RepeatKeysInterval

        # Cursor variables
        self.CursorSurface = pygame.Surface((int(self.FontSize / 20 + 1), self.FontSize))
        self.CursorSurface.fill(CursorColor)
        self.CursorPosition = len(InitialString)
        self.CursorVisible = True  # switches every CursorBlinkDelay ms
        self.CursorBlinkDelay = 500
        self.CursorBlinkTime = 0

        self.Clock = pygame.time.Clock()

    def Update(self, EventList):

        for CurrentEvent in EventList:
            if CurrentEvent.type == pygame.KEYDOWN:
                # show cursor
                self.CursorVisible = True  

                # if none exist, create a counter for that key
                if CurrentEvent.key not in self.KeyRepeatCounters:
                    self.KeyRepeatCounters[CurrentEvent.key] = [0, CurrentEvent.unicode]

                if CurrentEvent.key == pl.K_RETURN or CurrentEvent.key == pl.K_KP_ENTER:
                    # return input string
                    return True

                elif CurrentEvent.key == pl.K_BACKSPACE:
                    # delete previous character and move cursor back 1 space
                    self.InputString = (
                        self.InputString[:max(self.CursorPosition - 1, 0)]
                        + self.InputString[self.CursorPosition:]
                    )
                    self.CursorPosition = max(self.CursorPosition - 1, 0)

                elif CurrentEvent.key == pl.K_DELETE:
                    # delete next character
                    self.InputString = (
                        self.InputString[:self.CursorPosition]
                        + self.InputString[self.CursorPosition + 1:]
                    )

                elif CurrentEvent.key == pl.K_RIGHT:
                    # move cursor 1 space forward, do not exceed string length
                    self.CursorPosition = min(self.CursorPosition + 1, len(self.InputString))

                elif CurrentEvent.key == pl.K_LEFT:
                    # move cursor 1 space backward
                    self.CursorPosition = max(self.CursorPosition - 1, 0)

                elif CurrentEvent.key == pl.K_END:
                    # move cursor to end of string
                    self.CursorPosition = len(self.InputString)

                elif CurrentEvent.key == pl.K_HOME:
                    # move cursor to start of string
                    self.CursorPosition = 0
             
                elif len(self.InputString) < self.MaxStringLength or self.MaxStringLength == -1:
                    # if string does not exceed max length, add key to string
                    if CurrentEvent.unicode is not None and len(str(CurrentEvent.unicode)) == 1:
                        self.InputString = (
                            self.InputString[:self.CursorPosition]
                            + CurrentEvent.unicode
                            + self.InputString[self.CursorPosition:]
                        )
                        self.CursorPosition += len(CurrentEvent.unicode)  # some unicodes may be empty, like K_UP
                        print(CurrentEvent.unicode)

            elif CurrentEvent.type == pl.KEYUP:
                # note: because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if CurrentEvent.key in self.KeyRepeatCounters:
                    del self.KeyRepeatCounters[CurrentEvent.key]

        # Update key counters:
        for Key in self.KeyRepeatCounters:
            self.KeyRepeatCounters[Key][0] += self.Clock.get_time()  # Update clock

            # generate new key events if enough time has passed:
            if self.KeyRepeatCounters[Key][0] >= self.KeyRepeatIntialDelay:
                self.KeyRepeatCounters[Key][0] = (
                    self.KeyRepeatIntialDelay
                    - self.KeyRepeatInterval
                )

                EventKey, EventUnicode = Key, self.KeyRepeatCounters[Key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=EventKey, unicode=EventUnicode))

        # Re-render text surface:
        self.Surface = self.FontObject.render(self.InputString, self.Antialias, self.TextColor)

        # Update cursor
        self.CursorBlinkTime += self.Clock.get_time()
        if self.CursorBlinkTime >= self.CursorBlinkDelay:
            self.CursorBlinkTime %= self.CursorBlinkDelay
            self.CursorVisible = not self.CursorVisible

        if self.CursorVisible:
            CursorY = self.FontObject.size(self.InputString[:self.CursorPosition])[0]
            # note: without this, the cursor is invisible when cursor position > 0
            if self.CursorPosition > 0:
                CursorY -= self.CursorSurface.get_width()
            self.Surface.blit(self.CursorSurface, (CursorY, 0))

        # Add delay and return to main loop
        self.Clock.tick()
        return False


    def GetSurface(self):
        return self.Surface


    def GetText(self):
        return self.InputString


    def GetCursorPosition(self):
        return self.CursorPosition


    def SetTextColor(self, Color):
        self.TextColor = Color


    def SetCursorColor(self, Color):
        self.CursorSurface.fill(Color)


    def ClearText(self):
        self.InputString = ""
        self.CursorPosition = 0


# Self testing
if __name__ == "__main__":
    pygame.init()

    # create TextInput object
    TextInputTest = TextInput(MaxStringLength=30)

    # initialize screen and event clock with PyGame
    Screen = pygame.display.set_mode((1000, 200))
    Clock = pygame.time.Clock()

    # main loop
    while True:
        Screen.fill((225, 225, 225))

        # get PyGame events
        Events = pygame.event.get()
        for Event in Events:
            # exit when user clicks on windows red cross
            if Event.type == pygame.QUIT:
                sys.exit(0)

        # feed TextInput with events and return input text if Return is pressed
        if TextInputTest.Update(Events):
            # print input text in console
            print(TextInputTest.GetText())
            
        # blit its surface onto the screen
        Screen.blit(TextInputTest.GetSurface(), (10, 10))

        # update screen
        pygame.display.update()

        # event delay
        Clock.tick(30)
