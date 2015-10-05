import sys
import re
import os
import heapq, Queue
from random import shuffle
from Tkinter import *
import time
from node import Node
from grid import Grid
from kart import Kart

inFile = sys.argv[1]

class Search(object):
    def __init__(self, grid):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.map = grid
        self.count = 0
        self.pathlength = 0
        self.path = []

    def getPath(self, node, path):
        path.append(node)
        if node.parent == None:
            return path
        else:
            return self.getPath(node.parent, path)

    # HEURISTIC
    def calculate_heuristic(self , position, goal):
        return abs(position[0]- goal[0]) + abs(position[1]-goal[1])

    # SUCCESSORS
    def generate_successor_astar(self, node):
        successors = []
        #east
        if node.position[0]+1 <= self.map.mapsize[0]-1:
            if (node.position[0]+1, node.position[1]) not in self.map.walls:
                new_node1 = Node((node.position[0]+1, node.position[1]), node)
                successors.append(new_node1)

        #north east
        '''
        if node.position[0]+1 <= self.map.mapsize[0]-1 and node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0]+1, node.position[1]+1) not in self.map.walls:
                new_node2 = Node((node.position[0]+1, node.position[1]+1), node)
                successors.append(new_node2)
        '''
        #north
        if node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0], node.position[1]+1) not in self.map.walls:
                new_node3 = Node((node.position[0], node.position[1]+1), node)
                successors.append(new_node3)

        #north west
        '''
        if node.position[0]-1 >= 0 and node.position[1]+1 <= self.map.mapsize[1]-1:
            if (node.position[0]-1, node.position[1]+1) not in self.map.walls:
                new_node4 = Node((node.position[0]-1, node.position[1]+1), node)
                successors.append(new_node4)
        '''
        #west
        if node.position[0]-1 >= 0:
            if (node.position[0]-1, node.position[1]) not in self.map.walls:
                new_node5 = Node((node.position[0]-1, node.position[1]), node)
                successors.append(new_node5)
        #south west
        '''
        if node.position[0]-1 >= 0 and node.position[1]-1 >= 0:
            if (node.position[0]-1, node.position[1]-1) not in self.map.walls:
                new_node6 = Node((node.position[0]-1, node.position[1]-1), node)
                successors.append(new_node6)
        '''

        #south
        if node.position[1]-1 >= 0:
            if (node.position[0], node.position[1]-1) not in self.map.walls:
                new_node7 = Node((node.position[0], node.position[1]-1), node)
                successors.append(new_node7)
        '''
        #south east
        if node.position[0]+1 <= self.map.mapsize[0]-1 and node.position[1]-1 >= 0:
            if (node.position[0]+1, node.position[1]-1) not in self.map.walls:
                new_node8 = Node((node.position[0]+1, node.position[1]-1), node)
                successors.append(new_node8)
        '''

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

    def addToOpenlist(self,node):
        if mode == "dfs" or mode == "bfs":
            self.openlist.append(node)
        if mode == "astar":
            heapq.heappush(self.openlist, node)

    def removeFromOpenlist(self):
        if mode == "dfs":
            return self.openlist.pop()
        if mode == "bfs":
            return self.openlist.pop(0)
        if mode == "astar":
            return heapq.heappop(self.openlist)

    def run_algorithm(self,mode):
        # creating initial node
        self.start = self.map.start
        print "starting position is %s" % (self.start,)
        self.goal = self.map.goal
        print "the goal is at  %s" % (self.goal,)

        move_cost = 1
        initial_node = Node(self.start,None)
        initial_node.g_cost = 0
        initial_node.h_cost = self.calculate_heuristic(initial_node.position, self.goal)
        initial_node.f_cost = initial_node.g_cost + initial_node.h_cost

        self.addToOpenlist(initial_node)
        #Agenda loop
        best_path_so_far = [list(),list()]

        while True:
            if len(self.openlist) == 0:
                print "openlist is empty, no solution"
                break

            node = self.removeFromOpenlist()
            self.closedlist.append(node)
            self.count += 1

            #GUI
            path = self.getPath(node,path=[])
            best_path_so_far[1] = path
            paintPath(best_path_so_far[0],best_path_so_far[1])

            if node.position == self.goal:
                #display path, break the while loop
                print "solution found"
                print "pathlength: %d" % (len(path))
                print "number of searchnodes: %d\n" %(self.count)

                break
            #adds to the open list
            self.successors = self.generate_successor_astar(node)
            shuffle(self.successors)

            for successor in self.successors:
                node.appendkid(successor)
                #Sjekker om successor node finnes i open- eller closedlist
                if self.unique(successor):
                    #Hvis successor er unik, fiks all info til den og sett den i openlist
                    self.attach_eval(successor, node)
                    self.addToOpenlist(successor)


                elif node.g_cost + successor.move_cost < successor.g_cost:

                    self.attach_eval(successor,node)
                    if successor in self.closedlist:
                        propagate_path_improvements(successor)

            best_path_so_far[0] = path


