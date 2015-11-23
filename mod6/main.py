from visuals import GameWindow
from board import Board
from Tkinter import *
import random, sys, copy, time
from ann import Ann
import numpy as np
import theano
import get_data
from solver import Solver
from welch import welch

def doMove(move):
    if move == 0 or move == "w":
        board.upAddition(board.swipeUp(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 2 or move == "a":
        board.leftAddition(board.swipeLeft(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 1 or move == "s":
        board.downAddition(board.swipeDown(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 3 or move == "d":
        board.rightAddition(board.swipeRight(board.grid),False)
        window.update_view( board.generateState(board.grid) )

def play(ann):
    while True:
        window.update_view( board.generateState(board.grid) )
        print "POINTS========> >  > " + str(board.points) + " <  < <========POINTS"
        print "BEST-TILE = | " + str(2 ** board.bestTile) + " |"
        gridBeforeMove = copy.deepcopy(board.grid)
        pred_in = np.asarray(board.generateState(gridBeforeMove), dtype=theano.config.floatX)
        pred_in = pred_in/13.
        movement_choice = ann.predict([pred_in])
        movement_choice = movement_choice.flatten().tolist()
        print movement_choice
        movement_choice = sorted(range(len(movement_choice)), key=lambda k: movement_choice[k])[::-1]
        print movement_choice

        for move in movement_choice:
            doMove(move)
            gridAfterMove = copy.deepcopy(board.grid)
            if board.changedAfterMove(gridBeforeMove,gridAfterMove):
                break

        #evaluating the game state after a move, win, lose or a valid move
        evaluation, nextBoard = board.evaluateMove(gridBeforeMove, gridAfterMove)
        board.grid = nextBoard
        if evaluation == "win":
            break
        elif evaluation == "lose":
            break
        else:

            window.update_view( board.generateState(board.grid) )

    window.update_view( board.generateState(board.grid) )
    #Feedback about how the game went
    if board.bestTile >= 2048:
        print "Your best tile is: " + str(int(2 ** board.bestTile))
        print "Congratulations!! You scored ", str(board.points), "points"
    else:
        print "YOU DIED"
        print "Your best tile is: " + str(int(2 ** board.bestTile))
        print "You scored ", str(board.points), "points"
    return int(2 ** board.bestTile)

root = Tk()
window = GameWindow(root)


a = Ann(neuronsInHiddenLayers=[16,500,500,4], listOfFunctions=["rectify","rectify","softmax"], learningRate=0.001, momentumRate=10, errorFunc=10)
for i in range (50):
    print "Training data "+str(i+1)
    trX, trY = get_data.get_training_data('training/train_data_'+str(i+1))
    a.training(trX, trY,40,1)

random_res = []
for i in range(50):
    board = Board()
    window.update_view( board.generateState(board.grid) )
    solver = Solver(board, window, root)
    solver.startSolver("random")
    random_res.append(int(2**board.bestTile))

print random_res

ann_res=[]

for asd in range(50):
    board = Board()
    window.update_view( board.generateState(board.grid) )
    x = play(a)
    ann_res.append(x)

print ann_res
#trX, trY = get_data.get_training_data('train_data_1')

welch(random_res,ann_res)


root.mainloop()
