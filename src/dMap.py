# Class to produce random map layouts
from random import *
from math import *

wedidit=True


# N is the set of nodes {a,b,c..}
# A is the set of arcs with costs {(a,b,1),(a,c,2)..}
#
# Use: Kruskal (N,A)

def find (u, C):
  i = 0
  for c in C:
    if (u in c): return (c,i)
    i += 1
  
def merge (C, ucomp, vcomp):
  return [ucomp[0] + vcomp[0]] + [i for j, i in enumerate(C) if j not in [ucomp[1], vcomp[1]]]


def Kruskal (N, A):
  A = sorted(A, key= lambda A: A[2])
  C = [[u] for u in N]
  T = []
  n = len(N)
  for shortestA in A:
    u, v = shortestA[0], shortestA[1]
    ucomp, vcomp = find(u, C), find(v, C)
    if (ucomp != vcomp):
      C = merge (C, ucomp, vcomp)
      T.append((u,v))
      if (len(T) == (n-1)): break
      
  return T



class dMap:
   def __init__(self):
       self.roomList=[]
       self.cList=[]

   def makeCave(self,w,l,openings):
    self.caveArr = [[55 for _ in range(l)] for _ in range(w)]
    (cx,cy) = (randint(1,w-2),randint(1,l-2))

    self.caveArr[cx][cy] = 0
    for o in openings:
        sx = (cx>o[0])*2 - 1        
        sy = (cy>o[1])*2 - 1

        moves = [0 for _ in range(abs(cx-o[0]))] + [1 for _ in range(abs(cy-o[1]))]
        shuffle(moves)
        x = o[0]
        y = o[1]
        for m in moves:
            self.caveArr[x][y] = 0
            if m == 0:
                x+=sx
            if m == 1:
                y+=sy
        self.caveArr[o[0]][o[1]] = 0


    for t in range(10):
        x = cx
        y = cy
    
        for c in range(0,15):
            if randint(0,1)==0:
                x+=randint(-1,1)
            else:
                y+=randint(-1,1)
            if (not x in range(1,w-1)) or (not y in range(1,l-1)):
                break
            self.caveArr[x][y] = 0
        
    

   def makeMap(self,xsize,ysize,fail,b1,b2,mrooms):
       global wedidit
       wedidit = True
       """Generate random layout of rooms, corridors and other features"""
       #makeMap can be modified to accept arguments for values of failed, and percentile of features.
       #Create first room
       self.mapArr=[[1 for y in range(ysize)] for x in range(xsize)]
       w,l,t=self.makeRoom()
       while len(self.roomList)==0:
           y=randrange(ysize-1-l)+1
           x=randrange(xsize-1-w)+1
           p=self.placeRoom(l,w,x,y,xsize,ysize,6,0)
       failed=0
       while failed<fail: #The lower the value that failed< , the smaller the dungeon
            chooseRoom=randrange(len(self.roomList))
            ex,ey,ex2,ey2,et=self.makeExit(chooseRoom)
            feature=randrange(100)
            if feature<b2:
                 w,l,t=self.makeTemple()
            elif feature<b1: #Begin feature choosing (more features to be added here)
               w,l,t=self.makeCorridor()
            elif feature<b1+5:
                w,l,t=self.makeHall()
            else:
                w,l,t=self.makeRoom()
            roomDone=self.placeRoom(l,w,ex2,ey2,xsize,ysize,t,et)
            if roomDone==0: #If placement failed increase possibility map is full
               failed+=1
            elif roomDone==2: #Possiblilty of linking rooms
               if self.mapArr[ey2][ex2]==0:
                   if randrange(100)<7:
                       self.makePortal(ex,ey)
                   failed+=1
            else: #Otherwise, link up the 2 rooms
               self.makePortal(ex,ey)
               failed=0
               if t<5:
                   tc=[len(self.roomList)-1,ex2,ey2,t]
                   self.cList.append(tc)
                   self.joinCorridor(len(self.roomList)-1,ex2,ey2,t,50)
            if len(self.roomList)==mrooms:
               failed=fail
       self.finalJoins()

       self.adjustTemple()

       toclean=[]
       for i in range(0,xsize):
        for j in range(0,ysize):
            if self.mapArr[j][i] == 55:
                clean = True
                gg = [ (x,y) for x in [i-1,i,i+1] for y in [j-1,j,j+1] ]
                for g in gg:
                    if (not g[0] in range(0,xsize)) or (not g[1] in range(0,ysize)):
                        continue
                    if self.mapArr[g[1]][g[0]] in [0]:
                        clean = False
                if clean:
                    toclean.append((i,j))
       for t in toclean:
        self.mapArr[t[1]][t[0]] = 1

       return wedidit

   def makeRoom(self):
       """Randomly produce room size"""
       rtype=5
       if randint(0,4) == 0:
        rwide = 20
        rlong = 20
       else:
            rwide=randrange(8)+3
            rlong=randrange(8)+3
       return rwide,rlong,rtype

   def makeHall(self):
    rtype=6
    rwide=11+randrange(3)
    rlong=11+randrange(3)
    return rwide,rlong,rtype   

   def makeTemple(self):
    rtype=100
    saas=randrange(3)+5
    rwide=saas
    rlong=saas
    return rwide,rlong,rtype

   def makeCorridor(self):
       """Randomly produce corridor length and heading"""
       clength=randrange(18)+3
       heading=randrange(4)
       if heading==0: #North
           wd=1
           lg=-clength
       elif heading==1: #East
           wd=clength
           lg=1
       elif heading==2: #South
           wd=1
           lg=clength
       elif heading==3: #West
           wd=-clength
           lg=1
       return wd,lg,heading
   def placeRoom(self,ll,ww,xposs,yposs,xsize,ysize,rty,ext):
       """Place feature if enough space and return canPlace as true or false"""
       #Arrange for heading
       xpos=xposs
       ypos=yposs
       if ll<0:
           ypos+=ll+1
           ll=abs(ll)
       if ww<0:
           xpos+=ww+1
           ww=abs(ww)
       #Make offset if type is room
       if rty in [5,6,100]:
           if ext==0 or ext==2:
               offset=randrange(ww)
               xpos-=offset
           else:
               offset=randrange(ll)
               ypos-=offset
       #Then check if there is space
       canPlace=1
       if ww+xpos+1>xsize-1 or ll+ypos+1>ysize:
           canPlace=0
           return canPlace
       elif xpos<1 or ypos<1:
           canPlace=0
           return canPlace
       else:
           for j in range(ll):
               for k in range(ww):
                   if self.mapArr[(ypos)+j][(xpos)+k]!=1:
                       canPlace=2
       #If there is space, add to list of rooms
       if canPlace==1:
           temp=[ll,ww,xpos,ypos,rty]
           self.roomList.append(temp)

           walltype = 2
           if rty == 100:
                walltype = 99
           dragon = 98

           for j in range(ll+2): #Then build walls
               for k in range(ww+2):
                   self.mapArr[(ypos-1)+j][(xpos-1)+k]=walltype
           for j in range(ll): #Then build floor
               for k in range(ww):
                   self.mapArr[ypos+j][xpos+k]=0
                   if (rty == 6) and ((ww>8) and (ll>8)) and ((j-ll//2)**2 + (k-ww//2)**2 < 4): #add middle column
                            self.mapArr[ypos+j][xpos+k]=walltype
           if (rty in [5,6]) and randint(0,1) > 0 and ww>9 and ll>9:
            for s in [[xpos+1,ypos+1] , [xpos+1,ypos+ll-2] , [xpos+ww-2,ypos+ll-2] , [xpos+ww-2,ypos+1]]:
                self.mapArr[s[1]][s[0]] = walltype
  
           if(rty == 100):
                self.mapArr[ypos+ll//2-1][xpos+ww//2-1]= dragon

    
       return canPlace #Return whether placed is true/false
   def makeExit(self,rn):
       global wedidit
       """Pick random wall and random point along that wall"""
       room=self.roomList[rn]
       safecount=0
       while safecount < 300:
           rw=randrange(4)
           if rw==0: #North wall
               rx=randrange(room[1])+room[2]
               ry=room[3]-1
               rx2=rx
               ry2=ry-1
           elif rw==1: #East wall
               ry=randrange(room[0])+room[3]
               rx=room[2]+room[1]
               rx2=rx+1
               ry2=ry
           elif rw==2: #South wall
               rx=randrange(room[1])+room[2]
               ry=room[3]+room[0]
               rx2=rx
               ry2=ry+1
           elif rw==3: #West wall
               ry=randrange(room[0])+room[3]
               rx=room[2]-1
               rx2=rx-1
               ry2=ry
           if self.mapArr[ry][rx] in [2,99]: #If space is a wall, exit
               break
           safecount +=1
       if safecount >= 3000:
         wedidit = (wedidit) and False
       return rx,ry,rx2,ry2,rw
   def makePortal(self,px,py):
       """Create doors in walls"""
       ptype=randrange(100)
       if ptype>100: #Secret door
           self.mapArr[py][px]=5
           return
       elif ptype>100: #Closed door
           self.mapArr[py][px]=4
           return
       elif ptype>10: #Open door
           self.mapArr[py][px]=3
           return
       else: #Hole in the wall
           self.mapArr[py][px]=0
   def joinCorridor(self,cno,xp,yp,ed,psb):
       """Check corridor endpoint and make an exit if it links to another room"""
       cArea=self.roomList[cno]
       if xp!=cArea[2] or yp!=cArea[3]: #Find the corridor endpoint
           endx=xp-(cArea[1]-1)
           endy=yp-(cArea[0]-1)
       else:
           endx=xp+(cArea[1]-1)
           endy=yp+(cArea[0]-1)
       checkExit=[]
       if ed==0: #North corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
       elif ed==1: #East corridor
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       elif ed==2: #South corridor
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
       elif ed==3: #West corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       for xxx,yyy,xxx1,yyy1 in checkExit: #Loop through possible exits
           if self.mapArr[yyy][xxx]==0: #If joins to a room
               if randrange(100)<psb: #Possibility of linking rooms
                   self.makePortal(xxx1,yyy1)
   def finalJoins(self):
       """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
       for x in self.cList:
           self.joinCorridor(x[0],x[1],x[2],x[3],10)
   def adjustTemple(self):
    for r in self.roomList:
        (ll,ww,xpos,ypos,t) = r
        if t == 100:
            for j in range(ll+2): 
                    for k in range(ww+2):
                        if self.mapArr[(ypos-1)+j][(xpos-1)+k]==2:
                            self.mapArr[(ypos-1)+j][(xpos-1)+k]=99
            for j in range(ll+2):
                    for k in [0,ww+1]:
                        if self.mapArr[(ypos-1)+j][xpos-1+k] == 1:
                            self.mapArr[(ypos-1)+j][xpos-1+k] = 99
                            if self.mapArr[(ypos-1)+j][(xpos-1)+k] == 0:
                                self.mapArr[(ypos-1)+j][(xpos-1)+k]=3
            for k in range(ww+2):
                    for j in [0,ll+1]:
                        if self.mapArr[(ypos-1)+j][(xpos-1)+k] == 0:
                            self.mapArr[(ypos-1)+j][(xpos-1)+k]=3

        if t == 5 and randint(0,1)==0   and ll>7 and ww > 7:
            ops = []
            doors = [3,4,5]
            for j in range(ll+2):
                    for k in [0,ww+1]:
                            if self.mapArr[(ypos-1)+j][(xpos-1)+k] in doors:
                                ops.append([k,j])
            for k in range(ww+2):
                    for j in [0,ll+1]:
                        if self.mapArr[(ypos-1)+j][(xpos-1)+k] in doors:
                            ops.append([k,j])
 
            self.makeCave(ww+2,ll+2,ops)


            for j in range(ll+2):
                for k in range(ww+2):
            #       if not self.caveArr[k][j] == 1 :                
                    self.mapArr[ypos-1+j][xpos-1+k] = self.caveArr[k][j]


   def makeLava(self,xsize,ysize,amt,iters):
        self.lavaArr = [[int(random() < amt) for i in range(0,ysize)] for j in range(0,xsize)]
        self.tempArr = [[self.lavaArr[i][j] for i in range(0,ysize)] for j in range(0,xsize)]
        for i in range(0,1):
            for x in range(0,xsize):
                if x == 0 or x == xsize-1:
                    for y in range(0,ysize):
                        self.tempArr[y][x] = 0
                else:
                    for y in range(0,ysize):
                        if y== 0 or y == ysize-1:
                            self.tempArr[y][x] = 0
                        else:
#                           s = sum([self.lavaArr[ups][x-1:x+2] for ups in range(y-1,y+2)]) - self.lavaArr[y][x]
                            s = self.lavaArr[y-1][x-1] + self.lavaArr[y-1][x] + self.lavaArr[y-1][x+1] + self.lavaArr[y][x-1] + self.lavaArr[y][x+1] + self.lavaArr[y+1][x-1] + self.lavaArr[y+1][x] + self.lavaArr[y+1][x+1]

                            if self.lavaArr[y][x] == 0:
                                if s>5:
                                    self.tempArr[y][x] = 1
                                else:
                                    self.tempArr[y][x] = 0
                            else:
                                if s>4:
                                    self.tempArr[y][x] = 1
                                else:
                                    self.tempArr[y][x] = 0
            
            for x in range(0,xsize):
                for y in range(0,ysize):
                    self.lavaArr[y][x] = self.tempArr[y][x]

   def gayLava(self,xsize,ysize,thresh,balls,rad):
    #place metaballs
    mb = []
    for c in range(0,balls):
        mb.append(  ( randint(0,xsize-1)  ,  randint(0,ysize-1)   )   )

    self.lavaArr = [[0]*ysize for _ in range(xsize) ]

    for x in range(0,xsize):
        for y in range(0,ysize):
            value = float(randint(-10,10))//100
            for m in mb:
                rq = (x-m[0])**2 + (y-m[1])**2 
                if rq < rad**2:
                        value += (1 - float(rq)//float(rad**2))**2
        #   print value
            if value > thresh:
                self.lavaArr[y][x] = 1
            else:
                self.lavaArr[y][x] = 0
    

   def drawranline(self,x1,y1,x2,y2):

        if x1<0 or x1>=len(self.caveArr) or x2<0 or x2>=len(self.caveArr):
            return
        sx = (x1>x2)*2 - 1        
        sy = (y1>y2)*2 - 1

        status = 0 
        #0: in room 1
        #1: in room 1 wall
        #2: in transit
        #3: in room 2 wall
        #4: in room 2

        moves = [0 for _ in range(abs(x1-x2))] + [1 for _ in range(abs(y1-y2))]
        shuffle(moves)
        x = x2
        y = y2
        px = x
        py = y
        for m in moves:

            if self.caveArr[x][y] == 2:
                self.caveArr[x][y] = 3
            else:
                self.caveArr[x][y] = 0

                


            #move
            px = x
            py = y
            if m == 0:
                x+=sx
            if m == 1:
                y+=sy
        self.caveArr[x1][y1] = 0


   def dropNode(self,x,y,r):
    if r<1 and randint(0,3)==0:
        for c in range(0,50):
            if randint(0,1)==0:
                x+=randint(0,1)*2-1
            else:
                y+=randint(0,1)*2-1
            if (not x in range(1,len(self.caveArr)-1)) or (not y in range(1,len(self.caveArr[0])-1)):
                break
            self.caveArr[x][y] = 0
        return
                
    if r<1 or x<r+2 or x>len(self.caveArr)-r-2 or y<r+2 or y>len(self.caveArr[0])-r-2:
        return
    for i in range(int(x-r-1),int(x+r+2)):
        for j in range(int(y-r-1),int(y+r+2)):
            if (i-x)**2 + (j-y)**2 < r**2+1:
                self.caveArr[i][j] = 0
    for i in range(0,1+int(r)):
        theta = float(randint(0,1000))/1000 * 2 * pi
        nx = x + int(cos(theta) * r * 1)
        ny = y + int(sin(theta) * r * 1)
        self.dropNode(nx,ny,uniform(0,r*.4))

    for i in range(0,randint(int(r//3),int(r//2))):
            (px,py) = (randint(1,len(self.caveArr)-2),randint(1,len(self.caveArr[0])-2))
            self.drawranline(x,y,px,py)
            self.dropNode(px,py,r*0.6)

   def dropRiver(self,xs,ys,t):
    if t<=0:
        return
    x = xs
    for j in range(ys,len(self.caveArr[0])):
        for i in range(max(0,x-t),min(x,len(self.caveArr))):
            if self.caveArr[i][j] == 0:
                self.caveArr[i][j] = 66
        x+=randint(-1,1)
        if randint(0,20) == 0:
            self.dropRiver(x+  (randint(0,1)*2-1)*(t+1) ,j,t-1)
            if randint(0,1) == 0:
                t-=1

   def makeRayH(self):
    y = randint(2,len(self.caveArr[0])-3)
    g = []
    for x in range(0,len(self.caveArr)):
        if self.caveArr[y][x] in [0,66]:
            g.append(x)
    shuffle(g)
    s = g[:(len(g)-1)//10]
    for x in g:
        if x in s:
            self.caveArr[y][x] = 3
        else:
            self.caveArr[y][x] = 2

   def makeRayV(self):
    x = randint(2,len(self.caveArr)-3)
    g = []
    for y in range(0,len(self.caveArr[0])):
        if self.caveArr[y][x] in [0,66]:
            g.append(y)
    shuffle(g)
    s = g[:(len(g)-1)//10]
    for y in g:
        if y in s:
            self.caveArr[y][x] = 3
        else:
            self.caveArr[y][x] = 2


   def makeCaveLevel(self,xsize,ysize):
#    self.caveArr = [[55 for _ in range(ysize)] for _ in range(xsize)]
    self.makeCave(xsize,ysize,[])
    self.dropNode(30,30,10)
#    self.drawranline(0,0,59,59)
    self.makeRayH()
    self.makeRayV()
    if randint(0,3)<3:
        self.dropRiver(30,0,randint(2,5))


    toclean=[]
    for i in range(0,xsize):
        for j in range(0,ysize):
            if self.caveArr[j][i] == 55:
                clean = True
                gg = [ (x,y) for x in [i-1,i,i+1] for y in [j-1,j,j+1] ]
                for g in gg:
                    if (not g[0] in range(0,xsize)) or (not g[1] in range(0,ysize)):
                        continue
                    if self.caveArr[g[1]][g[0]] in [0,3,66]:
                        clean = False
                if clean:
                    toclean.append((i,j))
    for t in toclean:
        self.caveArr[t[1]][t[0]] = 1

   def makeVillage(self,xsize,ysize):

    self.caveArr = [[55 for i in range(ysize)] for t in range(xsize)]

    nodes = [ (randint(1,xsize-2),randint(1,ysize-2)) for _ in range(13) ]

    rooms = []
    safec = 0
    while len(rooms)<30 and safec<400:
        w = randint(5,11)
        l = randint(5,11)        
        x = randint(1,xsize-2-w)
        y = randint(1,ysize-2-l)
        canPlace = True
        for i in range(x+1,x+w-1):
            for j in range(y,y+l-1):
                if self.caveArr[i][j] != 55:
                    canPlace = False
        if canPlace:
                rooms.append((x,y,w,l))
                if randint(0,3) > 0:
                    for i in range(x,x+w):
                        for j in range(y,y+l):           
                            self.caveArr[i][j] = 0
                            if i == x or i == x+w-1 or j == y or j == y+l-1:
                                   self.caveArr[i][j] = 2
                else:

                    for d in range(0,randint(1,3)):
                        xs = x+ w//2
                        ys = y+ l//2
                 
                        for c in range(20):
                            if randint(0,1)==0:
                                xs += randint(0,1)*2-1
                            else:
                                ys += randint(0,1)*2-1
                            xs = max(x,min(xs,x+w-1))
                            ys = max(y,min(ys,y+l-1))
                            self.caveArr[xs][ys] = 0
                                   
                            


        safec += 1


    nodes = [ (r[0],r[1],r[2],r[3]) for r in rooms ]

    edges = [ (a,b, abs(a[0]-b[0]) + abs(a[1]-b[1])) for a in nodes for b in nodes ]

    mst = Kruskal(nodes,edges)


    for e in mst:
        r1 = e[0]
        r2 = e[1]
        
        
        p1 = (r1[0] + r1[2]//2 , r1[1] + r1[3]//2)
        p2 = (r2[0] + r2[2]//2 , r2[1] + r2[3]//2)
        
        self.drawranline(p1[0],p1[1],p2[0],p2[1])

    toclean=[]
    for i in range(0,xsize):
        for j in range(0,ysize):
            if self.caveArr[j][i] == 55:
                clean = True
                gg = [ (x,y) for x in [i-1,i,i+1] for y in [j-1,j,j+1] ]
                for g in gg:
                    if (not g[0] in range(0,xsize)) or (not g[1] in range(0,ysize)):
                        continue
                    if self.caveArr[g[1]][g[0]] in [0,3,66]:
                        clean = False
                if clean:
                    toclean.append((i,j))
    for t in toclean:
        self.caveArr[t[1]][t[0]] = 1

