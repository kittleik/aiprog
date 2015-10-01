#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gac import GAC
from graph import Graph
import re
import sys
import heapq, Queue

inFile = sys.argv[1]


class Node(object):
    def __init__(self,state, parent):
        self.state = state
        self.f_cost = 0
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
    def generateSuccerssors(self, domains):
        successors = []
        for k in domains:
            for d in domains[k]:


class Search(object):

    def __init__(self, graph):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.states = {}

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

    def a_star(self,state):
            # creating initial node
            # Setter opp første node og dens state
            state = state
            node = Node(state,None)
            node.f = node.computeHeuristic(self.states[state])
            heapq.heappush(self.openlist, node)

            #AGENDA LOOP
            while True:
                if len(self.openlist) == 0:
                    print "openlist is empty, no solution"
                    break
                node = heapq.heappop(self.openlist)
                state_domains = self.states[node.state]
                successors = node.generateSuccerssors(state_domains)
                #print successors

                '''
                successors = node.generateSuccerssors()
                # generate successors
                for successor in successors:
                    generateUID(Node(runGac(successor), node))
'''


            '''
            #Agenda loop
            count = 0
            while True:

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
                    #Sjekker om successor node finnes i open- eller closedlist
                    if self.unique(successor):
                        #Hvis successor er unik, fiks all info til den og sett den i openlist
                        self.attach_eval(successor, node)
                        heapq.heappush(self.openlist, successor)
                    elif node.g_cost + successor.move_cost < successor.g_cost:
                        #hvis ikke
                        self.attach_eval(successor,node)
                        if successor in self.closedlist:
                            propagate_path_improvements(successor)
                '''



    # --------------------READING GRAPH FROM FILE---------------------------

onlyNumbers = re.compile('\d+(?:\.\d+)?')

instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]
instructions = [[int(y) for y in x] for x in instructions]
# number of variables
nv = instructions[0][0]
# number of edges
ne = instructions[0][1]
# [index_of_vertex, x, y]
ixy = instructions[1:nv+1]
# [index_of_neighbour1, index_of_neighbour2]
edges = instructions[nv+2:]

domain = [0,1,2,3,4,5]
g = Graph(ixy,edges,domain,nv)
'''
g.domains["n18"] = [1]
g.domains["n12"] = [2]
g.domains["n11"] = [3]
g.domains["n10"] = [4]
g.domains["n15"] = [5]
g.domains["n13"] = [0]
g.domains["n2"] = [1]
'''

# Kjører GAC første gang
gac = GAC(g)
# Returnerer (Bool,{domains})
result = gac.runGAC(gac.graph.domains)
done = result[0]
filtered_initial_domains = result[1]

search = Search(g)
# Lager UID
initial_uid = search.generateUID(filtered_initial_domains)
# Setter inn domains med UID inn i A* sin states dictionary
search.states[initial_uid] = filtered_initial_domains
search.a_star(initial_uid)



#search.a_star(state)
#print search.generateUID(domains)

#print "----neighbors-----"
#print gac.graph.neighbors
