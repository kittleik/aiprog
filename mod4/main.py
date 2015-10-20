from visuals import GameWindow
from board import Board
import time
import random
import sys
import copy
import math

bestTile = 0


def nextPiece():
    possible = [1,1,1,1,1,1,1,1,1,2]
    return random.choice(possible)

window = GameWindow()
#Setting up game grid first time


grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
firstPieceRow = random.randint(0,3)
firstPieceColumn = random.randint(0,3)
grid[firstPieceRow][firstPieceColumn] = 1
secondPieceRow = random.randint(0,3)
secondPieceColumn = random.randint(0,3)
b = Board(grid)
window.update_view( b.generateState(b.grid) )

while True:
    if firstPieceRow == secondPieceRow and firstPieceColumn == secondPieceRow:
        secondPieceRow = random.randint(0,3)
        secondPieceColumn = random.randint(0,3)
    else:
        grid[secondPieceRow][secondPieceColumn] = 1
        break

b = Board(grid)
window.update_view( b.generateState(b.grid) )

while True:
    window.update_view( b.generateState(b.grid) )
    print b.points
    print "---before---"
    gridBeforeMove = copy.deepcopy(b.grid)
    print gridBeforeMove
    print "------------"
    movement_choice = raw_input("Make your move::::>>>>    ")
    if movement_choice == "exit":
        break
    elif movement_choice == "w":
        b.upAddition(b.swipeUp(b.grid))
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "a":
        b.leftAddition(b.swipeLeft(b.grid))
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "s":
        b.downAddition(b.swipeDown(b.grid))
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "d":
        b.rightAddition(b.swipeRight(b.grid))
        window.update_view( b.generateState(b.grid) )

    gridAfterMove = b.grid
    print "---after---"
    print "before: " + str(gridBeforeMove)
    print "after: " + str(gridAfterMove)

    changed = False

    for i in range(0,4):
        if changed:
            break
        for j in range(0,4):
            if gridBeforeMove[i][j] != gridAfterMove[i][j]:
                changed = True
                break

    if changed:
        available_spots = []

        for i in range(0,4):
            for j in range(0,4):
                if b.grid[i][j] > bestTile:
                    bestTile = b.grid[i][j]
                if b.grid[i][j] == 0:
                    available_spots.append((i,j))
                if b.grid[i][j] == 2048:
                    print "YOU WIN"
                    break
        print "bestTile: " + str(int(math.pow(2,bestTile)))
        print "availspots: " + str(available_spots)
        print len(available_spots)
        if len(available_spots) > 1:
            next_spot = random.choice(available_spots)
            b.grid[next_spot[0]][next_spot[1]] = nextPiece()
        elif len(available_spots) == 1:
            next_spot = available_spots[0]
            b.grid[next_spot[0]][next_spot[1]] = nextPiece()
            window.update_view( b.generateState(b.grid) )

            # CHECK IF POSSIBLE TO MOVE IN THE DIFFERENT DIRECTIONS
            temp_grid = copy.deepcopy(b.grid)
            temp_grid_up = copy.deepcopy(b.grid)
            temp_grid_down = copy.deepcopy(b.grid)
            temp_grid_left = copy.deepcopy(b.grid)
            temp_grid_right = copy.deepcopy(b.grid)

            up = b.upAddition(b.swipeUp(temp_grid_up))
            down = b.downAddition(b.swipeDown(temp_grid_down))
            left = b.leftAddition(b.swipeLeft(temp_grid_left))
            right = b.rightAddition(b.swipeRight(temp_grid_right))


            if temp_grid == up and temp_grid == down and temp_grid == left and temp_grid == right:
                break
        print "nextPiece: " + str(b.grid[next_spot[0]][next_spot[1]])
        print "nextspot: " + str(next_spot)

if bestTile >= 2048:
    print "Your best tile is: " + str(int(math.pow(2,bestTile)))
    print "Congratulations!! You scored ", str(b.points), "points"
else:
    print "YOU DIED"
    print "Your best tile is: " + str(int(math.pow(2,bestTile)))
    print "You scored ", str(b.points), "points"



window.mainloop()
