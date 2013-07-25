DEBUG = False
DEBUG = True

sgn = lambda x : cmp(x,0)
def reverse(lis):
	return lis[::-1]

import curses
from random import randint
from dMap import *

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.curs_set(0)

#DATA

tfile = open('title','r')
title = tfile.readlines()
tfile.close()

def isfree(num):
	return (num in [0])

#OBJECT STRUCTURE:
# [0] x / null in inv
# [1] y / null in inv
# [2] id
# [3] adj
# [4] plant type
# [5] clear

OBJ_GOLD  = 0
OBJ_PLANT = 1
OBJ_BREAD = 2
OBJ_DROP = 3
OBJ_EMERALD = 4
OBJ_GOULASH = 5

OBJ_BOOK_BOTANY = 100
OBJ_BOOK_TELEPORTATION = 101
OBJ_BOOK_FIRE = 102
OBJ_BOOK_THUNDER = 103
MAXBOOK = 103

OBJ_SWORD = 200
OBJ_GLOVES = 201
OBJ_SHIELD = 202
OBJ_WAND = 203
MAXARMOUR = 203

def object_names(obj):
	num = obj[2]
	out="ERROR"
	matr= {
	0:"Gold_DEBUG",
	1:"Plant_DEBUG",
	2:"Bread",
	3:"DEBUG",
	4:"DEBUG",
	5:"Goulash",
	
	100:"Book of Botany",
	101:"Book of Teleportation",
	102:"Book of Fire",

	200:"Sword",
	201:"Gloves",
	202:"Shield",
	203:"Magic Wand"

	}
	if num in matr:
		out=matr[num]
	if num == 1:
		if obj[5] == 1:
			if obj[3] == 0:
				out = plants[obj[4]]
			else:
				out = plant_adjectives[obj[3]][1] + " " + plants[obj[4]]
		else:
			out = "Herb"
	return out


plant_adjectives = {
0:(0.5,"PLAIN"),
1:(0.7,"Stinging"),
2:(0.8,"Sacred"),
3:(0.9,"Spicy"),
4:(1,"Silver"),
5:(0.95,"Golden")
}

plants = {
0:("Basil"),
1:("Stramonium"),
2:("Sage"),
3:("Nettle"),
4:("Dandelion")
}

solids = []


# name / sprite / attack / defense / hp / exp

mobsalphabet = {
0:"Ant",
1:"Bee",
2:"Chicken",
3:"Dog",
4:"Emu",
5:"Frog",
6:"Gerbil",
7:"Hyena",
8:"Impala",
9:"Jackal",
10:"Kangaroo",
11:"Leech",
12:"Moth",
13:"Nabarlek",
14:"Ostrich",
15:"Penguin",
16:"Quetzal",
17:"Rabbit",
18:"Squid",
19:"Tiger",
20:"Uakari",
21:"Vulture",
22:"Wolf",
23:"Xanclomys",
24:"Yak",
25:"Zebra"}

                                      #atk   #dfn            #hp             #exp
mobs = [(mobsalphabet[i] , ord('a')+i, i+2  ,  max(1,i-1), 4+2*(i+i*i/4), i/2+1) for i in range(0,len(mobsalphabet))]

bosses = {
	"Dragon": ["Dragon", 'D', 30, 25, 400, 200]
}

'''mobs = {
0:("Worm"	,'w',1,0,5 ,2),
1:("Frog"	,'f',1,1,8 ,3),
2:("Moth"	,'m',2,0,10,3),
3:("Squid"	,'s',2,2,11,5),
4:("Leech"	,'l',3,2,14,7),
5:("Rabbit"	,'r',4,3,16,9),
6:("Zombie"	,'z',5,2,19,11),
7:("Tiger"	,'t',8,4,22,13),
8:("Ghost"	,'g',7,6,24,14)
}'''

LV_W=60
LV_H=60
LW_W=40
LW_H=15

converter = {
0:0,
1:2,
2:1,
3:3,
4:3,
5:3,

98:6,
99:5
}


tset = {
0: (' ',0),
1: ('#',1),
2: ('.',0),
3: ('=',5),
4: ('v',0),
5: ('#',7),
6: ('C',3),


100: ('~',6)
}

