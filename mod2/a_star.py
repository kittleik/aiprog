#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gac import GAC
from graph import Graph
import re
import sys
import heapq, Queue
import copy
import time
import Tkinter as tk

start_time = time.time()





class Node(object):
    def __init__(self,state, parent):
        self.state = state
        self.f_cost = self.computeHeuristic(state)
        self.parent = parent
        self.kids = []

    def __cmp__(self, other):
        return cmp(self.f_cost, other.f_cost)

    def appendkid(self, node):
        self.kids.append(node)

    def computeHeuristic(self, domains):
        result = 0
        for domain in domains:
            result += (len(domains[domain]) - 1)
        return result
    def generateSuccerssors(self,  parent, search):
        successors = []
        solution = False
        domains = parent.state
        assumption_choice = "n0"

        x = 100

        for node in domains:
            if 1 < len(domains[node]) < x:
                assumption_choice= node
                x = len(domains[node])
                if x == 2:
                    break
        print assumption_choice,

        search.assumtions +=1
        for c in domains[assumption_choice]:
            domains[assumption_choice] = [c]
            successor = search.gac.domainFilteringLoop(domains, assumption_choice)
            # Returnerer (Bool, {newDomains})
            if successor[0]:
                solution = Node(successor[1],parent)
                #break
            #legger til alle barn
            successors.append(Node(successor[1],parent))

    #for k in domains:
        #for d in domains[k]:
        return solution, successors


class Search(object):

    def __init__(self, gac):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.states = {}
        self.assumtions = 0
        self.gac = gac
        #incremental variables
        self.incrementalOpenlist = []

        self.incremental = False

    def makeStringFromList(self, list):
        result = ""
        for i in list:
            result += str(i)
        return result


    def generateUID(self,domains):
        uid = ""
        for key in domains:
            uid += (key + self.makeStringFromList(domains[key]))
        return uid

    def a_star(self):
        # creating initial node
        # Setter opp første node og dens state
        domains = self.gac.graph.domains
        # Kjører gac med full domains
        self.gac.runGAC(domains, assumed=None)
        node = Node(domains,None)
        heapq.heappush(self.openlist, node)

        #AGENDA LOOP
        while True:
            if len(self.openlist) == 0:
                print "openlist is empty, no solution"
                return
            node = heapq.heappop(self.openlist)

            solution, successors = node.generateSuccerssors(node, self)
            #print successors

            if solution:
                print solution.state
                print "THIS IS THE FUCKING SOPULTIONB!!!!!!!!3<3<3<3<3"
                print self.assumtions
                return solution

            for suc in successors:

                heapq.heappush(self.openlist, suc)

    def incremental_a_star(self):

        if not self.incremental:

            heapq.heapify(self.incrementalOpenlist)
            self.incremental = True

            domains = self.gac.graph.domains
            self.gac.runGAC(domains, assumed=None)
            node = Node(domains,None)
            heapq.heappush(self.incrementalOpenlist, node)

            return node

        if not self.incrementalOpenlist:
            self.incremental = False
            return False

        node = heapq.heappop(self.incrementalOpenlist)
        solution, successors = node.generateSuccerssors(node, self)

        if solution:
            print solution.state
            print "THIS IS THE FUCKING SOPULTIONB!!!!!!!!3<3<3<3<3"
            print self.assumtions
            self.resetIncremental()
            return solution

        for suc in successors:

            heapq.heappush(self.incrementalOpenlist, suc)
        return node

    def resetIncremental(self):
        self.incrementalOpenlist = []
        self.incremental = False

