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
            domains["c_"+str(i)] = 0
            print "c_"+str(i)
            min_tiles = len(self.columns[1][i])-1
            #getting minimum length of tiles for instructions
            print self.columns[1][i]
            for l in self.columns[1][i]:
                min_tiles += l
            print min_tiles
            #For every instruction
            for z in range(len(self.columns[1][i])):
                #For every movable spaces in the tiles
                for y in range(self.columns[0]-min_tiles):
                    #For every possible d
                    for x in range(len(self.columns[1][i])):
                        domains["c_"+str(i)] = int(domains["c_"+str(i)])+1
                        print (i,z,y,x)
                        print "column number " + str(i)
                        print "instruction number " +str(z)
                        print "open space " + str(y)
                        print "asd"

        return domains
