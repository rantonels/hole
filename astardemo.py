import astar
from random import *

mapp = [[randint(0,10)//10 for _ in range(0,50)] for _ in range(0,50)]

def isblocked(x,y):
    global mapp

    if not (x in range(0,50) and y in range(0,50)):
        return 1
    return (mapp[x][y] != 0)

start = (randint(0,49),randint(0,49))
end = (randint(0,49),randint(0,49))

mapp[start[0]][start[1]] = 0
mapp[end[0]][end[1]] = 0

p = astar.pathfind(isblocked,start,end)

print p

l = ""

for i in range(0,50):
    for j in range(0,50):
        if (i,j) in p:
            if mapp[i][j] > 0:
                l+="E"
            else:
                l+=str(p.index((i,j))%10)
            
        elif mapp[i][j] > 0:
            l+="#"
        else:
            l+=" "
    l+="\n"
print l
