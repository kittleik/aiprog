import itertools
import copy


class GAC:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        #self.domains = self.construct_domains(self.columns)
        self.domains_rows = self.construct_domains(self.rows,"r")
        self.domains_columns = self.construct_domains(self.rows,"c")

        self.constraints = self.createConstraints(self.domains_rows, self.domains_columns)

        self.neighbors = self.generateNeighbors(self.domains_rows,self.domains_columns)
        self.domains = self.domains_rows.copy()
        self.domains.update(self.domains_columns)

        self.todoRevise = []

        print self.runGAC(self.domains, assumed=None)

    def generateNeighbors(self, rows, columns):
        result = {}
        rl = []
        cl = []
        for r in rows:
            rl.append(r)
        for c in columns:
            cl.append(c)
        for r in rows:
            result[r] = cl
        for c in columns:
            result[c] = rl
        return result


    def get_todo_revise(self,rows,columns):
        todoRevise = []
        for row in rows:
            for column in columns:
                todoRevise.append((row ,row+'_'+column))
                todoRevise.append((column ,column+'_'+row))
        return todoRevise

    def runGAC(self, domains, assumed):

		self.todoRevise = self.get_todo_revise(self.domains_rows, self.domains_columns)
		# Domain filtering loop
		result = self.domainFilteringLoop(domains, assumed)
		return result

    def domainFilteringLoop(self, domains, assumed):
		reducedDomains = dict(domains)
		todoRevise = []
		if assumed:
			for revise in self.todoRevise:
				string = revise[1]
				index = string.index('_')
				if string[index+1:] == assumed:
					todoRevise.append(revise)
		else:
			todoRevise = list(self.todoRevise)

		while len(todoRevise) > 0:
			x, c = todoRevise.pop(0)
			result = self.revise(x, c, reducedDomains)
			is_reduced = result[0]
			to_be_removed = result[1]
			current_domain = reducedDomains[x]

			if is_reduced:

				new_domain = self.getNewDomainValues(current_domain,to_be_removed)
				reducedDomains[x] = new_domain
				if not reducedDomains[x]:
					print "no solution"
					return (False, {})
				current_neighbors = self.getNeighborsExceptCurrent(x,c)
				for n in current_neighbors:
					constraint_name = (str(n) + '_' + str(x))
					if constraint_name in self.constraints:
						todoRevise.append((n, constraint_name))
		# Check if solution is found
		if self.isFullyReduced(self.rows[0]+self.columns[0],reducedDomains):
			print "DONE"
			# domains is the answer
			return (True,reducedDomains)

		else:
			return (False,reducedDomains)

    def getNeighborsExceptCurrent(self,var,constraint):
		current_variables = self.constraints[constraint][0]
		neighbors = self.neighbors[var]
		for v in current_variables:
			if v in neighbors:
				neighbors.remove(v)

		return neighbors

    def revise(self, x, c, domains):
		constraint = self.constraints[c]
		var_names = constraint[0]
		func = constraint[1]
		result = self.reduced(x, var_names, func, domains)
		reduced = False
		for r in result:
			if r == False:
				reduced = True
				break
		return (reduced,result)

    def reduced(self, x, var_names, func, domains):
		domX = domains[x]
		reduced = [False]*len(domX)
		all_pairs = self.getAllPairs(var_names,domains)
		focal_index = self.getFocalIndex(x, var_names)
		for i in range(len(domX)):
			for p in all_pairs:
				if p[focal_index] == domX[i]:
					if apply(func,p):
						reduced[i] = True
		return reduced

    def getFocalIndex(self,x ,var_names):
		for i in range(len(var_names)):
			if var_names[i] == x:
				index = i
				break

		return index

    def getNewDomainValues(self,domain,removes):
		newdom = []
		for r in range(len(removes)):
			if removes[r]:
				d_value = domain[r]
				newdom.append(d_value)
		return newdom


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


    def createConstraints(self, rows, columns):
        constraints = {}
        for r in rows:
            for c in columns:
                var1 = str(r)
                var2 = str(c)
                lr = str(r)[1:]
                lc = str(c)[1:]
                func = self.makefunc(["a","b"],"a["+lc+"]==b["+lr+"]")
                constraint = [[var1,var2],func]
                constraints[var1+'_'+var2] = constraint
                constraints[var2+'_'+var1] = constraint
        return constraints




    def makefunc(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names: args = args + "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

    def construct_domains(self, variable, type_str):

          domains = {}
          domains_block_index = {}
              #For every Column
          for i in range(variable[0]):

              domains[type_str+str(i)] = []
              domains_block_index[type_str+str(i)] = []
              temp_domains = []
              min_tiles = len(variable[1][i])-1
              #getting minimum length of tiles for instructions
              index_addition = 0
              for l in variable[1][i]:
                  min_tiles += l
                  #For every instruction
              for x in range(len(variable[1][i])):
                  dl = []
                  y = 0
                  for y in range(variable[0]-min_tiles+1):

                      dl.append(y+index_addition)
                      y+=1
                      #For every valid spot
                      #for y in range (variable[0]-min_tiles+1)

                  temp_domains.append(dl)
                  index_addition += variable[1][i][x] + 1
              temp_domains = self.getAllPairsInit(temp_domains)
              domains_block_index[type_str+str(i)] = self.simpleDomainFiltering(temp_domains)
              #print self.setDomain(domains_block_index[type_str+str(i)][0], variable[1][0])
              for q in range(len(domains_block_index[type_str+str(i)])):

                  domains[type_str+str(i)].append(self.setDomain(domains_block_index[type_str+str(i)][q], variable[1][i],variable[0]))


          return domains

    def setDomain(self, block_pos, block_size,variable):

        domain = ['_']*variable

        for i in range(len(block_pos)):
            for x in range(block_size[i]):
                domain[block_pos[i]+x] = '#'
        return domain
                #if self.checkConstraint(i[])
                #return
    def simpleDomainFiltering(self,d_list):
        ret_list = copy.copy(d_list)
        counter = 0
        for a in range(len(d_list)):

            #print temp_domains[a]
            for b in range(len(d_list[a])-1):
                if not self.checkConstraint(d_list[a][b],d_list[a][b+1]):
                    ret_list.pop(a-counter)
                    counter += 1
        return ret_list

    def getAllPairs(self, var_names, domains):
		all_pairs = []
		current_domains = []
		for v in var_names:
			current_domains.append(domains[v])
		for n in itertools.product(*current_domains):
			all_pairs.append(list(n))
		return all_pairs

    def getAllPairsInit(self, current_domains):
        all_pairs=[]
        for n in itertools.product(*current_domains):
            all_pairs.append(list(n))
        return all_pairs

    def checkConstraint(self, x,y):
        if x+1 < y:
            return True
        return False
