import sys
import re
import heapq, Queue

inFile = sys.argv[1]


class Node(object):
    def __init__(self,position, parent):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent = parent
        self.kids = []
        self.position = position


class A_star_search(object):
    def __init__(self):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []


    def calculate_heuristic(self , position ,goal ):
        return abs(position[0]-goal[0]) + abs(position[1]-goal[1])

    def generate_successor(self, node):

        return "TODO, lag dette, return en liste med kidsnoder"

    def unique (self, node):
        return "returner bool"
    def run(self):
        # creating initial node
        start = (1,0)
        goal = (4,2)
        path = []
        move_cost = 1
        initial_node = Node((1,0),None)
        initial_node.g_cost = 1
        initial_node.h_cost = self.calculate_heuristic((1,0), goal)
        initial_node.f_cost = initial_node.g_cost + initial_node.h_cost
        #pushes into openlist that is a priorty queue with
        heapq.heappush(self.openlist, initial_node)
        #Agenda loop

        while True:
            if len(openlist) == 0:
                print "openlist is empty, no solution"
                break

            node = heapq.heappop(self.openlist)
            closedlist.append(node)
            if node.position == self.goal:
                #display path, break the while loop
                # path = 1
                print "solution found"
                break
            #adds to the open list
            successors = generate_successor(node)
            for successor in successors:
                node.appendkid(successor)
                if unique(successor):
                    attach_eval()
                    heapq.heappush(openlist, successor)
                elif node.g_cost + arc_cost(node,successor) < successor.g_cost:
                    attach_eval()
                    if successor in closedlist:
                        propagate_path_improvements(successor)




    #def createState(self, openlist=[]):





class Map:
    def __init__(self, width, height, start, goal, walls):
        #creating empty grid
        self.grid = [[' ' for i in range(width)] for i in range(height)]
        #adding start, goal and walls
        self.grid[start[0]][start[1]] = 'S'
        self.grid[goal[0]][goal[1]] = 'G'

        for i in walls:
            basex = i[0]
            basey = i[1]

            wallwidth = i[2]
            wallheight = i[3]
            for x in range(wallwidth):
                for y in range(wallheight):
                    self.grid[basex+x][basey+y] = '#'

    def printMap(self):
        for i in (self.grid):
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

#star = A_star_search()

#star.run()

print "position (1,0): " + theMap.grid[1][0]
print "position (5,5): " + theMap.grid[5][5]




