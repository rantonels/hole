# Class to produce random map layouts
from numpy import *
from random import *
from math import *

wedidit=True
class dMap:
   def __init__(self):
       self.roomList=[]
       self.cList=[]
   def makeMap(self,xsize,ysize,fail,b1,b2,mrooms):
       global wedidit
       wedidit = True
       """Generate random layout of rooms, corridors and other features"""
       #makeMap can be modified to accept arguments for values of failed, and percentile of features.
       #Create first room
       self.mapArr=ones((ysize,xsize))
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
	saas=randrange(3)+9
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
		   if (rty == 6) and ((ww>8) and (ll>8)) and ((j-ll/2)**2 + (k-ww/2)**2 < 4):
			self.mapArr[ypos+j][xpos+k]=walltype
	   if(rty == 100):
		   self.mapArr[ypos+ll/2-1][xpos+ww/2-1]= dragon

	
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
         					if self.mapArr[(ypos-1)+j][(xpos-1)+k] == 0:
							self.mapArr[(ypos-1)+j][(xpos-1)+k]=3
			for k in range(ww+2):
					for j in [0,ll+1]:
						if self.mapArr[(ypos-1)+j][(xpos-1)+k] == 0:
							self.mapArr[(ypos-1)+j][(xpos-1)+k]=3


   def makeLava(self,xsize,ysize,amt,iters):
		self.lavaArr = [[int(random() < amt) for i in range(0,ysize)] for j in range(0,xsize)]
		self.tempArr = [[self.lavaArr[i][j] for i in range(0,ysize)] for j in range(0,xsize)]
		for i in range(0,1):
			print i+1
			for x in range(0,xsize):
				if x == 0 or x == xsize-1:
					for y in range(0,ysize):
						self.tempArr[y][x] = 0
				else:
					for y in range(0,ysize):
						if y== 0 or y == ysize-1:
							self.tempArr[y][x] = 0
						else:
#							s = sum([self.lavaArr[ups][x-1:x+2] for ups in range(y-1,y+2)]) - self.lavaArr[y][x]
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
