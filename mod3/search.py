
import heapq, Queue


class Node(object):
    def __init__(self,state, parent):
        self.state = state
        self.f_cost = self.computeHeuristic(state)
        self.parent = parent
        self.kids = []

    def __cmp__(self, other):
        return cmp(self.f_cost, other.f_cost)

    def appendkid(self, node):
        self.kids.append(node)

    def computeHeuristic(self, domains):
        result = 0
        for domain in domains:
            result += (len(domains[domain]) - 1)
        return result

    def generateSuccerssors(self,  parent, search):
        successors = []
        solution = False
        domains = parent.state
        assumption_choice = 0

        x = 100
        for node in domains:
            if 1 < len(domains[node]) < x:
                assumption_choice= node
                x = len(domains[node])
                if x == 2:
                    break

        search.assumtions +=1

        for c in domains[assumption_choice]:
            domains[assumption_choice] = [c]
            successor = search.gac.domainFilteringLoop(domains, assumption_choice)
            # Returnerer (Bool, {newDomains})
            print successor[1]
            if successor[0]:
                solution = Node(successor[1],parent)
                #break
            #legger til alle barn
            print successor[1]
            print parent.state
            if not successor[1] == {}:
                successors.append(Node(successor[1],parent))

    #for k in domains:
        #for d in domains[k]:
        return solution, successors

class Search(object):

    def __init__(self, gac):
        self.openlist = []
        heapq.heapify(self.openlist)
        self.closedlist = []
        self.states = {}
        self.assumtions = 0
        self.gac = gac
        #incremental variables
        self.incrementalOpenlist = []

        self.incremental = False

    def makeStringFromList(self, list):
        result = ""
        for i in list:
            result += str(i)
        return result


    def generateUID(self,domains):
        uid = ""
        for key in domains:
            uid += (key + self.makeStringFromList(domains[key]))
        return uid

    def a_star(self):
        # creating initial node
        # Setter opp forste node og dens state
        domains = self.gac.domains
        # Kjorer gac med full domains
        self.gac.runGAC(domains, assumed=None)
        node = Node(domains,None)
        heapq.heappush(self.openlist, node)

        #AGENDA LOOP
        while True:
            if len(self.openlist) == 0:
                print "openlist is empty, no solution"
                return
            node = heapq.heappop(self.openlist)
            print len(self.openlist)
            print "hei"
            solution, successors = node.generateSuccerssors(node, self)
            #print successors

            if solution:
                print solution.state
                print "THIS IS THE FUCKING SOPULTIONB!!!!!!!!3<3<3<3<3"
                print self.assumtions
                return solution

            for suc in successors:

                heapq.heappush(self.openlist, suc)

    def incremental_a_star(self):

        if not self.incremental:

            heapq.heapify(self.incrementalOpenlist)
            self.incremental = True

            domains = self.gac.graph.domains
            self.gac.runGAC(domains, assumed=None)
            node = Node(domains,None)
            heapq.heappush(self.incrementalOpenlist, node)

            return node

        if not self.incrementalOpenlist:
            self.incremental = False
            return False

        node = heapq.heappop(self.incrementalOpenlist)
        solution, successors = node.generateSuccerssors(node, self)

        if solution:
            print solution.state
            print "THIS IS THE FUCKING SOPULTIONB!!!!!!!!3<3<3<3<3"
            print self.assumtions
            self.resetIncremental()
            return solution

        for suc in successors:

            heapq.heappush(self.incrementalOpenlist, suc)
        return node

    def resetIncremental(self):
        self.incrementalOpenlist = []
        self.incremental = False
