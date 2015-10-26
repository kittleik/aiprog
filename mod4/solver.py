import copy, time, random
from operator import itemgetter

class Solver():
    def __init__(self,board,gui,root):
        self.root = root
        self.board = board
        self.gui = gui


    def expectimax(self, grid, depth, agentIndex):
        player = 0
        rand = 1

        if depth <= 0:
            return [ self.getUtility(grid), 0 ]

        if agentIndex == player:
            best = [0, 0]
            for action in range(0,4):
                next_grid_list = self.board.updateGrid(grid, action)
                next_grid = next_grid_list[0]
                moved = next_grid_list[1]
                if not moved:
                    continue
                value_list = self.expectimax(next_grid, depth - 1, rand)
                value = value_list[0]
                if value >= best[0]:
                    best = [value, action]
            return best
        else:
            grid_options = self.board.getNextGridOptions(grid)
            best = 0
            for grid_option in grid_options:
                next_grid = grid_option[0]
                probability = grid_option[1]
                value_list = self.expectimax(next_grid, depth - 1, player)
                value = value_list[0]
                best = best + value * probability
            return [best, 0]



    def getUtility(self,grid):
        if len(self.board.availableCells(grid)) == 0:
            if self.board.isEnd(grid):
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

        value = 0
        for x in range(0,4):
            for y in range(0,4):
                value += gradients[x][y] * ( 2 ** grid[x][y] )

        return value + len(self.board.availableCells(grid))*25

    def generateNextState(self, state):
        currentState = state
        self.gui.update_view(self.board.generateState(state))

    def lookOneStepAhead(self, state):
        temp_grid = copy.deepcopy(state)
        temp_grid_up = copy.deepcopy(state)
        temp_grid_down = copy.deepcopy(state)
        temp_grid_left = copy.deepcopy(state)
        temp_grid_right = copy.deepcopy(state)

        up = self.board.upAddition(self.board.swipeUp(temp_grid_up),False)
        down = self.board.downAddition(self.board.swipeDown(temp_grid_down),False)
        left = self.board.leftAddition(self.board.swipeLeft(temp_grid_left),False)
        right = self.board.rightAddition(self.board.swipeRight(temp_grid_right),False)

        values = []
        if self.board.changedAfterMove(temp_grid, up):
            values.append(( self.board.gradientHeuristic(up) , "up"))
        if self.board.changedAfterMove(temp_grid, down):
            values.append(( self.board.gradientHeuristic(down) , "down"))
        if self.board.changedAfterMove(temp_grid, left):
            values.append(( self.board.gradientHeuristic(left) , "left"))
        if self.board.changedAfterMove(temp_grid, right):
            values.append(( self.board.gradientHeuristic(right) , "right"))

        sorted_values = sorted(values, key=itemgetter(0), reverse=True)
        return sorted_values.pop(0)




    def doMove(self, move):
        if move == "up":
            print "up"
            self.board.upAddition(self.board.swipeUp(self.board.grid),False)
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()

        if move == "down":
            print "down"
            self.board.downAddition(self.board.swipeDown(self.board.grid),False)
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()
        if move == "left":
            print "left"
            self.board.leftAddition(self.board.swipeLeft(self.board.grid),False)
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()
        if move == "right":
            print "right"
            self.board.rightAddition(self.board.swipeRight(self.board.grid),False)
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()

    def converNumberToDirection(self, number):
        if number == 0:
            return "up"
        if number == 1:
            return "left"
        if number == 2:
            return "down"
        if number == 3:
            return "right"


    def nextMove(self,mode,lastMove):
        if mode == "upleftdownright":
            if lastMove == "up":
                return "left"
            elif lastMove == "left":
                return "down"
            elif lastMove == "down":
                return "right"
            elif lastMove == "right":
                return "up"
        elif mode == "random":
            return random.choice(["up","down","left","right"])
        elif mode == "onestepahead":
            return self.lookOneStepAhead(self.board.grid)[1]
        elif mode == "expectimax":
            if len(self.board.availableCells(self.board.grid)) < 2:
                depth = 5
            elif len(self.board.availableCells(self.board.grid)) > 2 and len(self.board.availableCells(self.board.grid)) <= 4:
                depth = 4
            elif len(self.board.availableCells(self.board.grid)) > 4 and len(self.board.availableCells(self.board.grid)) <= 7:
                depth = 3
            else:
                depth = 3
            return self.converNumberToDirection(self.expectimax(self.board.grid, depth, 0)[1])
        else:
            print "THIS H.WARD GAAAAAY"

    def startSolver(self,mode):
        self.gui.update_view(self.board.generateState(self.board.grid))
        self.root.update()
        moveTodo = self.converNumberToDirection(self.expectimax(self.board.grid, 3, 0)[1])
        print moveTodo
        #moveTodo = "up"

        while True:
            #print "POINTS========> >  > " + str(self.board.points) + " <  < <========POINTS"
            #print "BEST-TILE = | " + str(2 ** self.board.bestTile) + " |"

            gridBeforeMove = copy.deepcopy(self.board.grid)
            self.doMove(moveTodo)
            gridAfterMove = copy.deepcopy(self.board.grid)
            #evaluating the game state after a move, win, lose or a valid move
            evaluation, gridAfterEvaluation = self.board.evaluateMove(gridBeforeMove, gridAfterMove)
            if evaluation == "win":
                self.gui.update_view(self.board.generateState(gridAfterEvaluation))
                self.root.update()
                break
            elif evaluation == "lose":
                self.gui.update_view(self.board.generateState(gridAfterEvaluation))
                self.root.update()
                break
            else:
                self.board.grid = gridAfterEvaluation
                self.gui.update_view(self.board.generateState(self.board.grid))

            moveTodo = self.nextMove(mode,moveTodo)

        if self.board.bestTile >= 2048:
            print "Your best tile is: " + str(int(2 ** self.board.bestTile))
            print "Congratulations!! You scored ", str(self.board.points), "points"
        else:
            print "YOU DIED"
            print "Your best tile is: " + str(int(2 ** self.board.bestTile))
            print "You scored ", str(self.board.points), "points"
