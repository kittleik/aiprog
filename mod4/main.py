from visuals import GameWindow
from board import Board
import time

window = GameWindow()


b = Board()
#b.checkNeighbour("up")
#print "columns: " + str(b.getColumns())
#print "rows: " + str(b.getRows())
print b.grid
g1 = b.swipeUp(b.grid)
b.upAddition(b.grid)
window.update_view( b.generateState(g1) )
#g2 = b.swipeDown(b.grid)
#b.downAddition(b.grid)
#window.update_view( b.generateState(g2) )
print g1
#print g2

window.update_view( b.generateState(b.grid) )

window.mainloop()
