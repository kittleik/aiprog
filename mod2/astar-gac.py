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
		constraint = self.graph.constraints[c]
		var_names = constraint[0]
		func = constraint[1]
		result = self.reduced(x, var_names, func)
		reduced = False
		for r in result:
			if r == False:
				reduced = True
				break
		return (reduced,result)


	def reduced(self, x, var_names, func):
		reduced = [False]*len(self.graph.domains[x])
		all_pairs = self.getAllPairs(var_names)
		focal_index = self.getFocalIndex(x, var_names)

		domX = self.graph.domains[x]

		for i in range(len(domX)):
			for p in all_pairs:
				if p[focal_index] == domX[i]:
					if apply(func,p):
						reduced[i] = True
		return reduced																					#returns a list of Bool [True,False] which represents
																										#domain values being reduced of not, False means reduced
																										#because the constraint did not match any values of dom(x)
	def getFocalIndex(self,x ,var_names):
		for i in range(len(var_names)):
			if var_names[i] == x:
				index = i
				break

		return index

	def getNeighborsExceptCurrent(self,var,constraint):
		current_variables = self.graph.constraints[constraint][0]
		neighbors = self.graph.neighbors[var]
		for v in current_variables:
			if v in neighbors:
				neighbors.remove(v)

		return neighbors

	def runGAC(self):
		todoRevise = []																					#initialize queue
		todoDelete = {}
		for variable in self.graph.neighbors:
			for neighbor in self.graph.neighbors[str(variable)]:										#putting requests to queue
				constraint_name = (str(variable) + '_' + str(neighbor))
				if constraint_name in self.graph.constraints:
					todoRevise.append((variable, constraint_name))

		while len(todoRevise) > 0:
			x, c = todoRevise.pop(0)
			result = self.revise(x, c)
			is_reduced = result[0]
			to_be_removed = result[1]
			current_domain = self.graph.domains[x]

			if is_reduced:
				new_domain = self.getNewDomainValues(current_domain,to_be_removed)
				self.graph.domains[x] = new_domain
				current_neighbors = self.getNeighborsExceptCurrent(x,c)

				for n in current_neighbors:
					constraint_name = (str(n) + '_' + str(x))
					if constraint_name in self.graph.constraints:
						todoRevise.append((n, constraint_name))


	def getNewDomainValues(self,domain,removes):
		newdom = []
		for r in range(len(removes)):
			if removes[r]:
				d_value = domain[r]
				newdom.append(d_value)
		return newdom

	def makefunc(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names: args = args + "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)


	def reRun(self):
		return True

def deleteMerge(lista, listb):
	res = []
	for a in range(len(lista)):
		if lista[a]:
			res.append(listb[a])
	return res


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
g = Graph(ixy,edges,domain)

g.domains["n18"] = [1]
g.domains["n12"] = [2]
g.domains["n11"] = [3]
g.domains["n10"] = [4]
g.domains["n15"] = [5]
g.domains["n13"] = [0]
g.domains["n13"] = [1]
g.domains["n2"] = [1]

gac = GAC(g)

#print "----neighbors-----"
#print gac.graph.neighbors


gac.runGAC()
print gac.graph.domains





#combi = list(itertools.product())
