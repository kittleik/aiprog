import sys
import re
import heapq, Queue

inFile = sys.argv[1]


class Node(object):
    def __init__(self,x, y, parent, kids):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent = None
        self.kids = []
        self.x = x
        self.y = y


class A_star_search(object):
    def __init__(self):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = set()


    def calculate_heuristic(self ,x ,y ,goal ):
        return abs(x-goal[0]) + abs(y-goal[1])

    def generate_successor(self, node):
        return "TODO, lag dette"

    def run(self):
        # creating initial node
        start = (1,0)
        goal = (4,2)
        path = []
        move_cost = 1
        initial_node = Node(1,0,None,None)
        initial_node.g_cost = 1
        initial_node.h_cost = self.calculate_heuristic(initial_node.x, initial_node.y, goal)
        initial_node.f_cost = initial_node.g_cost + initial_node.h_cost
        #pushes into openlist that is a priorty queue with
        heapq.heappush(self.openlist, (initial_node.f_cost, (1,0)))
        #Agenda loop
        while not path and len(openlist) > 0 :
            f, node = heapq.heappop(self.openlist)
            closedlist.add(node)
            if node == self.goal:
                #display path, break the while loop
                # path = 1
                print "solution found"
                break
            #adds to the open list
            successors = generate_successor(node)
            for successor in successors:
                if unique(successor):
                    closedlist.





    #def createState(self, openlist=[]):





class Map:
    def __init__(self, width, height, start, goal, walls):
        self.grid = [['.' for i in range(width)] for i in range(height)]
        self.grid[start[1]][start[0]] = 'S'
        self.grid[goal[1]][goal[0]] = 'G'

        for i in walls:
            basex = i[0]
            basey = i[1]

            wallwidth = i[2]
            wallheight = i[3]
            for x in range(wallwidth):
                for y in range(wallheight):
                    self.grid[basey+y][basex+x] = '#'

    def printMap(self):
        for i in reversed(self.grid):
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

star = A_star_search()

star.run()

a = ['a','b','c']

if (1,1) == (1,1):
    print "hei"
a.append('f')
print a
