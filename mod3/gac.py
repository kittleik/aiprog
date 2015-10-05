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
        #For every Column
        for i in range(self.columns[0]):
            domains["c_"+str(i)] = []
            print "c_"+str(i)
            min_tiles = len(self.columns[1][i])-1
            #getting minimum length of tiles for instructions
            for l in self.columns[1][i]:
                min_tiles += l
            print min_tiles
            #For every instruction
            '''
            for i in range(len(self.columns[1][i])):
                #For every movable spaces in the tiles
                for y in range(self.columns[0]-min_tiles):
                    #For every possible domain
                    for x in range(len(self.columns[1][i])-y):
                        domain =
                        domains["c_"+str(i)].append(domain)
                        '''

        return domains
