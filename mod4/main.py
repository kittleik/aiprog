from visuals import GameWindow
from board import Board

window = GameWindow()


b = Board()
#b.checkNeighbour("up")
board1 = b.generateState(b.grid)


board = [   # A list of values currently present in the board on the form 2^x.
            # Eg: the number 4 implies that the graphical board should display,
            # 2^4 = 16, the digit 16. This board represents the board in the screen dump below.
            0, 2, 4, 4,
            0, 2, 1, 3,
            0, 1, 1, 3,
            0, 0, 2, 1
        ]


window.update_view( board1 )

window.mainloop()
