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

    def upAddition(self, grid, explore):
        i = 0

        for j in range(0,4):
            if grid[i][j] == grid[i+1][j] and grid[i][j] != 0:
                grid[i][j] += 1
                if not explore:
                    self.points += 2 ** grid[i][j]
                grid[i+1][j] = grid[i+2][j]
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+1][j] == grid[i+2][j] and grid[i+1][j] != 0:
                grid[i+1][j] += 1
                if not explore:
                    self.points += 2 ** grid[i+1][j]
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+2][j] == grid[i+3][j] and grid[i+2][j] != 0:
                grid[i+2][j] += 1
                if not explore:
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

    def downAddition(self, grid, explore):
        i = 0

        for j in range(0,4):
            if grid[i+3][j] == grid[i+2][j] and grid[i+3][j] != 0:
                grid[i+3][j] += 1
                if not explore:
                    self.points += 2 ** grid[i+3][j]
                grid[i+2][j] = grid[i+1][j]
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+2][j] == grid[i+1][j] and grid[i+2][j] != 0:
                grid[i+2][j] += 1
                if not explore:
                    self.points += 2 ** grid[i+2][j]
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+1][j] == grid[i][j] and grid[i+1][j] != 0:
                grid[i+1][j] += 1
                if not explore:
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

    def leftAddition(self, grid, explore):
        j = 0

        for i in range(0,4):
            if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                grid[i][j] += 1
                if not explore:
                    self.points += 2 ** grid[i][j]
                grid[i][j+1] = grid[i][j+2]
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+1] == grid[i][j+2] and grid[i][j+1] != 0:
                grid[i][j+1] += 1
                if not explore:
                    self.points += 2 ** grid[i][j+1]
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+2] == grid[i][j+3] and grid[i][j+2] != 0:
                grid[i][j+2] += 1
                if not explore:
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

    def rightAddition(self, grid, explore):
        j = 0

        for i in range(0,4):
            if grid[i][j+3] == grid[i][j+2] and grid[i][j+3] != 0:
                grid[i][j+3] += 1
                if not explore:
                    self.points += 2 ** grid[i][j+3]
                grid[i][j+2] = grid[i][j+1]
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+2] == grid[i][j+1] and grid[i][j+2] != 0:
                grid[i][j+2] += 1
                if not explore:
                    self.points += 2 ** grid[i][j+2]
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+1] == grid[i][j] and grid[i][j+1] != 0:
                grid[i][j+1] += 1
                if not explore:
                    self.points += 2 ** grid[i][j+1]
                grid[i][j] = 0
        return grid

    # todo, find a way to skip point update on every call of movement
    def updateGrid(self, grid, action):
        gridBeforeMove = copy.deepcopy(grid)
        if action == 0:
            gridAfterMove = self.upAddition(self.swipeUp(copy.deepcopy(gridBeforeMove)),True)
            changedAfterMove = self.changedAfterMove(gridBeforeMove, gridAfterMove)
            return [gridAfterMove, changedAfterMove]
        if action == 1:
            gridAfterMove = self.leftAddition(self.swipeLeft(copy.deepcopy(gridBeforeMove)),True)
            changedAfterMove = self.changedAfterMove(gridBeforeMove, gridAfterMove)
            return [gridAfterMove, changedAfterMove]
        if action == 2:
            gridAfterMove = self.downAddition(self.swipeDown(copy.deepcopy(gridBeforeMove)),True)
            changedAfterMove = self.changedAfterMove(gridBeforeMove, gridAfterMove)
            return [gridAfterMove, changedAfterMove]
        if action == 3:
            gridAfterMove = self.rightAddition(self.swipeRight(copy.deepcopy(gridBeforeMove)),True)
            changedAfterMove = self.changedAfterMove(gridBeforeMove, gridAfterMove)
            return [gridAfterMove, changedAfterMove]


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
    def getNextGridOptions(self, grid):
        grid_options = []
        availableCells = self.availableCells(grid)
        numOfAvailableCells = len(availableCells)
        for cell in availableCells:
            next_grid = copy.deepcopy(grid)
            next_grid[cell[0]][cell[1]] = 1
            grid_options.append([next_grid, 0.9 / numOfAvailableCells])
            next_grid = copy.deepcopy(grid)
            next_grid[cell[0]][cell[1]] = 2
            grid_options.append([next_grid, 0.1 / numOfAvailableCells])
        return grid_options


    def availableCells(self, grid):
        available_cells = []
        for i in range(0,4):
            for j in range(0,4):
                if grid[i][j] == 0:
                    available_cells.append((i,j))
        return available_cells


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

                if self.isEnd(gridAfterMove):
                    return ("lose",gridAfterMove)
                else:
                    return ("valid",gridAfterMove)

        else:
            return ("valid",gridAfterMove)
    def isEnd(self,gridAfterMove):
        temp_grid = copy.deepcopy(gridAfterMove)
        temp_grid_up = copy.deepcopy(gridAfterMove)
        temp_grid_down = copy.deepcopy(gridAfterMove)
        temp_grid_left = copy.deepcopy(gridAfterMove)
        temp_grid_right = copy.deepcopy(gridAfterMove)

        up = self.upAddition(self.swipeUp(temp_grid_up),True)
        down = self.downAddition(self.swipeDown(temp_grid_down),True)
        left = self.leftAddition(self.swipeLeft(temp_grid_left),True)
        right = self.rightAddition(self.swipeRight(temp_grid_right),True)
        if temp_grid == up and temp_grid == down and temp_grid == left and temp_grid == right:
            return True
        return False

    def gradientHeuristic(self,grid):
        if len(self.availableCells(grid)) == 0:
            if self.isEnd(grid):
                return 0
        """gradients = [

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
        gradients = [[10,8,7,6.5],
                    [.5,.7,1,3],
                    [-.5,-1.5,-1.8,-2],
                    [-3.8,-3.7,-3.5,-3]]"""

        gradients = [[13.58,12.19,10.28,9.99],
                    [9.98,8.88,7.67,7.24],
                    [6.07,5.63,3.71,1.62],
                    [1.25,0.99,0.58,0.34]]

        values = 0
        for x in range(0,4):
            for y in range(0,4):
                values += gradients[x][y] * ( 2 ** grid[x][y] )

        return values + len(self.availableCells(grid))*25
