# module 2
# General Arc Consistency

import sys
import re
import itertools
import time
from graph import Graph

inFile = sys.argv[1]

class GAC:
	def __init__(self, graph):
		self.queue = []
		self.graph = graph

	def getAllPairs(self, a, b):
		return itertools.product(a,b)

	def get_all_neighboring_arcs(self, var):
		nba = []
		for i in self.graph.constraints:
			if i[0] == var:
				nba.append(i[1])
		for i in self.graph.constraints:
			if i[1] == var:
				nba.append(i[0])
		return nba

	def revise(self, x, c):
		deleted = False

		name = x[1]
		domain = self.graph.domains[x[0]]
		nba = self.get_all_neighboring_arcs(name)
		domain2 = self.graph.domains["n2"]
		a = itertools.product(domain, domain2)



	def initGAC(self, graph):
		#(a,b)
		pairs = self.generatePairs(graph)
		q = []
		for pair in pairs:
			varX = pair[0]
			varY = pair[1]
			nodeX = self.getVertex(varX,graph)
			nodeY = self.getVertex(varY,graph)
			revise_request = [nodeX,nodeY]
			q.append(revise_request)
		# returning a queue of node pairs
		return q

	def generatePairs(self, graph):
		edges = graph.edges
		q = []
		for e in edges:
			pair = (e[0],e[1])
			q.append(pair)
		return q

	def runGAC(self):
		print "VARIABLES"
		print self.graph.variables
		print "DOMAINS"
		print self.graph.domains
		print "NEIGHBORS"
		print self.graph.neighbors
		revise_pairs = []
		for variable in self.graph.neighbors:
			neighbors = self.graph.neighbors[variable]
			for neighbor in neighbors:
				revise_pairs.append((variable, neighbor))
		print revise_pairs

	def makefunc(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names: args = args + "," + n
		print "(lambda " + args[1:] + ": " + expression + ")"
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

	def reduced(self,a,b):
		matches = set(a) & set(b)
		return len(a) == len(matches)


	def domainFiltering(self):
		#TODO implement
		# While queue not empty
		# -TODO-REVISE*(X*,Ci)
		# -call REVISE*(X*Ci)
		# -if domain(X*) gets reduced by the call, then:
		#	- Push TODO-REVISE*(Xkm, Ck) onto QUEUE for all Ck(k not = i) in which X*
		#		appers, and all Xkm not = X*
		return True

	def reRun(self):
		return True


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

domain = [0,1,2]
g = Graph(ixy,edges,domain)
gac = GAC(g)
gac.runGAC()


a = 100
b = 22
c = 11
x = 1
y = 2
z = 3
#func = gac.makefunc(['a','b', 'c'],"a + b + c")
#func(a,b,c)
#print apply(func,[a,y,z])


