from visuals import GameWindow
from board import Board
from solver import Solver
from Tkinter import *
import random, sys, copy, time

root = Tk()
window = GameWindow(root)
board = Board()
window.update_view( board.generateState(board.grid) )
solver = Solver(board, window, root)
#modes: random, upleftdownright, partialAI, onestepahead
solver.startSolver("expectimax")



#board.grid = [[0,1,2,3],[1,2,3,4],[2,3,4,6],[3,4,6,10]]
#window.update_view(board.generateState(board.grid))




root.mainloop()
