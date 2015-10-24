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
solver.startSolver("onestepahead")



#board.grid = [[2,2,4,5],[2,2,4,4],[2,2,4,4],[6,2,4,4]]
#print board.gradientHeuristic(board.grid)
#print solver.lookOneStepAhead(board.grid)


root.mainloop()