ssheet = {
0: ('*',3),
1: ('Y',2),
2: ('0',3),
3: ('*',8),
4: ('*',2),
5: ('Q',3),

100: ('?',3),
101: ('?',3),
102: ('?',3),
103: ('?',3),

200: ('!',0),
201: (':',0),
202: ('O',0),
203: ('\\',0)
}

SPELL_FIRE = 0
SPELL_TELEPORT = 1
SPELL_SUICIDE = 2
SPELL_HEAL = 3
SPELL_GOLDEN = 4
SPELL_WATCH = 5
SPELL_SHOCKWAVE = 6
SPELL_THUNDER = 7

def spellcast(n):
	global entities, x, y, mxhp, hp
	wand = 0
	for k in equip:
		if k[0][2]==OBJ_WAND:
			wand = 1

	if n==0: #fire spell
		mess("You cast a Fire Spell")
		count = 0
		for e in entities:
			if e[0] in range(x-5,x+6) and e[1] in range(y-5,y+6):
				hite(e,8*(1+wand) + atk/2  )
				count +=1
		if count>0:
			mess(str(count)+" enemies got burned by your spell")
		else:
			mess("... but there is noone to hurt.")
	elif n==1:
		(x,y)=findfree()
		mess("You teleport somewhere else")
	elif n==2:
		hitp(60,True)
		mess("You miscast and hurt yourself (-60 HP)")
	elif n==3:
		s=20 + randint(0,30*wand)
		hp = min(mxhp,hp+s)
		mess("You cast a healing spell (+"+str(s)+" HP)")
	elif n==4:
		s=randint(20,50)
		for i in range(0,s):
			xm = randint(x-4,x+5)
			ym = randint(y-4,y+5)
			if isfreepos(xm,ym):
				objects.append([xm,ym,OBJ_GOLD])
		mess("You make a large amount of coins materialize")
	elif n==5:
		if wand == 0:
			for i in range(max(0,x-5),min(x+6,LV_W-1)):
				for j in range(max(0,y-5),min(y+6,LV_H-1)):
					floodfill(i,j)
		else:
			for i in range(0,LV_W):
				for j in range(0,LV_H):
					floodfill(i,j)

		mess("You cast a clairvoyance spell.")
	elif n==6:
		mess("You cast a Shockwave Spell")
		count = 0
		for e in entities:
			if e[0] in range(x-5,x+6) and e[1] in range(y-5,y+6):
				nx = e[0]+randint(2,5+3*wand)*sign(e[0]-x)
				ny = e[1]+randint(2,5+3*wand)*sign(e[1]-y)
				if isfreepos(nx,ny):
					e[0]=nx
					e[1]=ny
					count+=1
				else:
					if randint(0,2) == 0:
						hite(e,(3 + atk/2)*(1+wand))
						count+=1
		if count>0:
			mess(str(count)+" enemies were affected by the wave")
		else:
			mess("... but there is noone to hurt.")
	elif n==7:
		count = []
		leclos = 100
		for i in range(0,len(entities)):
			e = entities[i]
			if e[0] in range(x-8,x+9) and e[1] in range(y-8,y+9):
				r= abs(e[0]-x) + abs(e[1]-y) 
				if r < leclos:
					leclos = r
					count=[i]
				elif r == leclos:
					count.append(i)
		if len(count)>0:
			tget =  choice(count)
		mess("You cast a Thunder Spell on the "+e[2]+str(leclos))
		hite(e,int((3+atk)*(1+0.5*wand)))

	else:
		mess("You cast a Thunder Spell that goes nowhere")
					

def exprofile(r):
	return int(r*4.9)


curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #1 black on white
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) #2 green
curses.init_pair(3, curses.COLOR_YELLOW,curses.COLOR_BLACK) #3 yellow
curses.init_pair(4, curses.COLOR_RED,   curses.COLOR_BLACK) #4 red
curses.init_pair(5, curses.COLOR_BLACK,   curses.COLOR_YELLOW) #4 black on brown
curses.init_pair(6, curses.COLOR_WHITE,  curses.COLOR_BLUE) #white on blue
curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_WHITE) 
curses.init_pair(8, curses.COLOR_BLUE,  curses.COLOR_BLACK) #blue on black

mypad = curses.newpad(LV_W,LV_H)
stdscr.refresh()

back = curses.newwin(0,0)

