import itertools


class GAC:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.domains = self.construct_domains()
        print self.domains

    def construct_domains(self):
        domains = {}
        print self.columns[0]
        print self.columns[1]
            #For every Column
        for i in range(self.columns[0]):
            print "-----------------"
            domains["c_"+str(i)] = []
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

                domains["c_"+str(i)].append(dl)
                index_addition += self.columns[1][i][x]
            self.calculate_domain(domains["c_"+str(i)])

        return domains

    def calculate_domain(self, dl):
        res = []
        for n in range(len(dl)):
            for i in range(n,len(dl[n])-n):
                for x in range (len(dl[n])-i):
                    res.append([])
                    for y in range()
                    print (dl[n][i],dl[n][x])
