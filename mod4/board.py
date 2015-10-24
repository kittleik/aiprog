from cell import Cell
import random
import copy

class Board():

    def __init__(self):
        self.grid = self.initGrid()
        self.state = self.generateState(self.grid)
        self.points = 0
        self.bestTile = 0

    def initGrid(self):
        grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        firstPiece = (random.randint(0,3), random.randint(0,3))
        grid[firstPiece[0]][firstPiece[1]] = 1

        secondPiece = (random.randint(0,3), random.randint(0,3))
        while True:
            if firstPiece == secondPiece:
                secondPiece = (random.randint(0,3), random.randint(0,3))
            else:
                break
        grid[secondPiece[0]][secondPiece[1]] = 1
        return grid

    #Turning grid [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] into --> [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Using "state form" to update UI
    def generateState(self,grid):
        state = []
        for row in grid:
            for element in row:
                state.append(element)
        return state

    def swipeUp(self, grid):
        i = 0
        for j in range(0,4):
            if grid[i][j] != 0 or grid[i+1][j] != 0 or grid[i+2][j] != 0 or grid[i+3][j] != 0:
                if grid[i][j] == 0:
                    while grid[i][j] == 0:
                        grid[i][j] = grid[i+1][j]
                        grid[i+1][j] = grid[i+2][j]
                        grid[i+2][j] = grid[i+3][j]
                        grid[i+3][j] = 0

                if grid[i+1][j] == 0 and (grid[i+2][j] != 0 or grid[i+3][j] != 0):
                    while grid[i+1][j] == 0:
                        grid[i+1][j] = grid[i+2][j]
                        grid[i+2][j] = grid[i+3][j]
                        grid[i+3][j] = 0

                if grid[i+2][j] == 0 and grid[i+3][j] != 0:
                    while grid[i+2][j] == 0:
                        grid[i+2][j] = grid[i+3][j]
                        grid[i+3][j] = 0

        return grid

    def upAddition(self, grid):
        i = 0

        for j in range(0,4):
            if grid[i][j] == grid[i+1][j] and grid[i][j] != 0:
                grid[i][j] += 1
                print "to be added :" + str(2 ** grid[i][j])
                self.points += 2 ** grid[i][j]
                grid[i+1][j] = grid[i+2][j]
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+1][j] == grid[i+2][j] and grid[i+1][j] != 0:
                grid[i+1][j] += 1
                print "to be added :" + str(2 ** grid[i+1][j])
                self.points += 2 ** grid[i+1][j]
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+2][j] == grid[i+3][j] and grid[i+2][j] != 0:
                grid[i+2][j] += 1
                print "to be added :" + str(2 ** grid[i+1][j])
                self.points += 2 ** grid[i+1][j]
                grid[i+3][j] = 0
        return grid


    def swipeDown(self, grid):
        i = 0
        for j in range(0,4):
            if grid[i][j] != 0 or grid[i+1][j] != 0 or grid[i+2][j] != 0 or grid[i+3][j] != 0:
                if grid[i+3][j] == 0:
                    while grid[i+3][j] == 0:
                        grid[i+3][j] = grid[i+2][j]
                        grid[i+2][j] = grid[i+1][j]
                        grid[i+1][j] = grid[i][j]
                        grid[i][j] = 0

                if grid[i+2][j] == 0 and (grid[i+1][j] != 0 or grid[i][j] != 0):
                    while grid[i+2][j] == 0:
                        grid[i+2][j] = grid[i+1][j]
                        grid[i+1][j] = grid[i][j]
                        grid[i][j] = 0

                if grid[i+1][j] == 0 and grid[i][j] != 0:
                    while grid[i+1][j] == 0:
                        grid[i+1][j] = grid[i][j]
                        grid[i][j] = 0
        return grid

    def downAddition(self, grid):
        i = 0

        for j in range(0,4):
            if grid[i+3][j] == grid[i+2][j] and grid[i+3][j] != 0:
                grid[i+3][j] += 1
                self.points += 2 ** grid[i+3][j]
                grid[i+2][j] = grid[i+1][j]
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+2][j] == grid[i+1][j] and grid[i+2][j] != 0:
                grid[i+2][j] += 1
                self.points += 2 ** grid[i+2][j]
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+1][j] == grid[i][j] and grid[i+1][j] != 0:
                grid[i+1][j] += 1
                self.points += 2 ** grid[i+1][j]
                grid[i][j] = 0
        return grid

    def swipeLeft(self, grid):
        j = 0
        for i in range(0,4):
            if grid[i][j] != 0 or grid[i][j+1] != 0 or grid[i][j+2] != 0 or grid[i][j+3] != 0:
                if grid[i][j] == 0:
                    while grid[i][j] == 0:
                        grid[i][j] = grid[i][j+1]
                        grid[i][j+1] = grid[i][j+2]
                        grid[i][j+2] = grid[i][j+3]
                        grid[i][j+3] = 0

                if grid[i][j+1] == 0 and (grid[i][j+2] != 0 or grid[i][j+3] != 0):
                    while grid[i][j+1] == 0:
                        grid[i][j+1] = grid[i][j+2]
                        grid[i][j+2] = grid[i][j+3]
                        grid[i][j+3] = 0

                if grid[i][j+2] == 0 and grid[i][j+3] != 0:
                    while grid[i][j+2] == 0:
                        grid[i][j+2] = grid[i][j+3]
                        grid[i][j+3] = 0
        return grid

    def leftAddition(self, grid):
        j = 0

        for i in range(0,4):
            if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                grid[i][j] += 1
                self.points += 2 ** grid[i][j]
                grid[i][j+1] = grid[i][j+2]
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+1] == grid[i][j+2] and grid[i][j+1] != 0:
                grid[i][j+1] += 1
                self.points += 2 ** grid[i][j+1]
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+2] == grid[i][j+3] and grid[i][j+2] != 0:
                grid[i][j+2] += 1
                self.points += 2 ** grid[i][j+2]
                grid[i][j+3] = 0
        return grid

    def swipeRight(self, grid):
        j = 0
        for i in range(0,4):
            if grid[i][j] != 0 or grid[i][j+1] != 0 or grid[i][j+2] != 0 or grid[i][j+3] != 0:
                if grid[i][j+3] == 0:
                    while grid[i][j+3] == 0:
                        grid[i][j+3] = grid[i][j+2]
                        grid[i][j+2] = grid[i][j+1]
                        grid[i][j+1] = grid[i][j]
                        grid[i][j] = 0

                if grid[i][j+2] == 0 and (grid[i][j+1] != 0 or grid[i][j] != 0):
                    while grid[i][j+2] == 0:
                        grid[i][j+2] = grid[i][j+1]
                        grid[i][j+1] = grid[i][j]
                        grid[i][j] = 0

                if grid[i][j+1] == 0 and grid[i][j] != 0:
                    while grid[i][j+1] == 0:
                        grid[i][j+1] = grid[i][j]
                        grid[i][j] = 0
        return grid

    def rightAddition(self, grid):
        j = 0

        for i in range(0,4):
            if grid[i][j+3] == grid[i][j+2] and grid[i][j+3] != 0:
                grid[i][j+3] += 1
                self.points += 2 ** grid[i][j+3]
                grid[i][j+2] = grid[i][j+1]
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+2] == grid[i][j+1] and grid[i][j+2] != 0:
                grid[i][j+2] += 1
                self.points += 2 ** grid[i][j+2]
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+1] == grid[i][j] and grid[i][j+1] != 0:
                grid[i][j+1] += 1
                self.points += 2 ** grid[i][j+1]
                grid[i][j] = 0
        return grid

    #Creating a piece with probability 90% for piece |2| and 10% for piece |4|
    def generatePiece(self):
        possible = [1,1,1,1,1,1,1,1,1,2]
        return random.choice(possible)

    def changedAfterMove(self,before,after):
        changed = False
        for i in range(0,4):
            if changed:
                break
            for j in range(0,4):
                if before[i][j] != after[i][j]:
                    changed = True
                    break
        return changed

    #Evaluating a move returns ("win", grid), ("lose", grid) or ("valid", grid)
    def evaluateMove(self, before, after):
        gridBeforeMove = copy.deepcopy(before)
        gridAfterMove = copy.deepcopy(after)

        changed = self.changedAfterMove(gridBeforeMove,gridAfterMove)

        if changed:
            available_spots = []
            for i in range(0,4):
                for j in range(0,4):
                    #updating best tile
                    if gridAfterMove[i][j] > self.bestTile:
                        self.bestTile = gridAfterMove[i][j]
                    #appending available spots
                    if gridAfterMove[i][j] == 0:
                        available_spots.append((i,j))
                    #evaluate if game is won
                    if gridAfterMove[i][j] == 2048:
                        print "YOU WIN"
                        return ("win", gridAfterMove)
            if len(available_spots) > 1:
                next_spot = random.choice(available_spots)
                gridAfterMove[next_spot[0]][next_spot[1]] = self.generatePiece()
                return ("valid",gridAfterMove)
            elif len(available_spots) == 1:
                next_spot = available_spots[0]
                gridAfterMove[next_spot[0]][next_spot[1]] = self.generatePiece()
                # CHECK IF POSSIBLE TO MOVE IN THE DIFFERENT DIRECTIONS WHEN THERE IS NO EMPTY SPACES LEFT
                temp_grid = copy.deepcopy(gridAfterMove)
                temp_grid_up = copy.deepcopy(gridAfterMove)
                temp_grid_down = copy.deepcopy(gridAfterMove)
                temp_grid_left = copy.deepcopy(gridAfterMove)
                temp_grid_right = copy.deepcopy(gridAfterMove)

                up = self.upAddition(self.swipeUp(temp_grid_up))
                down = self.downAddition(self.swipeDown(temp_grid_down))
                left = self.leftAddition(self.swipeLeft(temp_grid_left))
                right = self.rightAddition(self.swipeRight(temp_grid_right))
                if temp_grid == up and temp_grid == down and temp_grid == left and temp_grid == right:
                    return ("lose",gridAfterMove)
                else:
                    return ("valid",gridAfterMove)

        else:
            return ("valid",gridAfterMove)

    def gradientHeuristic(self,grid):
        gradients = [
                    [[ 3,  2,  1,  0],
                     [ 2,  1,  0, -1],
                     [ 1,  0, -1, -2],
                     [ 0, -1, -2, -3]],
                    [[ 0,  1,  2,  3],
                     [-1,  0,  1,  2],
                     [-2, -1,  0,  1],
                     [-3, -2, -1, -0]],
                    [[ 0, -1, -2, -3],
                     [ 1,  0, -1, -2],
                     [ 2,  1,  0, -1],
                     [ 3,  2,  1,  0]],
                    [[-3, -2, -1,  0],
                     [-2, -1,  0,  1],
                     [-1,  0,  1,  2],
                     [ 0,  1,  2,  3]]
                    ]
        values = [0, 0, 0, 0]
        print grid
        for i in range(0,4):
            for x in range(0,4):
                for y in range(0,4):
                    values[i] += gradients[i][x][y] * grid[x][y]
        print values
        return max(values)
