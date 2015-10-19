from cell import Cell
import numpy as np

class Board():

    def __init__(self, grid):
        self.grid = grid
        self.state = self.generateState(self.grid)
        self.points = 0
        #self.rows = [[0, 1, 2, 3],[4, 5, 6, 7],[8, 9, 10, 11],[12, 13, 14, 15]]
        #self.columns = [[0, 4, 8, 12],[1, 5, 9, 13],[2, 6, 10, 14],[3, 7, 11, 15]]


    def getColumns(self):
        grid = np.array(list(self.grid))
        columns = []
        for i in range(len(grid)):
            columns.append(grid[:,i])
        return np.array(columns).tolist()

    def getRows(self):
        return list(self.grid)


    def generateState(self,grid):
        print grid
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
                    while grid[i+2] == 0:
                        grid[i+2][j] = grid[i+3][j]
                        grid[i+3][j] = 0
        print grid
        return grid

    def upAddition(self, grid):
        i = 0

        for j in range(0,4):
            if grid[i][j] == grid[i+1][j]:
                grid[i][j] = grid[i][j] + grid[i+1][j]
                self.points += grid[i][j] ** 2
                grid[i+1][j] = grid[i+2][j]
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+1][j] == grid[i+2][j]:
                grid[i+1][j] = grid[i+1][j] + grid[i+2][j]
                self.points += grid[i+1][j] ** 2
                grid[i+2][j] = grid[i+3][j]
                grid[i+3][j] = 0

            if grid[i+2][j] == grid[i+3][j]:
                grid[i+2][j] = grid[i+2][j] + grid[i+3][j]
                self.points += grid[i+1][j] ** 2
                grid[i+3][j] = 0
        print grid

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
                    while grid[i+1] == 0:
                        grid[i+1][j] = grid[i][j]
                        grid[i][j] = 0
        print grid
        return grid

    def downAddition(self, grid):
        i = 0

        for j in range(0,4):
            if grid[i+3][j] == grid[i+2][j]:
                grid[i+3][j] = grid[i+3][j] + grid[i+2][j]
                self.points += grid[i][j] ** 2
                grid[i+2][j] = grid[i+1][j]
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+2][j] == grid[i+1][j]:
                grid[i+2][j] = grid[i+2][j] + grid[i+1][j]
                self.points += grid[i+2][j] ** 2
                grid[i+1][j] = grid[i][j]
                grid[i][j] = 0

            if grid[i+1][j] == grid[i][j]:
                grid[i+1][j] = grid[i+1][j] + grid[i][j]
                self.points += grid[i+1][j] ** 2
                grid[i][j] = 0
        print grid


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
        print grid
        return grid

    def leftAddition(self, grid):
        j = 0

        for i in range(0,4):
            if grid[i][j] == grid[i][j+1]:
                grid[i][j] = grid[i][j] + grid[i][j+1]
                self.points += grid[i][j] ** 2
                grid[i][j+1] = grid[i][j+2]
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+1] == grid[i][j+2]:
                grid[i][j+1] = grid[i][j+2] + grid[i][j+3]
                self.points += grid[i][j+1] ** 2
                grid[i][j+2] = grid[i][j+3]
                grid[i][j+3] = 0

            if grid[i][j+2] == grid[i][j+3]:
                grid[i][j+2] = grid[i][j+2] + grid[i][j+3]
                self.points += grid[i][j+2] ** 2
                grid[i][j+3] = 0
        print grid

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
        print grid
        return grid

    def rightAddition(self, grid):
        j = 0

        for i in range(0,4):
            if grid[i][j+3] == grid[i][j+2]:
                grid[i][j+3] = grid[i][j+3] + grid[i][j+2]
                self.points += grid[i][j+3] ** 2
                grid[i][j+2] = grid[i][j+1]
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+2] == grid[i][j+1]:
                grid[i][j+2] = grid[i][j+2] + grid[i][j+1]
                self.points += grid[i][j+2] ** 2
                grid[i][j+1] = grid[i][j]
                grid[i][j] = 0

            if grid[i][j+1] == grid[i][j]:
                grid[i][j+1] = grid[i][j+1] + grid[i][j]
                self.points += grid[i][j+1] ** 2
                grid[i][j] = 0
        print grid
