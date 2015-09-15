import sys
import re
import heapq, Queue
from random import shuffle
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
        self.path = []

    def calculate_heuristic(self , position, goal):
        return abs(position[0]- goal[0]) + abs(position[1]-goal[1])

    def generate_successor_bfs(self, node, discovered):
        successors = []
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                if (node.position[0]+1, node.position[1]) not in discovered:
                    new_node1 = Node((node.position[0]+1, node.position[1]), node)
                    new_node1.parent = node
                    successors.append(new_node1)

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                if (node.position[0], node.position[1]+1) not in discovered:
                    new_node2 = Node((node.position[0], node.position[1]+1), node)
                    new_node2.parent = node
                    successors.append(new_node2)

        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                if (node.position[0]-1, node.position[1]) not in discovered:
                    new_node3 = Node((node.position[0]-1, node.position[1]), node)
                    new_node3.parent = node
                    successors.append(new_node3)

        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                if (node.position[0], node.position[1]-1) not in discovered:
                    new_node4 = Node((node.position[0], node.position[1]-1), node)
                    new_node4.parent = node
                    successors.append(new_node4)

        return successors

    def generate_successor_dfs(self, node):
        successors = []
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                new_node1 = Node((node.position[0]+1, node.position[1]), node)
                new_node1.parent = node
                successors.append(new_node1)

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                new_node2 = Node((node.position[0], node.position[1]+1), node)
                new_node2.parent = node
                successors.append(new_node2)

        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                new_node3 = Node((node.position[0]-1, node.position[1]), node)
                new_node3.parent = node
                successors.append(new_node3)

        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                new_node4 = Node((node.position[0], node.position[1]-1), node)
                new_node4.parent = node
                successors.append(new_node4)
        return successors

    def generate_successor_astar(self, node):
        successors = []
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                new_node1 = Node((node.position[0]+1, node.position[1]), node)
                successors.append(new_node1)
            #self.count += 1

        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                new_node2 = Node((node.position[0], node.position[1]+1), node)
                successors.append(new_node2)
            #self.count += 1

        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                new_node3 = Node((node.position[0]-1, node.position[1]), node)
                successors.append(new_node3)
            #self.count += 1

        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                new_node4 = Node((node.position[0], node.position[1]-1), node)
                successors.append(new_node4)
            #self.count += 1

        return successors

    def unique (self, node):
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
        self.path.append(node)
        if node.parent:
            self.draw_path_to_map(node.parent)

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
                paintPath(self.path)
                self.map.printMap()
                break
            if v.position not in discovered:
                discovered.add(v.position)
                successors = self.generate_successor_dfs(v)
                shuffle(successors)
                for successor in successors:
                    stack.append(successor)
                    paintSingleSquare(successor.position[0],successor.position[1],theMap.width,"cyan")
                    paintSingleSquare(successor.parent.position[0],successor.parent.position[1],theMap.width,"yellow")


    def bfs(self, start, goal):
        queue = Queue.Queue()
        initial_node = Node(start,None)
        queue.put(initial_node)
        discovered = set()

        while True:
            if queue.empty():
                break
            next_node = queue.get()
            if next_node.position == goal:
                print "solution found"
                self.draw_path_to_map(next_node)
                #animasjon
                paintPath(self.path)
                self.map.printMap()
                break
            if next_node.position not in discovered:
                discovered.add(next_node.position)

            successors = self.generate_successor_bfs(next_node,discovered)
            shuffle(successors)

            for successor in successors:
                successor.parent = next_node
                queue.put(successor)
                discovered.add(successor.position)
                #animasjon
                paintSingleSquare(successor.position[0],successor.position[1],theMap.width,"cyan")
                paintSingleSquare(successor.parent.position[0],successor.parent.position[1],theMap.width,"yellow")

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
                paintPath(self.path)
                self.map.printMap()
                print "pathlength: %d" % (self.pathlength)
                print "number of searchnodes: %d\n" %(self.count)
                break
            #adds to the open list

            self.successors = self.generate_successor_astar(node)
            shuffle(self.successors)
            for successor in self.successors:
                node.appendkid(successor)
                if self.unique(successor):
                    self.attach_eval(successor, node)
                    heapq.heappush(self.openlist, successor)
                elif node.g_cost + successor.move_cost < successor.g_cost:
                    self.attach_eval(successor,node)
                    if successor in self.closedlist:
                        propagate_path_improvements(successor)
                paintSingleSquare(successor.position[0],successor.position[1],theMap.width,"cyan")
                paintSingleSquare(successor.parent.position[0],successor.parent.position[1],theMap.width,"yellow")



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

