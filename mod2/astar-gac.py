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

	def getAllPairs(self, var_names):
		all_pairs = []
		domains = []
		for v in var_names:
			domains.append(self.graph.domains[v])
		for n in itertools.product(*domains):
			all_pairs.append(list(n))
		return all_pairs

	def getDomain(self,var):
		return self.graph.domains[var]

	def revise(self, x, c):
		focal = x
		constraint = self.graph.constraints[c]
		var_names = constraint[0]
		func = constraint[1]
		return self.reduced(focal, var_names, func)


	def reduced(self, x, var_names, func):
		reduced = [False]*len(self.graph.domains[x])
		all_pairs = self.getAllPairs(var_names)
		domX = self.graph.domains[x]
		for i in range(len(domX)):
			for p in all_pairs:
				if p[0] == domX[i]:
					if apply(func,p):
						#eg. a>b satisfied
						reduced[i] = True
		return reduced																					#returns a list of Bool [True,False] which represents
																										#domain values being reduced of not, False means reduced
																										#because the constraint did not match any values of dom(x)

	def runGAC(self):
		todoRevise = []																					#initialize queue
		for variable in self.graph.neighbors:
			for neighbor in self.graph.neighbors[str(variable)]:										#putting requests to queue
				constraint_name = (str(variable) + '_' + str(neighbor))
				if constraint_name in self.graph.constraints:
					todoRevise.append((variable, constraint_name))

		while len(todoRevise) > 0:
			x, c = todoRevise.pop(0)
			result = self.revise(x, c)
			removed_count = 0
			for i in range(len(result)):
				if result[i] == False:
					a = self.graph.domains[x].pop(i-removed_count)
					removed_count += 1
					neighbors = self.graph.neighbors[x]
		print self.graph.domains

	def makefunc(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names: args = args + "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)


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

domain = [1,2,3]
g = Graph(ixy,edges,domain)
g.domains["n12"] = [1]

#g.domains["n18"] = [1]
gac = GAC(g)
gac.runGAC()
print g.neighbors






'''
g.domains["n12"] = [1]
g.domains["n18"] = [1]
func = g.constraints["n12_n18"][1]
x = "n12"
var_names = g.constraints["n12_n18"][0]

print gac.reduced(x,var_names,func)



'''



#combi = list(itertools.product())