#INIT
mxhp=100
hp=100
mana=0
manacount=0
gold=0
rank=1
gems=[False]*50
exp=0
name="Sasellor"
DEBUG_CHEST = [ [0,0,OBJ_WAND], [0,0,OBJ_SHIELD] , [0,0,OBJ_GLOVES] ]
inventory = [ [0,0,OBJ_BREAD] ] #+ DEBUG_CHEST 
if DEBUG: inventory+= DEBUG_CHEST
equip = [ ]

def additem(o):
	if len(inventory)<10:
		inventory.append(o)
		return True
	else:
		return False

atk=1
dfn=0



objects = []
entities = []

def hitp(force,ignoredef=False):
global hp, dfn, equip
if ignoredef:
	damage = force
else:
	shield = 0
	for k in equip:
		if k[0][2] == OBJ_SHIELD:
			shield = 2
	damage = force - randint(0,dfn+shield)
damage = max(0,damage)
hp=max(0,hp-damage)

def dropshit(x,y,lv):
global objects
value = randint(0,lv)
lo = [0]
if value <= 1:
	lo = [OBJ_GOLD]
elif value <= 3:
	lo = ranplant()
elif value <= 6:
	lo = [choice(range(100,MAXBOOK))]
elif value <= 7:
	l0 = [choice(range(200,MAXARMOUR))]
else:
	lo = [OBJ_GOLD]
objects.append([x,y]+lo)

def hite(e,force):
damage = max(0,force-randint(0,e[5]))
e[6] = max(0,e[6]-force)
if(e[6]<=0):
	mess("The "+e[2]+" is dead.")
	if (e[3] in range(ord('a'),ord('z')+1)) and randint(0,5)==0:
		dropshit(e[0],e[1],e[3]-ord('a'))
	entities.remove(e)
	givexp(e[7])
else:
	if(damage>0):
		mess("The "+e[2]+" was hit. (-"+str(damage)+" HP)")
	else:
		mess("You missed the "+e[2])

def givexp(amt):
global exp, rank, atk, dfn, mxhp
exp += amt
lepl = False
while(exp >= exprofile(rank)):
	exp-=exprofile(rank)
	rank+=1
	atk+=1+rank/5
	dfn+=(rank+3)/5
	mxhp+=3 + rank**2/17
	lepl=True
if(lepl):
	mess("Welcome to level "+str(rank))

def isfreepos(cx,cy):
if((cx<0)or(cy<0)or(cx>=LV_W)or(cy>=LV_H)):
	return False
s = True
global x,y

if ((x==cx) and(y==cy)):
	s = False
for e in entities:
	if ((e[0]==cx) and(e[1]==cy)):
		s = False
for o in objects:
	if ((o[2]) in solids):
		if ((o[0]==cx)and(o[1]==cy)):
			s = False

return (s and isfree(lvl[cx][cy]))

def isfrees(qx,qy):
return isfree(lvl[qx][qy])

def cansee(xa,ya,xb,yb):
x1=min(xa,xb)
x2=max(xa,xb)
y1=min(ya,yb)
y2=max(ya,yb)
clear1=True
for x in range(x1,x2+1):
	clear1 = clear1 and isfrees(x,y1)
for y in range(y1,y2+1):
	clear1 = clear1 and isfrees(x2,y)

clear2=True
for y in range(y1,y2+1):
	clear2 = clear2 and isfrees(x1,y)
for x in range(x1,x2+1):
	clear2 = clear2 and isfrees(x,y2)

return clear1 or clear2

messages=["the adventure begins"]
def mess(strin):
if len(messages)>=5:
	messages.pop(0)
messages.append(strin)

def findfree():
global lvl
gx = 0
gy = 0
safe = 0
while not isfree(lvl[gx][gy]) and safe < 400:
	gx = randint(0,LV_W-1)
	gy = randint(0,LV_H-1)
	safe+=1
return (gx,gy)

fog = []
def floodfill(xs,ys,ite=-1):
if ite==0:
	return
if ite==-1:
	nex=-1
else:
	nex=ite-1
global fog
if fog[xs][ys] != 0:
	return
fog[xs][ys] = 1
if isfree(lvl[xs][ys]):
	floodfill(xs+1,ys,nex)
	floodfill(xs-1,ys,nex)
	floodfill(xs,ys-1,nex)
	floodfill(xs,ys+1,nex)
	floodfill(xs+1,ys+1,nex)
	floodfill(xs-1,ys+1,nex)
	floodfill(xs-1,ys-1,nex)
	floodfill(xs+1,ys-1,nex)

