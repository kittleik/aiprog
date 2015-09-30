# module 2
# General Arc Consistency

import itertools


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

	def runGAC(self, domains):
		todoRevise = []																					#initialize queue
		for variable in self.graph.neighbors:
			for neighbor in self.graph.neighbors[str(variable)]:										#putting requests to queue
				constraint_name = (str(variable) + '_' + str(neighbor))
				if constraint_name in self.graph.constraints:
					todoRevise.append((variable, constraint_name))
		# Domain filtering loop
		while len(todoRevise) > 0:
			x, c = todoRevise.pop(0)
			result = self.revise(x, c)
			is_reduced = result[0]
			to_be_removed = result[1]
			current_domain = domains[x]

			if is_reduced:
				new_domain = self.getNewDomainValues(current_domain,to_be_removed)
				domains[x] = new_domain
				if not domains[x]:
					print "no solution"
					return (False, [])
				current_neighbors = self.getNeighborsExceptCurrent(x,c)
				for n in current_neighbors:
					constraint_name = (str(n) + '_' + str(x))
					if constraint_name in self.graph.constraints:
						todoRevise.append((n, constraint_name))
		# Check if solution is found
		if self.isFullyReduced(self.graph.nv,domains):
			print "DONE"
			return (True,[])

		else:
			print "NOT DONE YET!"
			return (True, domains)

	def isFullyReduced(self,nv,domains):
		isFullyReduced = False
		count = 0
		for key in domains:
			if len(domains[key]) != 1:
				break
			else:
				count += 1
		if nv == count:
			isFullyReduced = True
		return isFullyReduced

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
