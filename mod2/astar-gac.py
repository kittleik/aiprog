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
		return self.reduced(x, var_names, func)


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
			todoDelete[x] = result
		res = {}
		for key in todoDelete:
			res[key] = deleteMerge(todoDelete[key],self.graph.domains[key])
		print todoDelete
		print res

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

domain = [0,2,3]
g = Graph(ixy,edges,domain)

#g.domains["n18"] = [1]
gac = GAC(g)



gac.runGAC()
'''
gac.graph.domains["n12"] = [1,2,3,5]
gac.graph.domains["n18"] = [2,4,10]
x = "n18"
constraint = "n18_n12"
a = gac.revise(x,constraint)
print a
print gac.graph.domains
'''











#combi = list(itertools.product())
