from tkinter import *


class Tile():

    def __init__(self, yPos, xPos):
        self.xPos = xPos
        self.yPos = yPos
        self.flagged = False
        self.revealed = False
        self.mined = False
        self.adjacentMines = 0
        self.adjacentFlags = 0

    def reveal(self):
        self.revealed = True
