import copy, time, random

class Solver():
    def __init__(self,board,gui,root):
        self.root = root
        self.board = board
        self.gui = gui

    def doMove(self, move):
        if move == "up":
            print "up"
            self.board.upAddition(self.board.swipeUp(self.board.grid))
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()

        if move == "down":
            print "down"
            self.board.downAddition(self.board.swipeDown(self.board.grid))
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()
        if move == "left":
            print "left"
            self.board.leftAddition(self.board.swipeLeft(self.board.grid))
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()
        if move == "right":
            print "right"
            self.board.rightAddition(self.board.swipeRight(self.board.grid))
            self.gui.update_view(self.board.generateState(self.board.grid))
            self.root.update()

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
        else:
            print "THIS H.WARD GAAAAAY"

    def startSolver(self,mode):
        self.gui.update_view(self.board.generateState(self.board.grid))
        self.root.update()
        moveTodo = "up"
        while True:
            print "POINTS========> >  > " + str(self.board.points) + " <  < <========POINTS"
            print "BEST-TILE = | " + str(2 ** self.board.bestTile) + " |"

            gridBeforeMove = copy.deepcopy(self.board.grid)
            self.doMove(moveTodo)
            gridAfterMove = copy.deepcopy(self.board.grid)
            time.sleep(0.1)
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
