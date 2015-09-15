#module 2

# Graph coloring with A*

import sys
import re
import itertools
import time

inFile = sys.argv[1]

class Graph:
	def __init__(self, nv, ne, vertices, edges, domain):
		self.vertices = self.createVertices(vertices)
		self.constraints = self.createConstraints(edges)
		self.domains = self.createDomains(vertices,domain)

	def createDomains(self,vertices,domains):
		nodes = {}
		for v in vertices:
			key = "n" + str(v[0])
			nodes[key] = list(domains)
		return nodes

	def createVertices(self,vertices):
		nodes = {}
		for v in vertices:
			key = "n" + str(v[0])
			xy = (v[0],v[1])
			nodes[key] = xy
		return nodes

	def createConstraints(self, edges):
		constraints = []
		for e in edges:
			constraints.append((e[0],e[1]))
		return constraints

# General Arc Consistency
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
		'''
		#generate the initial state
		init_state = self.graph
		# queue av [vertex1,vertex2]
		q = self.initGAC(init_state)
		while len(q) > 0:
			nextPair = q.pop(0)
			#domain of the revised vertex
			prevDomain = nextPair[0].domain
			revisedVertex = revise(nextPair[0], nextPair[1])
			revisedDomain = revisedVertex.domain

			if reduced(prevDomain, revisedDomain):
				q.append()

'''
		#domain filtering loop

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
# number of vertices
nv = instructions[0][0]
# number of edges
ne = instructions[0][1]
# [index_of_vertex, x, y]
ixy = instructions[1:nv+1]
# [index_of_neighbour1, index_of_neighbour2]
neighbours = instructions[nv+2:]

# Domain

domain = [0,1,2,3,4,5,6,7,8,9]
domain1 = [0,1,2,3,4,5,6,7,8,9]
c1 = "=="
g = Graph(nv,ne,ixy,neighbours, domain)
gac = GAC(g)
x = "n0"
gac.revise((x,10),c1)
