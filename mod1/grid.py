class Grid:
    def __init__(self, width, height, start, goal, walls):
        self.start = start
        self.goal = goal
        self.width = width
        self.height = height
        #creating empty grid
        self.mapsize =(width,height)
        self.grid = [['.' for i in range(width)] for i in range(height)]
        #adding start, goal and walls
        self.goal = tuple(goal)
        self.start = tuple(start)
        self.grid[start[0]][start[1]] = 'S'
        self.grid[goal[0]][goal[1]] = 'G'
        self.walls = []

        for i in walls:
            basex = i[0]
            basey = i[1]

            wallwidth = i[2]
            wallheight = i[3]
            for x in range(wallwidth):
                for y in range(wallheight):
                    self.grid[basex+x][basey+y] = '#'
                    self.walls.append((basex+x,basey+y))

        #print self.grid
    def printMap(self):
        for i in (self.grid):
            print '|',
            for y in i:
                print y,
            print '|'
        print "\n"