class GUI(tk.Tk):
    def __init__(self, graph):
        tk.Tk.__init__(self)
        self.graph = copy.deepcopy(graph)
        self.gac = GAC(self.graph)
        self.search = Search(self.gac)
        self.graph_size = 800.0
        self.vertex_size = 10.0

        self.ixy, self.x_size, self.y_size = self.getIXY()

        self.canvas = tk.Canvas(self, width = self.graph_size+50, height = self.graph_size+50, borderwidth = 0)
        self.canvas.pack(side="top", fill="both", expand="true")


        self.solveButton = tk.Button(self.canvas, text="solve", command=self.drawSolution)
        self.startAnimationButton = tk.Button(self.canvas, text="start ani", command=self.startAnimation)
        self.stopAnimationButton = tk.Button(self.canvas, text="stop ani", command=self.resetGraph)
        self.incrementButton = tk.Button(self.canvas, text="increment", command=self.incrementSolution)
        self.resetButton = tk.Button(self.canvas, text="reset", command=self.resetGraph)

        self.solveButton.pack(side="right")
        self.startAnimationButton.pack(side="right")
        self.stopAnimationButton.pack(side="right")
        self.incrementButton.pack(side="right")
        self.resetButton.pack(side="right")

        self.oval = {}

        for edge in self.graph.edges:

            x1 = (self.ixy[edge[0]][1] * (self.graph_size / self.x_size)) + (self.vertex_size / 2)
            y1 = (self.ixy[edge[0]][2] * (self.graph_size / self.y_size)) + (self.vertex_size / 2)
            x2 = (self.ixy[edge[1]][1] * (self.graph_size / self.x_size)) + (self.vertex_size / 2)
            y2 = (self.ixy[edge[1]][2] * (self.graph_size / self.y_size)) + (self.vertex_size / 2)

            self.canvas.create_line(x1, y1 ,x2, y2)

        for vertex in self.ixy:
            x1 = vertex[1] * (self.graph_size / self.x_size)
            y1 = vertex[2] * (self.graph_size / self.y_size)

            x2 = x1 + self.vertex_size
            y2 = y1 + self.vertex_size

            self.oval[vertex[1], vertex[2]] = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="gray80", tag="oval")

        #Place the window in the topmost left corner to prevent glitches in the gui
        #self.canvas.xview_moveto(0)
        #self.canvas.yview_moveto(0)
    def startAnimation(self):
        self.drawDomains(self.search.incremental_a_star().state)
        self.animateSolution()

    def animateSolution(self):
        if self.search.incremental:
            self.drawDomains(self.search.incremental_a_star().state)
            self.after(50, self.animateSolution)


    def incrementSolution(self):
        self.drawDomains(self.search.incremental_a_star().state)
        return
    def drawSolution(self):
        self.search.resetIncremental()
        start_time = time.time()
        domains = self.search.a_star().state
        print "The run time is %s seconds"%(time.time()-start_time)
        self.drawDomains(domains)

    def resetGraph(self):
        for oval in self.oval:
            self.setOvalColor(oval, "gray80")

    def setOvalColor(self, i, color):
        self.canvas.itemconfig(self.oval[i], fill=color)

    def drawDomains(self, domains):
        for domain in domains:
            i = int(domain[1:])
            node_x = self.graph.ixy[i][1]
            node_y = self.graph.ixy[i][2]
            i = (node_x,node_y)
            if len(domains[domain]) == 1:
                self.setOvalColor(i, domains[domain])
            else:
                self.setOvalColor(i, "gray80")

    def getIXY(self):
        ixy = self.gac.graph.ixy

        x_size = 0
        y_size = 0

        x_max = ixy[0][1]
        x_min = ixy[0][1]
        y_max = ixy[0][2]
        y_min = ixy[0][2]

        for index in ixy:
            if index[1] > x_max:
                x_max = index[1]
            if index[1] < x_min:
                x_min = index[1]
            if index[2] > y_max:
                y_max = index[2]
            if index[2] < y_min:
                y_min = index[2]

        if x_min<0:
            x_size = x_max-x_min
            for index in ixy:
                index[1] += abs(x_min)
        else:
            x_size = x_max

        if y_min<0:
            y_size = y_max-y_min
            for index in ixy:
                index[2] += abs(y_min)
        else:
            y_size = y_max

        return ixy, x_size, y_size




    # --------------------READING GRAPH FROM FILE---------------------------
inFile = sys.argv[1]
onlyNumbers = re.compile('\-?\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
#instructions = [[int(y) for y in x] for x in instructions]
# number of variables

nv = int(instructions[0][0])

# number of edges

ne = int(instructions[0][1])

# [index_of_vertex, x, y]

ixy = instructions[1:nv+1]

for node in ixy:
    node[0] = int(node[0])
    node[1] = float(node[1])
    node[2] = float(node[2])

# [index_of_neighbour1, index_of_neighbour2]
edges = instructions[nv+1:]
for constraint in range(len(edges)):
    for node in range(len(edges[constraint])):
        edges[constraint][node] = int(edges[constraint][node])
domain_count = int(sys.argv[2])
print domain_count
domain = ["red","blue","yellow","orange","cyan","green","plum", "black", "azure","brown"]
domain = domain[:domain_count]
g = Graph(ixy,edges,domain,nv)
'''
g.domains["n18"] = [1]
g.domains["n12"] = [2]
g.domains["n11"] = [3]

g.domains["n10"] = [4]
g.domains["n15"] = [5]
g.domains["n13"] = [0]

'''
#g.domains["n3"] = [3]
# Kjører GAC første gang

#lag GUI



# Returnerer (Bool,{domains})
"""
result = gac.runGAC(gac.graph.domains)
done = result[0]
filtered_initial_domains = result[1]
"""

gui = GUI(g)
gui.mainloop()



# Lager UID
#initial_uid = search.generateUID(filtered_initial_domains)
# Setter inn domains med UID inn i A* sin states dictionary
#search.states[initial_uid] = filtered_initial_domains
#search.a_star(initial_uid)



#search.a_star(state)
#print search.generateUID(domains)

#print "----neighbors-----"
#print gac.graph.neighbors
