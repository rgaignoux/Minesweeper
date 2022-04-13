from tkinter import *
import time
from Minesweeper import Minesweeper


class GameGUI:

    def __init__(self, ms):

        self.minesweeper = ms
        self.gameBoard = self.minesweeper.gameBoard
        self.height = self.minesweeper.y
        self.width = self.minesweeper.x

        # initialization of the GUI

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Minesweeper')
        self.root.iconphoto(True, PhotoImage(file='images/logo.png'))

        # the two containers of the GUI (bottom = the minesweeper, top = game menu)

        self.bottom_container = Frame(self.root)  # contains the tiles
        self.top_container = Frame(self.root)  # contains the timer, restart button and number of mines

        # font

        my_font = ("Verdana", 20, 'bold')

        # images

        self.button_smiley = PhotoImage(file='images/button_smiley.png')
        self.button_smiley_win = PhotoImage(file='images/button_smiley_win.png')
        self.button_smiley_loose = PhotoImage(file='images/button_smiley_loose.png')

        self.unopened_tile = PhotoImage(file='images/tile_unopened.png')
        self.opened_tile = PhotoImage(file='images/tile_opened.png')
        self.tile_flagged = PhotoImage(file='images/tile_flagged.png')

        self.tile_mined = PhotoImage(file='images/tile_mined.png')
        self.tile_mined_red = PhotoImage(file='images/tile_mined_red.png')
        self.tile_flagged_wrong = PhotoImage(file='images/tile_flagged_wrong.png')

        self.tile_1 = PhotoImage(file='images/tile_1.png')
        self.tile_2 = PhotoImage(file='images/tile_2.png')
        self.tile_3 = PhotoImage(file='images/tile_3.png')
        self.tile_4 = PhotoImage(file='images/tile_4.png')
        self.tile_5 = PhotoImage(file='images/tile_5.png')
        self.tile_6 = PhotoImage(file='images/tile_6.png')
        self.tile_7 = PhotoImage(file='images/tile_7.png')
        self.tile_8 = PhotoImage(file='images/tile_8.png')

        #
        # initialization of the bottom frame
        #

        self.button_array = [[Button() for i in range(self.height)] for j in range(self.width)]

        for i in range(self.height):
            for j in range(self.width):
                tile_ij = Button(self.bottom_container, width=40, height=40,
                                 image=self.unopened_tile, borderwidth=0, highlightthickness=0)

                # binds of the button :
                #   - left click : open a tile
                #   - right click : put or remove a flag
                #   - double left click : remove multiple squares at once (if flagged wrong around, the user loses)

                tile_ij.bind('<Button-1>', self.left_click)
                tile_ij.bind('<Button-3>', self.right_click)
                tile_ij.bind('<Double 1>', self.double_left_click)

                tile_ij.grid(row=i, column=j)

                self.button_array[i][j] = tile_ij

        #
        # initialization of the top frame
        #

        topframe_height = 100
        topframe_width = 40 * self.width
        bg_color = '#BDBDBD'

        self.top_container.configure(height=topframe_height, width=topframe_width, bg=bg_color)

        #
        # initialization of the flags label, the restart button and the timer
        #

        # flags label

        self.flags_label = Label(self.top_container, text=self.minesweeper.flags, font=my_font, bg=bg_color)

        # restart button

        self.restart_button = Button(self.top_container, image=self.button_smiley, borderwidth=0, highlightthickness=0,
                                     command=lambda: self.restart_game(mines=self.minesweeper.mines))

        # timer

        self.start_time = int(time.time())

        self.timer_label = Label(self.top_container, text=0, font=my_font, bg=bg_color)

        # we run this function one time, and it runs every second after that
        self.update_timer()

        #
        # put all the components in a grid of 1*3 (flags at the left, button in the center, timer at the right)
        #

        self.flags_label.grid(column=1, row=1, sticky="w", padx=30, pady=20)  # w : west
        self.restart_button.grid(column=2, row=1)
        self.timer_label.grid(column=3, row=1, sticky="e", padx=30, pady=20)  # e : east

        self.top_container.grid_columnconfigure(1, minsize=topframe_width / 3)
        self.top_container.grid_columnconfigure(2, minsize=topframe_width / 3)
        self.top_container.grid_columnconfigure(3, minsize=topframe_width / 3)

        #
        # packing all the frames into the root
        #

        self.bottom_container.pack(side='bottom')
        self.top_container.pack(side='top')

        self.root.mainloop()

    def right_click(self, event):
        if not self.minesweeper.game_ended():
            y = event.widget.grid_info()['row']
            x = event.widget.grid_info()['column']

            tile = self.gameBoard[y][x]

            self.minesweeper.right_click(tile)
            self.actualise_GUI(tile)

    def left_click(self, event):
        if not self.minesweeper.game_ended():
            y = event.widget.grid_info()['row']
            x = event.widget.grid_info()['column']

            tile = self.gameBoard[y][x]

            self.minesweeper.left_click(tile)
            self.actualise_GUI(tile)

    def double_left_click(self, event):
        if not self.minesweeper.game_ended():
            y = event.widget.grid_info()['row']
            x = event.widget.grid_info()['column']

            tile = self.gameBoard[y][x]

            self.minesweeper.double_left_click(tile)
            self.actualise_GUI(tile)

    def actualise_GUI(self, tile_clicked):

        # the tile in the parameter is used when the user clicked on a mine, to put it red

        # actualisation of the flags label

        self.flags_label['text'] = self.minesweeper.flags

        # actualisation of the smiley button (restart button)

        if self.minesweeper.won():
            self.restart_button.configure(image=self.button_smiley_win)

        elif self.minesweeper.lost:
            self.restart_button.configure(image=self.button_smiley_loose)

        # actualisation of the tiles buttons

        for i in range(self.height):
            for j in range(self.width):

                tile = self.gameBoard[i][j]
                button = self.button_array[i][j]

                if tile.revealed:

                    if tile.mined:

                        # red mine
                        if tile_clicked == tile:
                            button.configure(image=self.tile_mined_red)

                        # normal mine
                        else:
                            button.configure(image=self.tile_mined)

                    # tile flagged wrong
                    elif tile.flagged and not tile.mined:
                        button.configure(image=self.tile_flagged_wrong)

                    # tile not mined
                    else:
                        button.configure(image=self.tile_image(tile.adjacentMines))

                # tile flagged
                elif tile.flagged:
                    button.configure(image=self.tile_flagged)

                else:
                    button.configure(image=self.unopened_tile)

    def tile_image(self, adjacentMines):
        if adjacentMines == 0:
            return self.opened_tile
        if adjacentMines == 1:
            return self.tile_1
        elif adjacentMines == 2:
            return self.tile_2
        elif adjacentMines == 3:
            return self.tile_3
        elif adjacentMines == 4:
            return self.tile_4
        elif adjacentMines == 5:
            return self.tile_5
        elif adjacentMines == 6:
            return self.tile_6
        elif adjacentMines == 7:
            return self.tile_7
        elif adjacentMines == 8:
            return self.tile_8

    def update_timer(self):

        # we stop the timer when the game is ended
        if not self.minesweeper.game_ended():
            current_time = time.time()
            time_elapsed = int(current_time - self.start_time)

            # change time on the timer label
            self.timer_label["text"] = time_elapsed

            # run itself again after 1000 ms
            self.timer_label.after(1000, self.update_timer)

    def restart_game(self, mines):
        # we create a new window
        new_minesweeper = Minesweeper(self.height, self.width, mines)
        # self.root.after_cancel()
        self.root.destroy()
        self.__init__(new_minesweeper)
