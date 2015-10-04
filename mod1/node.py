class Node(object):
    def __init__(self,position, parent):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.move_cost = 1
        self.parent = parent
        self.kids = []
        self.position = position

    #heapen sorterer etter f verdien til noden

    def __lt__(self, other):
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost
        return self.f_cost < other.f_cost
        '''
    def __cmp__(self, other):
        if other == None:
            return
        return cmp(self.f_cost, other.f_cost)
        '''
    def appendkid(self, node):
        self.kids.append(node)
