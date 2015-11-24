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
    if move == 0:
        board.upAddition(board.swipeUp(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 2:
        board.leftAddition(board.swipeLeft(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 1:
        board.downAddition(board.swipeDown(board.grid),False)
        window.update_view( board.generateState(board.grid) )

    elif move == 3:
        board.rightAddition(board.swipeRight(board.grid),False)
        window.update_view( board.generateState(board.grid) )

def play(ann):
    while True:
        window.update_view( board.generateState(board.grid) )
        gridBeforeMove = copy.deepcopy(board.grid)
        #pred_in with empty

        pred_in = board.generateState(gridBeforeMove)
        pred_in.append(pred_in.count(0))
        pred_in = np.asarray(pred_in, dtype=theano.config.floatX)
        pred_in[:-1] = pred_in[:-1]/max(pred_in[:-1])
        pred_in[-1] = pred_in[-1]/16.
        '''
        #normal pred_in
        pred_in = board.generateState(gridBeforeMove)
        pred_in = np.asarray(pred_in, dtype=theano.config.floatX)
        pred_in = pred_in/max(pred_in)
        '''
        movement_choice = ann.predict([pred_in])
        movement_choice = movement_choice.flatten().tolist()

        movement_choice = sorted(range(len(movement_choice)), key=lambda k: movement_choice[k])[::-1]

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

    print "Your best tile is: " + str(int(2 ** board.bestTile))
    return int(2 ** board.bestTile)

root = Tk()
window = GameWindow(root)

EPOCHS_PER_GAME             = 10
NEURONS_IN_HIDDEN_LAYERS    = [17,500,500,4]
LIST_OF_FUNCTIONS           = ["rectify","rectify","softmax"]
LEARNING_RATE               = 0.003
MOMENTUM_RATE               = 0.9

a = Ann(neuronsInHiddenLayers=NEURONS_IN_HIDDEN_LAYERS, listOfFunctions=LIST_OF_FUNCTIONS, learningRate=LEARNING_RATE, momentumRate=MOMENTUM_RATE, errorFunc=10)
for i in range (50):
    trX, trY = get_data.get_training_data('training/train_data_'+str(i+1))
    print "Training on data "+str(i+1)
    a.training(trX, trY,len(trX)-1,EPOCHS_PER_GAME)

random_res = []
#random_res = [128, 128, 256, 64, 256, 128, 64, 64, 32, 64, 128, 128, 128, 128, 128, 128, 64, 128, 64, 128, 128, 64, 64, 64, 64, 128, 128, 128, 64, 128, 128, 128, 128, 128, 128, 128, 32, 128, 256, 64, 64, 128, 64, 64, 64, 128, 128, 64, 128, 64]

for i in range(50):
    print "Random game: "+str(i+1)
    board = Board()
    window.update_view( board.generateState(board.grid) )
    solver = Solver(board, window, root)
    solver.startSolver("random")
    random_res.append(int(2**board.bestTile))


ann_res=[]

for asd in range(50):
    print "ANN game: "+str(asd+1)
    board = Board()
    window.update_view( board.generateState(board.grid) )
    x = play(a)
    ann_res.append(x)
epo_str = "Epochs per game: " + str(EPOCHS_PER_GAME)+"\n"
nu_num_str = "Number of neurons: " + str(NEURONS_IN_HIDDEN_LAYERS)+"\n"
l_func_str = "List of fuctions: " + str(LIST_OF_FUNCTIONS)+"\n"

f = open('test_res.txt','a')
f.write(epo_str)
f.write(nu_num_str)
f.write(l_func_str)
f.write(welch(random_res,ann_res))
f.write('\n')
f.write('-----------------------------------------------------------------------\n')
f.close()
print welch(random_res,ann_res)

root.mainloop()
