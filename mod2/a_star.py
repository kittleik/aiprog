#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gac import GAC
from graph import Graph
import re
import sys
import heapq, Queue
import copy

inFile = sys.argv[1]


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
        solution = {}
        domains = parent.state
        for variable in domains:
            if len(domains[variable])>1:
                search.assumtions +=1
                print "---------------------"
                print "#########-------ASSUMED VARIABLE: %s   ---------------################" %(variable)
                ##??
                #[1,2,3,4]
                #[1]

                for c in domains[variable]:
                    domains[variable] = [c]
                    print "BEFORE:"
                    print domains

                    successor = search.gac.domainFilteringLoop(domains, variable)
                    # Returnerer (Bool, {newDomains})
                    print "AFTER:"
                    print successor[1]
                    print "-----------------"
                    if successor[0]:
                        solution = successor[1]
                        #break
                    #legger til alle barn
                    successors.append(Node(successor[1],parent))
                break
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
                    print solution
                    print "THIS IS THE FUCKING SOPULTIONB!!!!!!!!3<3<3<3<3"
                    print self.assumtions
                    return
                for suc in successors:

                    heapq.heappush(self.openlist, suc)
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
print ixy
# [index_of_neighbour1, index_of_neighbour2]
edges = instructions[nv+1:]

domain = [0,1,2,3]
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
gac = GAC(g)
# Returnerer (Bool,{domains})
"""
result = gac.runGAC(gac.graph.domains)
done = result[0]
filtered_initial_domains = result[1]
"""
search = Search(gac)
#search.a_star()
# Lager UID
#initial_uid = search.generateUID(filtered_initial_domains)
# Setter inn domains med UID inn i A* sin states dictionary
#search.states[initial_uid] = filtered_initial_domains
#search.a_star(initial_uid)



#search.a_star(state)
#print search.generateUID(domains)

#print "----neighbors-----"
#print gac.graph.neighbors
