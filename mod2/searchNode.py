
class searchNode:
	def __init__(self,parent):
		self.state = []
		self.g_cost = 0
		self.h_cost = 0
		self.f_cost = 0
		self.parent = parent
		self.neighbours = []
