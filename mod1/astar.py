import sys
import re
import heapq, Queue
import wx
import wx.grid
import random
from Tkinter import *
import time

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
        self.distance = None

    #heapen sorterer etter f verdien til noden
    def __cmp__(self, other):
        return cmp(self.f_cost, other.f_cost)

    def appendkid(self, node):
        self.kids.append(node)


class Search(object):

    def __init__(self, map):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.map = map
        self.map.printMap()
        self.count = 0
        self.pathlength = 0
        self.colored = set()

    def calculate_heuristic(self , position, goal):
        return abs(position[0]- goal[0]) + abs(position[1]-goal[1])

    def generate_successor_bfs(self, node, discovered):
        successors = []
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                if (node.position[0]+1, node.position[1]) not in discovered:
                    new_node1 = Node((node.position[0]+1, node.position[1]), node)
                    successors.append(new_node1)

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                if (node.position[0], node.position[1]+1) not in discovered:
                    new_node2 = Node((node.position[0], node.position[1]+1), node)
                    successors.append(new_node2)

        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                if (node.position[0]-1, node.position[1]) not in discovered:
                    new_node3 = Node((node.position[0]-1, node.position[1]), node)
                    successors.append(new_node3)

        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                if (node.position[0], node.position[1]-1) not in discovered:
                    new_node4 = Node((node.position[0], node.position[1]-1), node)
                    successors.append(new_node4)

        return successors

    def generate_successor_dfs(self, node):
        successors = []
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                new_node1 = Node((node.position[0]+1, node.position[1]), node)
                successors.append(new_node1)

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                new_node2 = Node((node.position[0], node.position[1]+1), node)
                successors.append(new_node2)

        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                new_node3 = Node((node.position[0]-1, node.position[1]), node)
                successors.append(new_node3)

        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                new_node4 = Node((node.position[0], node.position[1]-1), node)
                successors.append(new_node4)

        return successors

    def generate_successor_astar(self, node):
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
        # kan bruke dictionary her for optimalisering
        for closed in self.closedlist:
            if node.position == closed.position:
                return False

        for opened in self.openlist:
            if node.position == opened.position:
                return False
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
                kid.f_cost = kid.g_cost + kid.h_cost
                self.propogate_path_improvements(kid)

    def draw_path_to_map(self, node):
        self.pathlength += 1
        self.map.grid[node.position[0]][node.position[1]] = 'x'
        if node.parent:
            self.draw_path_to_map(node.parent)

    def draw_path_dfs(self,colored):
        for t in colored:
            self.map.grid[t[0]][t[1]] = 'x'

    def dfs(self,start,goal):
        initial_node = Node(start,None)
        discovered = set()
        stack = []
        stack.append(initial_node)
        while len(stack) > 0:
            v = stack.pop()
            if v.position == goal:
                print "solution found"
                self.draw_path_to_map(v)
                self.map.printMap()
                print "pathlength: %d" % (self.pathlength)
                print "number of searchnodes: %d\n" %(self.count)
                break
            if v.position not in discovered:
                discovered.add(v.position)
                successors = self.generate_successor_dfs(v)
                for successor in successors:
                    stack.append(successor)

    def bfs(self, start, goal):
        queue = Queue.Queue()
        initial_node = Node(start,None)
        initial_node.distance = 0
        queue.put(initial_node)
        discovered = set()

        while True:
            if queue.empty():
                break
            next_node = queue.get()
            self.map.grid[next_node.position[0]][next_node.position[1]] = 'o'
            if next_node.position == goal:
                print "solution found"
                self.draw_path_to_map(next_node)
                self.map.printMap()
                print "pathlength: %d" % (self.pathlength)
                print "number of searchnodes: %d\n" %(self.count)
                break
            if next_node.position not in discovered:
                discovered.add(next_node.position)
            successors = self.generate_successor_bfs(next_node,discovered)
            for successor in successors:
                if successor.distance == None:
                    successor.distance = next_node.distance + 1
                    successor.parent = next_node
                    queue.put(successor)
                    discovered.add(successor.position)


    def a_star(self):
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
            self.count += 1
            self.closedlist.append(node)
            if node.position == self.goal:
                #display path, break the while loop
                print "solution found"
                self.draw_path_to_map(node)
                self.map.printMap()
                print "pathlength: %d" % (self.pathlength)
                print "number of searchnodes: %d\n" %(self.count)
                break
            #adds to the open list
            self.successors = self.generate_successor_astar(node)
            for successor in self.successors:
                node.appendkid(successor)
                if self.unique(successor):
                    self.attach_eval(successor, node)
                    heapq.heappush(self.openlist, successor)
                elif node.g_cost + successor.move_cost < successor.g_cost:
                    self.attach_eval(successor,node)
                    if successor in self.closedlist:
                        propagate_path_improvements(successor)

        print len(self.openlist)


    #def createState(self, openlist=[]):



class Map:
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

# ------Tkinter-----------

theMap = Map(width, height, start, goal, walls)

root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(bottomFrame, text="start", fg="red")
button1.pack()
w = Canvas(topFrame, width=500, height=500)

x = 0
y = 0
max_y = 380
for i in theMap.grid:
    for j in i:
        if j == '#':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="black", outline = 'white')
            y += 1
        elif j == 'S':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="green", outline = 'white')
            y += 1
        elif j == 'G':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="blue", outline = 'white')
            y += 1
        elif j == 'x':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="cyan", outline = 'white')
            y += 1
        elif j == 'o':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="red", outline = 'white')
            y += 1
        else:
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="grey", outline = 'white')
            y += 1
    y = 0
    x += 1
w.pack()

star = Search(theMap)
#star.dfs(theMap.start,theMap.goal)
#star.bfs(theMap.start,theMap.goal)
star.a_star()


x = 0
y = 0
max_y = 380
for i in theMap.grid:
    for j in i:
        if j == '#':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="black", outline = 'white')
            y += 1
        elif j == 'S':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="green", outline = 'white')
            y += 1
        elif j == 'G':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="blue", outline = 'white')
            y += 1
        elif j == 'x':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="cyan", outline = 'white')
            y += 1
        elif j == 'o':
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="red", outline = 'white')
            y += 1
        else:
            w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="grey", outline = 'white')
            y += 1
    y = 0
    x += 1
w.pack()


root.mainloop()



#theMap.printMap()

#star = Search(theMap)
#star.dfs(theMap.start,theMap.goal)
#star.bfs(theMap.start,theMap.goal)
#star.run()