def fag(xp,yp):
global x,y
return fog[xp][yp] or 0# ( (xp in range(x-4,x+4)) and (yp in range(y-4,y+4)))

def ranplant():
r = (0,0,0,0,0,0,0,1,1,1,2,2,3,3,4,4,5)
return [OBJ_PLANT,choice(r),randint(0,4),randint(0,3)/3]

ppp = 3
for l in title:
stdscr.addstr(ppp,8,l)
ppp+=1

stdscr.addstr(12,5,"Input your name (Press Enter for random name):")
stdscr.refresh()
curses.echo()
name = stdscr.getstr(14,6,10)
curses.noecho()

if name=="":
name="Sasellor"

alive=True
stage=0
WATSTEPS=500
waterlvl=-200
while alive:
stage+=1
stdscr.addstr(3,3,"Generating dungeon...")
stdscr.refresh()

objects = []
entities = []


mapper=dMap()
dragonfactor = 4 * stage**2/(50**2)
mapper.makeMap(LV_W,LV_H,110,10+dragonfactor,dragonfactor,60)

lvl = [[converter[mapper.mapArr[j][i]] for i in range(0,LV_W)] for j in range(0,LV_H)]

for i in range(0,LV_W):
	for j in range(0,LV_H):
		if lvl[i][j] == 3:
			c = (lvl[i+1][j]==1)+(lvl[i-1][j]==1)+(lvl[i][j-1]==1)+(lvl[i][j+1]==1)
			if c<2:
				lvl[i][j] = 0

#add exit
if stage < 50:
	(ex,ey) = findfree()
	lvl[ex][ey] = 4 
else:
	mess("You enter the last dungeon...")

#add 15 gold pieces
for c in range(0,15):
	(gx,gy) = findfree()
	objects.append([gx,gy,OBJ_GOLD])

#add 0-2 mana drops
for c in range(0,2):
	(gx,gy) = findfree()
	objects.append([gx,gy,OBJ_DROP])

#add 1 emerald
for c in range(0,1):
	(gx,gy) = findfree()
	objects.append([gx,gy,OBJ_EMERALD])

#add food
for c in range(0,randint(0,1)):
	(gx,gy) = findfree()
	objects.append([gx,gy,OBJ_BREAD])
if stage > 5:
	for c in range(0,randint(0,1)):
		(gx,gy) = findfree()
		objects.append([gx,gy,OBJ_GOULASH])

#add plants
for c in range(0,randint(2,6)):
	gx = 0
	gy = 0
	while not isfree(lvl[gx][gy]):
		gx = randint(0,LV_W-1)
		gy = randint(0,LV_H-1)
	objects.append([gx,gy]+ranplant())

#add books
for c in range(0,randint(0,5)):
	(gx,gy) = findfree()
	objects.append([gx,gy,randint(100,MAXBOOK)])

#add other items
for c in range(0,randint(0,3+stage/3)):
	(gx,gy) = findfree()
	objects.append([gx,gy,randint(200,MAXARMOUR)])

#add mobs
for c in range(0,15+min(stage,50)):
	(gx,gy) = findfree()
	i = randint(min(max(0,stage/2-4-2*(i/20)),len(mobs)-1),min(stage/2,len(mobs)-1))
	entities.append([gx,gy]+list(mobs[i]))

#add boss
for i in range(0,LV_W):
	for j in range(0,LV_H):
		if lvl[i][j] == 6:
			entities.append([i,j]+bosses["Dragon"]+[i,j])
			lvl[j][i] = 0


x = LV_W/2
y = LV_H/2
while not isfree(lvl[x][y]):
	x = randint(0,LV_W-1)
	y = randint(0,LV_H-1)


camx = min(max(0,x-LW_W/2),LV_W-LW_W-1)
camy = min(max(0,y-LW_H/2),LV_H-LW_H-2)


fog = [[0 for j in range(0,LV_H)] for i in range(0,LV_W)]

floodfill(x,y)
#	for i in range(max(0,x-8),min(LV_W,x+8)):
#		for j in range(max(0,y-8),min(LV_H,y+8)):
#			fog[i][j] = 1

