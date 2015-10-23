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
#modes: random, upleftdownright, partialAI
solver.startSolver("random")
root.mainloop()
