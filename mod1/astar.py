import sys
import re
import heapq, Queue

inFile = sys.argv[1]


class Node(object):
    def __init__(self,position, parent):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.move_cost = 1
        self.parent = parent
        self.kids = []
        self.position = position

    def __cmp__(self, other):
        return cmp(self.f_cost, other.f_cost)

    def appendkid(self, node):
        self.kids.append(node)

class A_star_search(object):


    def __init__(self, map):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.map = map
        self.map.printMap()
        self.count = 0
        self.pathlength = 0


    def calculate_heuristic(self , position, goal):
        return abs(position[0]- goal[0]) + abs(position[1]-goal[1])

    def generate_successor(self, node):

        successors = []

        if node.position[0]+1 <= self.map.mapsize[0]-1:
            new_node1 = Node((node.position[0]+1, node.position[1]), node)
            successors.append(new_node1)
            #self.count += 1

            if new_node1.position in self.map.walls:
                new_node1.move_cost=10000

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            new_node2 = Node((node.position[0], node.position[1]+1), node)
            successors.append(new_node2)
            #self.count += 1

            if new_node2.position in self.map.walls:
                new_node2.move_cost=10000

        if node.position[0]-1 >= 0:
            new_node3 = Node((node.position[0]-1, node.position[1]), node)
            successors.append(new_node3)
            #self.count += 1

            if new_node3.position in self.map.walls:
                new_node3.move_cost=10000

        if node.position[1]-1 >= 0:
            new_node4 = Node((node.position[0], node.position[1]-1), node)
            successors.append(new_node4)
            #self.count += 1

            if new_node4.position in self.map.walls:
                new_node4.move_cost=10000

        return successors

    def unique (self, node):

        for closed in self.closedlist:
            if node.position == closed.position:
                return False

        for opened in self.openlist:
            if node.position == opened.position:
                return False


        self.count +=1
        return True


    def attach_eval(self, child, parent):
        child.parent = parent
        child.g_cost = parent.g_cost + child.move_cost
        child.h_cost = self.calculate_heuristic(child.position, self.goal)
        child.f_cost = child.g_cost + child.h_cost

    def propogate_path_improvements(self, parent):
        print "propogate_path_improvements()"
        for kid in parent.kids:
            if parent.g_cost + kid.move_cost < kid.g_cost:
                kid.parent = parent
                kid.g_cost = parent.g_cost + kid.move_cost
                kif.f_cost = kid.g_cost + kid.h_cost
                self.propogate_path_improvements(kid)

    def draw_path_to_map(self, node):
        self.pathlength += 1
        self.map.grid[node.position[0]][node.position[1]] = 'x'
        if node.parent:
            self.draw_path_to_map(node.parent)

    def run(self):
        # creating initial node
        self.start = self.map.start
        print "starting position is %s" % (self.start,)
        self.goal = self.map.goal
        print "the goal is at  %s" % (self.goal,)
        path = []
        move_cost = 1
        initial_node = Node(self.start,None)
        initial_node.g_cost = 1
        initial_node.h_cost = self.calculate_heuristic(initial_node.position, self.goal)
        initial_node.f_cost = initial_node.g_cost + initial_node.h_cost
        #pushes into openlist that is a priorty queue with
        heapq.heappush(self.openlist, initial_node)
        #Agenda loop
        count = 0
        while True:
            if len(self.openlist) == 0:
                print "openlist is empty, no solution"
                break
            #print count
            node = heapq.heappop(self.openlist)
            self.map.grid[node.position[0]][node.position[1]] = 'o'
            #self.map.printMap()
            self.closedlist.append(node)
            if node.position == self.goal:
                #display path, break the while loop
                # path = 1
                print "solution found"
                self.draw_path_to_map(node)
                self.map.printMap()
                print "pathlength: %d" % (self.pathlength)
                print "number of searchnodes: %d\n" %(self.count)
                break
            #adds to the open list
            self.successors = self.generate_successor(node)
            for successor in self.successors:
                node.appendkid(successor)
                if self.unique(successor):
                    self.attach_eval(successor, node)
                    heapq.heappush(self.openlist, successor)
                elif node.g_cost + successor.move_cost < successor.g_cost:
                    self.attach_eval(successor,node)
                    if successor in self.closedlist:
                        propagate_path_improvements(successor)



    #def createState(self, openlist=[]):



class Map:
    def __init__(self, width, height, start, goal, walls):
        self.start = start
        self.goal = goal
        self.width = width
        self.height = height
        #creating empty grid
        self.mapsize =(width,height)
        print self.mapsize
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

    def printMap(self):
        for i in (self.grid):
            print '|',
            for y in i:
                print y,
            print '|'
        print "\n"

onlyNumbers = re.compile('\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
instructions = [[int(y) for y in x] for x in instructions]

width = instructions[0][0]
height = instructions[0][1]
start = instructions[1]
goal = instructions[2]
walls = instructions[3:]

theMap = Map(width, height, start, goal, walls)

#theMap.printMap()
node = Node((1,0),None)

star = A_star_search(theMap)
star.run()
