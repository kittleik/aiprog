import copy
liste = [[0,2,3,4],[1,2,3,4],[1,2,3,4],[0,0,0,0]]

list1 = copy.deepcopy(liste)

for x in range(0,4):
    for y in range(0,4):
        if list1[x][y] == 0:
            list1[x][y] = 1
print liste
print list1
