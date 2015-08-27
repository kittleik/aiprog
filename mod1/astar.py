import sys
import re
inFile = sys.argv[1]

class Map:
    def __init__(self, width, height, start, goal, walls):
        self.grid = [['  ' for i in range(width)] for i in range(height)]
        self.grid[start[1]][start[0]] = 'S '
        self.grid[goal[1]][goal[0]] = 'G '

        for i in walls:
            basex = i[0]
            basey = i[1]

            wallwidth = i[2]
            wallheight = i[3]
            for x in range(wallwidth):
                for y in range(wallheight):
                    self.grid[basey+y][basex+x] = '##'

    def neighbors(self, xpos, ypos):
        results = [()]

    def printMap(self):
        for i in self.grid:
            print '|',
            for y in i:
                print y,
            print '|'

onlyNumbers = re.compile('\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
instructions = [[int(y) for y in x] for x in instructions]

width = instructions[0][0]
height = instructions[0][1]
start = instructions[1]
goal = instructions[2]
walls = instructions[3:]

theMap = Map(width, height, start, goal, walls)

theMap.printMap()