#==================RUNNING PROGRAM=======================================

onlyNumbers = re.compile('\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
instructions = [[int(y) for y in x] for x in instructions]

width = instructions[0][0]
height = instructions[0][1]
start = instructions[1]
goal = instructions[2]
walls = instructions[3:]

theMap = Map(width, height, start, goal, walls)
theMap_copy = Map(width, height, start, goal, walls)

# ------Tkinter-----------

root = Tk()
mode = "dfs"

def chooseMap():
    print "Ma lage dette for a endre map"

def switchMode(string):
    global mode
    if string == "dfs":
        mode = "dfs"
    elif string == "bfs":
        mode = "bfs"
    elif string == "astar":
        mode = "astar"
    else:
        print "not a mode"

def reset():
    global theMap_copy
    paintMap(theMap_copy.grid)

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

w = Canvas(topFrame, width=500, height=500)
paint_list = []
def callback():
    x = random.randint(0,19)
    y = random.randint(0,19)
    w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="yellow", outline = 'white')
    #root.after(1000, callback)

def start():
    star = Search(theMap)
    star.bfs(theMap.start,theMap.goal)
    paint_list = star.rekke
    while len(paint_list) > 0:
        square = paint_list.pop(0)
        x = square[0]
        y = square[1]
        w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill="yellow", outline = 'white')

#----------Menu--------------
menu = Menu(root)
root.config(menu=menu)

algorithm_Menu = Menu(menu)
menu.add_cascade(label="Algorithms", menu=algorithm_Menu)
algorithm_Menu.add_command(label="Depth first search", command=lambda *args: switchMode("dfs"))
algorithm_Menu.add_command(label="Breadth first search", command=lambda *args: switchMode("bfs"))
algorithm_Menu.add_command(label="A star", command=lambda *args: switchMode("astar"))
algorithm_Menu.add_command(label="Reset", command=reset)
#subMenu.add_separator()
map_Menu = Menu(menu)
menu.add_cascade(label="Maps", menu=map_Menu)
map_Menu.add_command(label="Map1", command=chooseMap)
map_Menu.add_command(label="Map2", command=chooseMap)
map_Menu.add_command(label="Map3", command=chooseMap)
map_Menu.add_command(label="Map4", command=chooseMap)
map_Menu.add_command(label="Map5", command=chooseMap)
map_Menu.add_command(label="Map6", command=chooseMap)

#---------Paint map----------
w = Canvas(topFrame, width=400, height=420)

def paintSingleSquare(x,y,the_map,fill):
    w.create_rectangle(20*x, (400-20)-20*y ,20+20*x,400-20*y, fill=fill, outline = 'white')
    time.sleep(0.01)
    root.update()

def paintPath(path_list):
    for node in reversed(path_list):
        x = node.position[0]
        y = node.position[1]
        paintSingleSquare(x,y,theMap,"red")
        time.sleep(0.01)
        root.update()

def paintMap(grid):
    x = 0
    y = 0

    for i in grid:
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

#---------Buttons------------
def start():
    search = Search(theMap)
    if mode == "bfs":
        search.bfs(theMap.start,theMap.goal)
    elif mode == "dfs":
        search.dfs(theMap.start,theMap.goal)
    elif mode == "astar":
        search.a_star()
    else:
        "this mode is not made"
button1 = Button(bottomFrame, text="start", fg="red", command=start)
button1.pack()

paintMap(theMap.grid)
root.mainloop()

#theMap.printMap()

#star = Search(theMap)
#star.dfs(theMap.start,theMap.goal)
#star.bfs(theMap.start,theMap.goal)
#star.run()
