class Graph:

	def __init__(self, ixy, edges, domain):
		self.variables = self.createVariables(ixy)
		self.domains = self.createDomains(self.variables, domain)
		self.neighbors = self.createNeighbors(self.variables,edges)

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