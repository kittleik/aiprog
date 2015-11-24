from Tkinter import *

GRID_LEN              = 4
GRID_PADDING          = 10
SIZE                  = 500

BACKGROUND_COLOR_GAME       = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
FONT                        = ("Verdana", 40, "bold")
BACKGROUND_COLOR_DICT       = {
                                1  : '#eee4da',
                                2  : '#ede0c8',
                                3  : '#f2b179',
                                4  : '#f59563',
                                5  : '#f67c5f',
                                6  : '#f65e3b',
                                7  : '#edcf72',
                                8  : '#edcc61',
                                9  : '#edc850',
                                10 : '#edc53f',
                                11 : '#FFAE00',
                                12 : '#444339',
                                13 : '#444339',
                                14 : '#444339',
                                15 : '#444339',
                                16 : '#444339'
                            }

class GameWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.master = master
        self.init_window()
        self.grid()
        self.grid_cells = []
        self.init_grid()
        self.update_view( (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) )
    #end

    def init_window(self):
        self.master.title('2048')
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        mode = Menu(menu)
        mode.add_command(label='normal',command=lambda *args: self.switchMode("normal"))
        mode.add_command(label='ai',command=lambda *args: self.switchMode("ai"))
        menu.add_cascade(label='Mode', menu=mode)

        playButton = Button(self, text="Quit")

    #MENU

    def switchMode(self, mode):
        if mode == "normal":
            print "normal"
        if mode == "ai":
            print "ai"


    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, height = SIZE )
        background.grid()

        for i in range(GRID_LEN):
            # Loop rows
            grid_row = []

            for j in range(GRID_LEN):
                # Loop columns
                cell = Frame(
                            background,
                            bg     = BACKGROUND_COLOR_CELL_EMPTY,
                            width  = SIZE/GRID_LEN,
                            height = SIZE/GRID_LEN)

                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
    #end

    def update_view(self, board ):
        for i in xrange( GRID_LEN ):
            for j in xrange( GRID_LEN ):
                digit = board[i*4+j]
                if digit == 0:
                    self.grid_cells[i][j].configure(
                                                text = "",
                                                bg   = BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    foreground_color = '#f9f6f2' if digit > 2 else '#776e65'
                    number = 1 << digit # the human friendly representation

                    self.grid_cells[i][j].configure(
                                                text = str( 1 << digit ),
                                                bg   = BACKGROUND_COLOR_DICT[ digit ],
                                                fg   = foreground_color )
        self.update_idletasks()
#endclass