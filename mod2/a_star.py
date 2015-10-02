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

    def generateSuccerssors(self, domains, gac, parent, search):
        successors = []

        for k in domains:
            assumedDomains = copy.deepcopy(domains)
            for d in domains[k]:
                assumedDomains[k] = [d]
                ret = gac.domainFilteringLoop(assumedDomains, k)
                done = ret[0]
                new_domains = ret[1]
                if done:
                    print new_domains
                    return []
                state = self.generateUID(new_domains)
                if not done and new_domains:
                    if state not in search.states:
                        search.states.add(state)
                        newNode = Node(new_domains ,parent)
                        successors.append(newNode)

        return successors

class Search(object):

    def __init__(self, gac):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.states = set()
        self.gac = gac





    def a_star(self):
            # creating initial node
            # Setter opp første node og dens state
            domains = self.gac.graph.domains
            self.gac.runGAC(domains, False)
            node = Node(domains, None)
            self.states.add(node.generateUID(node.state))

            node.computeHeuristic(node.state)
            heapq.heappush(self.openlist, node)
            print self.states
            #AGENDA LOOP
            while True:
                if len(self.openlist) == 0:
                    print "openlist is empty, no solution"
                    break
                node = heapq.heappop(self.openlist)
                # Gjette ny løsning i en av variablene.
                successors = list(node.generateSuccerssors(node.state, self.gac, node, self))
                #print self.openlist
                print len(successors)
                '''
                print len(successors)
                print successors[10].state
                for successor in successors:
                    heapq.heappush(self.openlist, successor)
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

domain = [0,1,2,3,4]
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
search = Search(gac)
#search.a_star()


domains = g.domains
print g.domains
domains["n3"] = [3]

print gac.runGAC(domains,"n3")
print g.domains

#search.a_star(state)
#print search.generateUID(domains)

#print "----neighbors-----"
#print gac.graph.neighbors
