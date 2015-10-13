from cell import Cell



class Board():

    def __init__(self):
        self.grid = [[0,0,3,0],[1,0,2,0],[1,0,0,0],[1,0,2,0]]
        self.state = self.generateState(self.grid)
        #self.rows = [[0, 1, 2, 3],[4, 5, 6, 7],[8, 9, 10, 11],[12, 13, 14, 15]]
        #self.columns = [[0, 4, 8, 12],[1, 5, 9, 13],[2, 6, 10, 14],[3, 7, 11, 15]]




    def generateState(self,grid):
        state = []
        for row in grid:
            for element in row:
                state.append(element)
        return state

    def swipeUp(self):
        for column in self.columns:
            for position in column:
                print "hei"




'''
    def checkNeighbour(self, direction):
        if direction == "up":
            for c in self.columns:
                for p in c:
                    print self.state[p]

    #def merge()


    def moveCells(self):
        for column in self.columns:
            for position in column:
                print self.state[position]
                if self.state[position] > 0:
                    for position in column:
                        print "greater than 0"

'''