#==================RUNNING PROGRAM=======================================

onlyNumbers = re.compile('\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
instructions = [[int(y) for y in x] for x in instructions]

width = instructions[0][0]
height = instructions[0][1]
start = instructions[1]
goal = instructions[2]
walls = instructions[3:]

grid = Grid(width, height, start, goal, walls)
grid_copy = Grid(width, height, start, goal, walls)

# ------Tkinter-----------
root = Tk()
mode = "dfs"

def chooseMap(mapFileName):
    print "Ma lage dette for a endre map"
    os.execl(sys.executable, 'python', __file__, mapFileName)

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
    global grid_copy
    paintMap(grid_copy.grid,maxCoordinates(width,height))

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

w = Canvas(topFrame, width=1000, height=1000)
paint_list = []
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
map_Menu.add_command(label="Map0", command=lambda :chooseMap("task0.txt"))
map_Menu.add_command(label="Map1", command=lambda :chooseMap("task1.txt"))
map_Menu.add_command(label="Map2", command=lambda :chooseMap("task2.txt"))
map_Menu.add_command(label="Map3", command=lambda :chooseMap("task3.txt"))
map_Menu.add_command(label="Map4", command=lambda :chooseMap("task4.txt"))
map_Menu.add_command(label="Map5", command=lambda :chooseMap("task5.txt"))
map_Menu.add_command(label="Map6", command=lambda :chooseMap("task6.txt"))
map_Menu.add_command(label="Map7", command=lambda :chooseMap("task7.txt"))

#---------Paint map----------
w = Canvas(topFrame, width=900, height=920)


paintsOnMap = {}
def maxCoordinates(width,height):
    return (width*20,height*20)

def paintSingleSquare(x,y,maxCoord,fill):
    maxY = maxCoord[1]
    key = str(x) + "." + str(y)
    square = paintsOnMap[key]
    w.delete(square)
    paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill=fill, outline = 'white')
    #time.sleep(0.01)
    #root.update()

def paintPath(old_path_list,path_list):

    if len(old_path_list) > 0:
        for node in reversed(old_path_list):
            x = node.position[0]
            y = node.position[1]
            paintSingleSquare(x,y,maxCoordinates(width,height),"grey")

    for node in reversed(path_list):
        x = node.position[0]
        y = node.position[1]
        paintSingleSquare(x,y, maxCoordinates(width,height),"red")
    root.update()


def paintMap(grid, maxCoord):
    w.delete("all")
    maxX = maxCoord[0]
    maxY = maxCoord[1]
    x = 0
    y = 0

    for i in grid:
        for j in i:
            if j == '#':
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill="black", outline = 'white')

                y += 1
            elif j == 'S':
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill="green", outline = 'white')
                y += 1
            elif j == 'G':
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill="blue", outline = 'white')
                y += 1
            elif j == 'x':
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxy-20*y, fill="cyan", outline = 'white')
                y += 1
            elif j == 'o':
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill="red", outline = 'white')
                y += 1
            else:
                key = str(x)+"."+str(y)
                paintsOnMap[key] = w.create_rectangle(20*x, (maxY-20)-20*y ,20+20*x,maxY-20*y, fill="grey", outline = 'white')
                y += 1
        y = 0
        x += 1
    w.pack()

#---------Buttons------------
def start():
    search = Search(grid)
    search.run_algorithm(mode)

button1 = Button(bottomFrame, text="start", fg="red", command=start)
button1.pack()

paintMap(grid.grid, maxCoordinates(width,height))
root.mainloop()
