from random import randrange
from Tile import Tile


class Minesweeper:

    def __init__(self, y, x, mines):
        self.y = y  # height
        self.x = x  # width

        self.mines = mines
        self.flags = mines
        self.tilesRevealed = 0
        self.lost = False

        # gameBoard : array of Tiles, used to represent the minesweeper

        self.gameBoard = [[Tile(i, j, ) for j in range(x)] for i in range(y)]

        # place mines in the minesweeper

        minesPlaced = 0

        while minesPlaced < mines:
            rand_xPos = randrange(0, x)
            rand_yPos = randrange(0, y)
            tile = self.gameBoard[rand_yPos][rand_xPos]

            if not tile.mined:
                tile.mined = True
                minesPlaced += 1

        # calculate adjacent mines

        for item in self.gameBoard:
            for tile in item:
                if not tile.mined:
                    self.calculate_adjacent_mines(tile)

    def correct_pos(self, xPos, yPos):

        # check if the (x, y) position is correct

        return 0 <= xPos < self.x and 0 <= yPos < self.y

    def flags_at_correct_pos(self, tile):
        xPos = tile.xPos
        yPos = tile.yPos
        correctPos = True

        # check if all the flags around the tile are at the correct position (i.e : on a mine)
        # function used when the user double left click

        for i in range(-1, 2):
            for j in range(-1, 2):

                if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                    tile_ij = self.gameBoard[yPos + i][xPos + j]

                    if tile_ij.flagged and not tile_ij.mined:
                        correctPos = False

        return correctPos

    def calculate_adjacent_mines(self, tile):
        nbMines = 0
        xPos = tile.xPos
        yPos = tile.yPos

        for i in range(-1, 2):
            for j in range(-1, 2):

                if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                    tile_ij = self.gameBoard[yPos + i][xPos + j]
                    if tile_ij.mined:
                        nbMines += 1

        tile.adjacentMines = nbMines

    def calculate_adjacent_flags(self, tile):
        nbFlags = 0
        xPos = tile.xPos
        yPos = tile.yPos

        for i in range(-1, 2):
            for j in range(-1, 2):

                if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                    tile_ij = self.gameBoard[yPos + i][xPos + j]
                    if tile_ij.flagged:
                        nbFlags += 1

        tile.adjacentFlags = nbFlags

    def has_tilezero_adjacent(self, tile):
        hasTile0Adjacent = False
        xPos = tile.xPos
        yPos = tile.yPos

        # return true if at least one of the 8 adjacent tiles has 0 adjacent mines

        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                    tile_ij = self.gameBoard[yPos + i][xPos + j]

                    if tile_ij.adjacentMines == 0:
                        hasTile0Adjacent = True

        return hasTile0Adjacent

    def left_click(self, tile):

        if not tile.revealed and not tile.flagged:

            if tile.mined:
                self.reveal_all_tiles()
                self.lost = True

            else:
                self.tilesRevealed += 1

                if tile.adjacentMines > 0:
                    tile.reveal()

                else:
                    tile.reveal()
                    xPos = tile.xPos
                    yPos = tile.yPos

                    # we check all the adjacent tiles
                    # if one of them has 0 adjacent tiles, we reveal it,
                    # we redo this process on this tile we revealed

                    for i in range(-1, 2):
                        for j in range(-1, 2):

                            if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                                tile_ij = self.gameBoard[yPos + i][xPos + j]
                                if self.has_tilezero_adjacent(tile_ij):
                                    self.left_click(tile_ij)

    def double_left_click(self, tile):

        if tile.revealed:

            self.calculate_adjacent_flags(tile)
            if tile.adjacentMines == tile.adjacentFlags:

                xPos = tile.xPos
                yPos = tile.yPos

                if self.flags_at_correct_pos(tile):

                    for i in range(-1, 2):
                        for j in range(-1, 2):

                            if self.correct_pos(yPos=yPos + i, xPos=xPos + j):
                                tile_ij = self.gameBoard[yPos + i][xPos + j]

                                if not tile.flagged:
                                    self.left_click(tile_ij)

                else:
                    self.lost = True
                    self.reveal_all_tiles()

    def right_click(self, tile):

        # when there is 0 flags left and we want to remove one

        if tile.flagged and self.flags == 0:
            tile.flagged = not tile.flagged
            self.flags += 1

        elif not tile.revealed and 0 < self.flags <= self.mines:

            if tile.flagged:
                self.flags += 1
            else:
                self.flags -= 1
            tile.flagged = not tile.flagged

    def reveal_all_tiles(self):
        for item in self.gameBoard:
            for tile in item:
                tile.reveal()

    def won(self):
        nbTiles = self.x * self.y - self.mines
        return nbTiles == self.tilesRevealed

    def game_ended(self):
        return self.lost or self.won()
