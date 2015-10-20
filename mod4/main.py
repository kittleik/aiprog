from visuals import GameWindow
from board import Board
import time
import random
import sys
import copy

window = GameWindow()

grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
firstPieceRow = random.randint(0,3)
firstPieceColumn = random.randint(0,3)
grid[firstPieceRow][firstPieceColumn] = 1
secondPieceRow = random.randint(0,3)
secondPieceColumn = random.randint(0,3)

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
        b.swipeUp(b.grid)
        b.upAddition(b.grid)
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "a":
        b.swipeLeft(b.grid)
        b.leftAddition(b.grid)
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "s":
        b.swipeDown(b.grid)
        b.downAddition(b.grid)
        window.update_view( b.generateState(b.grid) )

    elif movement_choice == "d":
        b.swipeRight(b.grid)
        b.rightAddition(b.grid)
        window.update_view( b.generateState(b.grid) )

    gridAfterMove = copy.deepcopy(b.grid)
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
                if b.grid[i][j] == 0:
                    available_spots.append((i,j))
                if b.grid[i][j] == 2048:
                    print "YOU WIN"
                    break
        print "availspots: " + str(available_spots)
        if len(available_spots) > 1:
            next_spot = random.choice(available_spots)
            b.grid[next_spot[0]][next_spot[1]] = 1
        elif len(available_spots) == 1:
            next_spot = available_spots[0]
            b.grid[next_spot[0]][next_spot[1]] = 1
        else:
            break
        print "nextspot: " + str(next_spot)
print "Congratulations!! You scored ", str(b.points), "points"


window.mainloop()
