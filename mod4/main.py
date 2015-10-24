from visuals import GameWindow
from board import Board
from solver import Solver
from Tkinter import *
import random, sys, copy, time

root = Tk()
window = GameWindow(root)
board = Board()
window.update_view( board.generateState(board.grid) )
#solver = Solver(board, window, root)
#modes: random, upleftdownright, partialAI
#solver.startSolver("random")
board.grid = [[2,2,4,256],[2,2,4,4],[2,2,4,4],[1024,2,4,4]]
print board.gradientHeuristic(board.grid)
root.mainloop()
