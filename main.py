from Minesweeper import Minesweeper
from GameGUI import GameGUI

height = 10
width = 10
number_of_mines = 10

minesweeper = Minesweeper(y=height, x=width, mines=number_of_mines)
GameGUI = GameGUI(minesweeper)
