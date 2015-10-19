from visuals import GameWindow
from board import Board
import time
import random
import sys

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
    print b.points
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

    row_indexes_with_zero = []
    column_indexes_with_zero = []

    for i in range(0,4):
        for j in range(0,4):
            if b.grid[i][j] == 0:
                row_indexes_with_zero.append(i)
                column_indexes_with_zero.append(j)
            if grid[i][j] == 2048:
                print "YOU WIN"
                break
    if len(row_indexes_with_zero) > 1:
        random_index = row_indexes_with_zero.index(random.choice(row_indexes_with_zero))
        row_to_place_next = row_indexes_with_zero[random_index]
        column_to_place_next = column_indexes_with_zero[random_index]
        b.grid[row_to_place_next][column_to_place_next] = 1
    elif len(row_indexes_with_zero) == 1:
        row_to_place_next = row_indexes_with_zero[0]
        column_to_place_next = column_indexes_with_zero[0]
        b.grid[row_to_place_next][column_to_place_next] = 1
    else:
        break
print "Congratulations!! You scored ", str(b.points), "points"


window.mainloop()
