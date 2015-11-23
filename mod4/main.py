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
solver.startSolver("random")
'''for i in range(1,50):
    board = Board()
    window.update_view( board.generateState(board.grid) )
    solver = Solver(board, window, root, train_nr=i)
#modes: random, upleftdownright, partialAI, onestepahead
    solver.startSolver("expectimax")'''

# TO PLAY THE GAME, UMCOMMENT THESE LINES
'''
while True:
    window.update_view( board.generateState(board.grid) )
    print "POINTS========> >  > " + str(board.points) + " <  < <========POINTS"
    print "BEST-TILE = | " + str(2 ** board.bestTile) + " |"
    gridBeforeMove = copy.deepcopy(board.grid)
    movement_choice = raw_input("Make your move::::>>>>    ")
    if movement_choice == "exit":
        sys.exit(0)
    elif movement_choice == "w":
        board.upAddition(board.swipeUp(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif movement_choice == "a":
        board.leftAddition(board.swipeLeft(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif movement_choice == "s":
        board.downAddition(board.swipeDown(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif movement_choice == "d":
        board.rightAddition(board.swipeRight(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    gridAfterMove = copy.deepcopy(board.grid)
    #evaluating the game state after a move, win, lose or a valid move
    evaluation, nextBoard = board.evaluateMove(gridBeforeMove, gridAfterMove)
    if evaluation == "win":
        break
    elif evaluation == "lose":
        break
    else:
        board.grid = nextBoard
        window.update_view( board.generateState(board.grid) )

#Feedback about how the game went
if bestTile >= 2048:
    print "Your best tile is: " + str(int(2 ** board.bestTile))
    print "Congratulations!! You scored ", str(board.points), "points"
else:
    print "YOU DIED"
    print "Your best tile is: " + str(int(2 ** board.bestTile))
    print "You scored ", str(board.points), "points"

'''
root.mainloop()
