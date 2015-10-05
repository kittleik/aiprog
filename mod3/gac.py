import itertools
import copy


class GAC:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.domains = self.construct_domains()
        for i in self.domains:
            print self.domains[i]

    def construct_domains(self):
        domains = {}
        domains_block_index = {}
        print self.columns[0]
        print self.columns[1]
            #For every Column
        for i in range(self.columns[0]):
            print "-----------------"
            domains["c_"+str(i)] = []
            domains_block_index["c_"+str(i)] = []
            temp_domains = []
            print "c_"+str(i)
            min_tiles = len(self.columns[1][i])-1
            #getting minimum length of tiles for instructions
            index_addition = 0
            for l in self.columns[1][i]:
                min_tiles += l
                #For every instruction
            for x in range(len(self.columns[1][i])):
                dl = []
                y = 0
                for y in range(self.columns[0]-min_tiles+1):

                    dl.append(y+index_addition)
                    y+=1
                    #For every valid spot
                    #for y in range (self.columns[0]-min_tiles+1)

                temp_domains.append(dl)
                index_addition += self.columns[1][i][x] + 1

            temp_domains = self.getAllPairs(temp_domains)
            domains_block_index["c_"+str(i)] = self.simpleDomainFiltering(temp_domains)

            for q in range(len(domains_block_index["c_"+str(i)])):
                domains["c_"+str(i)].append(self.setDomain(domains_block_index["c_"+str(i)][q], self.columns[1][q]))


        return domains

    def setDomain(self, block_pos, block_size):
        print block_pos
        domain = ['_']*self.columns[0]
        for i in range(len(block_size)):
            for x in range(block_size[i]):
                domain[block_pos[i]+x] = '#'

        return domain
                #if self.checkConstraint(i[])
                #return
    def simpleDomainFiltering(self,d_list):
        ret_list = copy.copy(d_list)
        for a in range(len(d_list)):
            counter = 0
            #print temp_domains[a]
            for b in range(len(d_list[a])-1):
                if not self.checkConstraint(d_list[a][b],d_list[a][b+1]):
                    ret_list.pop(a-counter)
                    counter += 1
        return ret_list

    def getAllPairs(self, current_domains):
        all_pairs=[]
        for n in itertools.product(*current_domains):
            all_pairs.append(list(n))
        return all_pairs

    def checkConstraint(self, x,y):
        if x+1 < y:
             return True
        return False

    def createConstraints(self,edges):
		constraints = {}
		for e in edges:
			var1 = 'n' + str(e[0])
			var2 = 'n' + str(e[1])
			func = self.makefunc(['a','b'],"a+1<b")
			constraint = [[var1,var2],func]
			# Adding constraints both ways
			constraints[str(var1)+'_'+str(var2)] = constraint
			constraints[str(var2)+'_'+str(var1)] = constraint


		return constraints
