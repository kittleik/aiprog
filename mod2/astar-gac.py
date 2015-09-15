#module 2

# Graph coloring with A*

import sys
import re

inFile = sys.argv[1]

class Vertex:
	def __init__(self, ixy, neighbours, domain):
		self.index = ixy[0]
		self.x = ixy[1]
		self.y = ixy[2]
		self.neighbours = neighbours
		self.domain = domain
		self.state = []

	def setColor(self, color):
		self.color = color

class Graph:
	def __init__(self, nv, ne, vertices, edges, domain):
		self.nv = nv
		self.ne = ne
		self.vertices = []
		self.indices = set()
		self.domain = domain
		self.edges = edges
		# Adding all vertices to a list
		# Applying domains for the vertices
		for v in vertices:
			vertex = Vertex(v, [], self.domain)
			self.vertices.append(vertex)
			self.indices.add(v[0])

		# Applying CSP state to vertices
		for v in self.vertices:
			v.state = self.vertices

		# Applying all edges
		for e in edges:
			e1 = e[0]
			e2 = e[1]
			if e1 in self.indices:
				self.vertices[e1].neighbours.append(e)
			if e2 in self.indices:
				self.vertices[e2].neighbours.append(e)


# General Arc Consistency
class GAC:
	def __init__(self, graph):
		self.queue = []
		self.graph = graph

	def getVertex(self,index,graph):
		return graph.vertices[index]

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
		#generate the initial state
		init_state = self.graph
		# queue av [vertex1,vertex2]
		q = self.initGAC(init_state)

		while len(q) > 0:
			todoRevise = q.pop[0]
		#domain filtering loop




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

	def revise(self,a,b):
		domain = []
		for i in a:
			for j in b:
				if not(i == j):
					domain.append(i)
					break
				else:
					continue
		return domain






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

g = Graph(nv,ne,ixy,neighbours, domain)

gac = GAC(g)
gac.runGAC()