crawlin=True
while alive and crawlin:
	#DISPLAY
	#level
	mypad.erase()
	for i in range(0,LV_W):
		for j in range(0,LV_H-1):
			if fag(i,j):
				mypad.addch(j,i,tset[lvl[i][j]][0] , curses.color_pair(tset[lvl[i][j]][1]  ))
			else:
				mypad.addch(j,i,'.')
	for o in objects:
		if fog[o[0]][o[1]]:
				mypad.addch(o[1],o[0],ssheet[o[2]][0], curses.color_pair(ssheet[o[2]][1]))	

	for e in entities:
		if fog[e[0]][e[1]]:
#				if cansee(x,y,e[0],e[1]):
#					c=curses.color_pair(6)
#				else:
#					c=curses.color_pair(4) 
			mypad.addch(e[1],e[0],e[3], curses.color_pair(4))
			'''if e[2] == "Dragon":
				x1 = min(e[0],e[8])
				x2 = max(e[0],e[8])
				y1 = min(e[1],e[9])
				y2 = max(e[1],e[9])
				for i in range(x1+1,x2+1):
					mypad.addch(y1,i,'o')
				for j in range(y1,y2):
					mypad.addch(j,x2,'o')  '''

	mypad.addch(y,x,'@')

	#border
	back.erase()
	back.addch(0,0,'+')
	back.addch(0,LW_W+2,'+')
	back.addch(LW_H+2,LW_W+2,'+')
	back.addch(LW_H+2,0,'+')
	for i in range(0,LW_W+1):	
		back.addch(0,i+1,'-')
		back.addch(LW_H+2,i+1,'-')
	for i in range(0,LW_H+1):
		back.addch(i+1,0,'|')
		back.addch(i+1,LW_W+2,'|')

	#info
	back.addstr(LW_H+3,1, "HP: "+str(hp)+"/"+str(mxhp))	
	back.addstr(LW_H+3,14, "Gold: "+str(gold))
	if mana>0:
		back.addstr(LW_H+3,25, "Mana: "+str(mana))
	if gems[stage-1]:
		back.addstr(LW_H+3,37, "EF!")
	ct=0
	for m in reverse(messages):
		if ct>3:
			lecol=curses.color_pair(4)
		elif ct == 3:
			lecol=curses.color_pair(3)
		else:
			lecol=curses.color_pair(0)	
		back.addstr(LW_H+5+ct,1, m, lecol)
		ct+=1

	back.addstr(LW_H+2,14,"*FLOOR "+str(stage)+"*")

	back.addstr(0,LW_W+3, "-----------------+")
	back.addstr(1,LW_W+3, name)
	back.addstr(1,LW_W+12, " - LV "+str(rank).zfill(2))
	back.addch(1,LW_W+20,'|')

	back.addstr(2,LW_W+2, "+----INVENTORY----+")
	for i in range(0,len(inventory)):
		s = object_names(inventory[i])

		back.addstr(3+i,LW_W+4, str(i)+". "+s)

	back.addstr(13,LW_W+2,"+-----EQUIPMT-----+")

	for i in range(0,len(equip)):
		back.addstr(14+i,LW_W+4, chr(ord('A')+i) + ". " + object_names(equip[i][0]))

	back.addstr(LW_H+5,LW_W+6,"ATK "+str(atk)+" DEF "+str(dfn))
	back.addstr(LW_H+6,LW_W+6,"EXP "+str(exp)+"/"+str(exprofile(rank)))

	if waterlvl >= WATSTEPS:
		back.addstr(LW_H+8,LW_W+6, "Water to floor "+str(waterlvl/WATSTEPS))


	back.noutrefresh()
	mypad.noutrefresh(camy,camx,1,1,LW_H+1,LW_W+1)

	curses.doupdate()

	#INPUT
	cmd = stdscr.getch()

	#COMPUTE
	turn=0
	#movement

	nx = x
	ny = y
	hasmoved = 0
	if  cmd == curses.KEY_DOWN:
	    ny = min(y+1,LV_H-2)
	    hasmoved = 1
	elif cmd == curses.KEY_UP:
	    ny = max (0,y-1)
	    hasmoved = 1
	elif cmd == curses.KEY_LEFT:
	    nx = max (0,x-1)
	    hasmoved = 1
	elif cmd == curses.KEY_RIGHT:
	    nx = min(x+1,LV_W-1)
	    hasmoved = 1
	if hasmoved:
		if isfreepos(nx,ny):
			x = nx
			y = ny
			turn=1	
		for e in entities:
			if( (e[0]==nx) and (e[1]==ny)):
				tpow = atk
				for k in equip:
					if k[0][2] == OBJ_SWORD:
						tpow = atk * 3/2
				
				hite(e,tpow)
		if lvl[nx][ny] == 3: #open doors
			lvl[nx][ny] = 0
			mess("You open the door.")
		if lvl[nx][ny] == 4: #exit
			crawlin = False
			mess("You descend the stairs...")

	#d drop item
	if cmd == ord('d'):
		stdscr.addstr(7,7,"Select the item you want to drop")
		it = stdscr.getch()
		if it in range(ord('0'),ord('9')+1):
			pos = it-ord('0')
			if pos<len(inventory):
				mess("You dropped the "+object_names(inventory[pos]))
				del inventory[pos]
			else:
				mess("That slot is empty")
		elif it in range(ord('a'),ord('c')+1):
			pos = it - ord('a')
			if pos<len(equip):
				mess("You drop the "+object_names(equip[pos][0]))
				del equip[pos]
			else:
				mess("That slot is empty")

		else:
			mess("You have to specify a slot in your inventory")
	
	#a button
	if cmd == ord('a'):
			found=False
			oc = objects
			for o in objects:
				if ((o[0] == x) and (o[1] == y)):
					found = True
					if o[2] == OBJ_PLANT:
						if additem(o):
							mess("You picked up a "+object_names(o))
							if o[3] == 1:
								gloves=0
								for k in equip:
									if k[0][2]==OBJ_GLOVES:
										gloves=1
								if gloves == 0:
									hitp(10,True)
									mess("You got stung by the herb. -10 HP")
							objects.remove(o)
						else:
							mess("Your inventory is full")
					else:
						if additem(o):
       	                                        	mess("You picked up a "+object_names(o))
       	                                        	objects.remove(o)
       	                                	else:
       	                                        	mess("Your inventory is full")
			if found==False:
				mess("There is nothing here.")
		
		#cast spell
		if cmd == ord('c'):
			if mana > 0:
				wand = 0
				for k in equip:
					if k[0][2]==OBJ_WAND:
						wand = 1
	
				leng=min(5+2*wand,mana)
				stdscr.addstr(7,7,"+-CAST SPELL-+")
				stdscr.addstr(8,7,"*" + (12-leng)/2*" " +leng*"_"  + (13-leng)/2*" "+"*")
				stdscr.addstr(9,7,"+------------+")
				stdscr.refresh()
				c = 0
				s = ""
				while c!= ord('\n') and len(s)<leng:
					c=stdscr.getch()
					if c>250:
						c=0
					if chr(c) in ['q','w','e','r']:
						s+=chr(c)
						stdscr.addstr(8,8+ (12-leng)/2,s)
						stdscr.refresh()

				mana= max(0,mana - len(s))
				mess("You cast the spell '"+s+"' (-"+str(len(s))+" MANA)")
				found=False
				if s.find("eqqr") != -1:
					found = True
					spellcast(SPELL_FIRE)
				if s.find("ewq") != -1:
					found = True
					spellcast(SPELL_TELEPORT)
				if (s.find("wwq") != -1)  or (s.find("qqq") != -1) or (s.find("eqe") != -1) or (s.find("rrw") != -1):
					found = True
					spellcast(SPELL_SUICIDE)
				if s.find("ww") != -1:
					found = True
					spellcast(SPELL_HEAL)
				if s.find("qeeeq") != -1:
					found = True
					spellcast(SPELL_GOLDEN)
				if s.find("qeqr") != -1:
					found = True
					spellcast(SPELL_WATCH)
				if s.find("qrw") != -1:
					found = True
					spellcast(SPELL_SHOCKWAVE)
				if s.find("rwe") != -1:
					found = True
					spellcast(SPELL_THUNDER)
				
				if not found:
					mess("...however, it has no effect.")
				
						
			else:
				mess("You don't have any mana to perform magic with")
	
		# use object (0-9)
		if cmd  in range(ord('0'),ord('9')+1):
			touse = cmd-ord('0')
			if touse in range(0,len(inventory)):
				idd = inventory[touse][2]
				if idd == OBJ_BREAD:
					mess("You eat the bread. +25 HP")
					hp = min(mxhp,hp+25)
					del inventory[touse]
				elif idd == OBJ_GOULASH:
					mess("You eat the goulash. +50 HP")
					hp = min(mxhp,hp+50)
					del inventory[touse]
				elif idd == OBJ_PLANT:
					species = inventory[touse][4]
					adj = inventory[touse][3]
					bonus = 1
					if adj == 5:
						bonus = 5
					elif adj == 4:
						bonus = 2
					elif adj == 1:
						mess("You get stung by the herb (-10 HP)")
						hitp(10,True)
					elif adj == 2:
						mess("This plant is sacred to the gods. +2 MANA")
						mana+=2
					
					if(species == 0):
						hp = min(mxhp,hp+40*bonus)
						mess("The herb makes you healthier. (+"+str(40*bonus)+" HP)")
					elif species == 1:
						hitp(70*bonus,True)
						mess("You eat the herb and feel very, very ill...")
					elif species == 2:
						mana+=2*bonus
						mess("The herb gives you spiritual powers. (MANA +"+str(2*bonus)+")")
					elif species == 3:
						if randint(0,4)<3:
							atk+=bonus
							mess("The herb makes you feel stronger. (ATK +"+str(bonus)+")")
						else:
							mess("You eat the herb, but nothing happens.")
					elif species == 4:
						if randint(0,2)==0:
							dfn+=bonus
							mess("As you chew on the herb, you feel stronger. (DEF +"+str(bonus)+")")
						else:
							mess("You eat the herb, but nothing happens.")
					else:
						mess("You eat the herb, but nothing happens.")
						
					del inventory[touse]

				elif idd == OBJ_BOOK_BOTANY:
					count = 0
					for p in inventory:
						if p[2] == OBJ_PLANT:
							if p[5] == 0:
								count += 1
							p[5] = 1
					mess(str(count)+" plants were identified.")
					del inventory[touse]
				elif idd == OBJ_BOOK_TELEPORTATION:
					spellcast(SPELL_TELEPORT)
					del inventory[touse]
				elif idd == OBJ_BOOK_FIRE:
					spellcast(SPELL_FIRE)
					del inventory[touse]
				elif idd == OBJ_BOOK_THUNDER:
					spellcast(SPELL_THUNDER)
					del inventory[touse]

				elif idd in range(200,300):
					if len(equip) < 3:
						mess("You equip the "+object_names(inventory[touse]))
						equip.append([inventory[touse],100])
						del inventory[touse]
					else:
						mess("You can't equip any more items")

				else:
					mess("You cannot use that.")
			else:
				mess("That slot is empty")

		#i button (stats screen)
		if cmd == ord('i'):
			stdscr.clear()
			stdscr.addstr(1,1,"Floor: "+str(stage).zfill(2) + "/50, water at floor "+str(waterlvl/WATSTEPS))
			for i in range(1,waterlvl/WATSTEPS+1):
				stdscr.addch(2,i,"~",curses.color_pair(6))
			for i in range(waterlvl/WATSTEPS+1,50):
				stdscr.addch(2,i,".")
			stdscr.addch(2,stage,"@")

			stdscr.addstr(4,1,"Emeralds:")
			for i in range(0,7):
				for j in range(0,7):
					if gems[j*7+i]:
						stdscr.addch(6+j,2+i,'*',2)
					else:
						stdscr.addch(6+j,2+i,'.')

			stdscr.refresh()
			stdscr.getch()

		#suicide
		if cmd == ord('p'):
			stdscr.addstr(7,7,"Are you sure you want to kill yourself? (Y/N)")
			stdscr.refresh()
			sure = stdscr.getch()
			if (sure in [ord('y'),ord('Y')]):
				mess("You commit suicide.")
				crawlin=False
				alive=False


		#DEBUG COMMANDS	
		#next level
		#mana cheat
		if DEBUG:
			if cmd == ord('n'):
				crawlin=False
			if cmd == ord('m'):
				mana=999
				givexp(500)
			if cmd == ord('b'):
				gems[3]=True
				gems[7]=True
				gems[0]=True
				gems[48]=True
		#move wotah
		waterlvl+=1
		if stage - waterlvl/WATSTEPS >= 3:
			waterlvl+=3
		if waterlvl==WATSTEPS*stage:
			mess("You hear the rumbling of water entering the dungeon...")
		if waterlvl/WATSTEPS>=stage:
			if waterlvl%15==0:
				(xw,yw) = findfree()
				lvl[xw][yw] = 100
			if waterlvl%10==0:
				for i in range(0,LV_W):
					for j in range(0,LV_H):
						if lvl[i][j]==100:
							for z in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
								if isfreepos(z[0],z[1]):
									lvl[z[0]][z[1]] = 99
				for i in range(0,LV_W):
					for j in range(0,LV_H):
						if lvl[i][j]==99:
							lvl[i][j]=100
	
		#move entities
		for e in entities:
						  
			if e[3] in range(ord('a'),ord('z')+1):
				if e[3] == ord('a'):
					reps = 1
				else:
					reps = 1 + randint(0,25)/(25-e[3]+ord('a'))
			else:
				reps = 2


			for lol in range(0,reps):
				ex=e[0]
				ey=e[1]
				if ((abs(ex-x)+abs(ey-y)) < 8) :
					if (abs(ex-x)+abs(ey-y)) == 1:
						hitp(e[4])
						mess("The "+e[2]+" has hit you. (-"+str(e[4])+" HP)")
						if (len(equip)>0) and (randint(0,30) == 0):
							q = randint(0,len(equip)-1)
							mess("The "+e[2]+" has stripped you of your "+object_names(equip[q][0])+"!")
							del equip[q]
						possible=[]
					else:
						if cansee(x,y,ex,ey):
							factx=-sgn(ex-x)
							facty=-sgn(ey-y)
							possible=[[ex,ey+facty],[ex+factx,ey]]
						else:
							possible=[[ex,ey-1],[ex,ey+1],[ex-1,ey],[ex+1,ey]]
				else:
					possible=[[ex,ey-1],[ex,ey+1],[ex-1,ey],[ex+1,ey]]

			#if e[2] == "Dragon":
			#	possible+=[[ex+i,ey+j] for i in (-1,1) for j in (-1,1)]
			#	possiblec=possible
			#	for p in possiblec:
			#		if ((p[0]-e[8])**2 + (p[1]-e[9])**2) > 5:
			#			possible.remove(p)
				possiblec=possible
				for p in possiblec:
					if not isfreepos(p[0],p[1]):
						possible.remove(p)
				if len(possible)>0:
					(nx,ny)=choice(possible)
					if isfreepos(nx,ny):
						(e[0],e[1])=(nx,ny)
		#mana grow
		if mana>0:
			manacount+=1
			if manacount%200 == 0:
				mana += 1 + mana/13
	
		#checkobjcollision
		oc = objects
		for o in oc:
			if ((o[0] == x) and (o[1]==y)):
				if o[2] == OBJ_GOLD:
					gold+=1
					mess("You find a gold nugget")
					objects.remove(o) 
				if o[2] == OBJ_DROP:
					mana+=1
					mess("You drink a mana drop")
					objects.remove(o)
				if o[2] == OBJ_EMERALD:
					gems[stage-1] = True
					mess("You find an emerald")
					objects.remove(o) 
		

		#extend fog
		
		floodfill(x,y)
		floodfill(x+1,y)
		floodfill(x-1,y)
		floodfill(x,y-1)
		floodfill(x,y+1)
		#for i in range(max(0,x-4),min(LV_W,x+4)):
		#	for j in range(max(0,y-4),min(LV_H,y+4)):
		#		fog[i][j] = 1
		
		
		#check for death
		if(hp<=0):
			alive=False
	
	
		#camera
		camx = min(max(0,x-LW_W/2),LV_W-LW_W-1)
		camy = min(max(0,y-LW_H/2),LV_H-LW_H-2)
	
	
stdscr.clear()
stdscr.refresh()
stdscr.addstr(2,30,"You are dead.")
stdscr.addstr(5,20,"Last messages:")
ppp=7
for m in reversed(messages):
	stdscr.addstr(ppp,23,m)
	ppp+=1

stdscr.addstr(13,20,"You made it to floor "+str(stage)+" with "+str(gold)+" gold.")

c = stdscr.getch()

#END
curses.nocbreak()
stdscr.keypad(0)
curses.echo()

#print mobs

