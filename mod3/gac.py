import itertools


class GAC:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.domains = self.construct_domains()

    def construct_domains(self):
        domains = {}

        for i in range(len(self.columns[1])):
            print self.columns[1][i]

        return domains
