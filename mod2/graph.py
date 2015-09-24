class Graph:

	def __init__(self, ixy, edges, domain):
		self.variables = self.createVariables(ixy)
		self.domains = self.createDomains(self.variables, domain)
		self.neighbors = self.createNeighbors(self.variables,edges)
		self.constraints = self.createConstraints(edges)


	def createVariables(self, ixy):
		variables = {}
		for i in ixy:
			variables["n"+str(i[0])] = (i[1],i[2])
		return variables

	def createDomains(self, variables, domain):
		domains = {}
		for i in variables:
			domains[str(i)] = domain
		return domains

	def createNeighbors(self, variables, edges):
		neighbors = {}
		for var in variables:
			neighbors[var] = []
			for e in edges:
				if e[0] == int(var[1:]):
					neighbors[var].append('n' + str(e[1]))
				if e[1] == int(var[1:]):
					neighbors[var].append('n' + str(e[0]))
		return neighbors

	# In this case all constraints are the same
	def createConstraints(self,edges):
		constraints = {}
		for e in edges:
			var1 = 'n' + str(e[0])
			var2 = 'n' + str(e[1])
			func = self.makefunc(['a','b'],"a!=b")
			constraint = [[var1,var2],func]
			# Adding constraints both ways
			constraints[str(var1)+'_'+str(var2)] = constraint
			constraints[str(var2)+'_'+str(var1)] = constraint


		return constraints


	def makefunc(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names: args = args + "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)
