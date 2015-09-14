#module 2

# Graph coloring with A*

import sys
import re

inFile = sys.argv[1]

class Vertex:
	def __init__(self, ixy, neighbours):
		self.index = ixy[0]
		self.x = ixy[1]
		self.y = ixy[2]
		self.neighbours = neighbours

class Graph:
    def __init__(self, nv, ne, vertices, edges):
        self.nv = nv
        self.ne = ne
        self.vertices = []
        self.indices = set()
        for v in vertices:
            vertex = Vertex(v, [])
            self.vertices.append(vertex)
            self.indices.add(v[0])

        for e in edges:
        	e1 = e[0]
        	e2 = e[1]
        	if e1 in self.indices:
        		self.vertices[e1].neighbours.append(e)
        	if e2 in self.indices:
        		self.vertices[e2].neighbours.append(e)





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

g = Graph(nv,ne,ixy,neighbours)