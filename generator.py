def putroom(l,x,y,w,h):
	for i in range(y+1,y+h-1):
		l[x][i] = 1
		l[x+w-1][i] = 1
	for i in range(x,x+w):
		l[i][y] = 1
		l[i][y+h-1] = 1
	for i in range(x+1,x+w-1):
		for j in range(y+1,y+h-1):
			l[i][j] = 0

	
def generatelvl(W,H):
	m = [[2 for i in range(0,W)] for j in range(0,H)]

	putroom(m,10,10,12,8)
	

	return m

''' lvl = generatelvl(60,60)

s=""
for i in range(0,60):
	for j in range(0,60):
		c= lvl[j][i]
		if c == 0:
			s = s+" "
		if c == 1:
			s = s+"#"
		if c == 2:
			s = s+"."
	s=s+'\n'

print s *}
'''

from dMap import *
startx=60
starty=60
somename= dMap()
somename.makeMap(startx,starty,110,15,5,60) 
#somename.makeLava(60,60,0.4,0)
for y in range(starty):
        line = ""
        for x in range(startx):
                if somename.mapArr[y][x]==0:
                        line += " "
                elif somename.mapArr[y][x]==1:
                        line += "."
                elif somename.mapArr[y][x]==2:
                        line += "#"
                elif somename.mapArr[y][x]==3 :#or somename.mapArr[y][x]==4 or somename.mapArr[y][x]==5:
                        line += "="
		elif somename.mapArr[y][x]==99:
			line += "H"
		elif somename.mapArr[y][x]==98:
			line += "D"
		else:
			line += "?"
			
        print line

'''for y in range(starty):
        line = ""
        for x in range(startx):
                if somename.lavaArr[y][x]==0:
                        line += " "
                elif somename.lavaArr[y][x]==1:
                        line += "."
                elif somename.lavaArr[y][x]==2:
                        line += "#"
                elif somename.lavaArr[y][x]==3 :#or somename.lavaArr[y][x]==4 or somename.lavaArr[y][x]==5:
                        line += "="
		elif somename.lavaArr[y][x]==99:
			line += "H"
		elif somename.lavaArr[y][x]==98:
			line += "D"
		else:
			line += "?"
			
        print line

'''
