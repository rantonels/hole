import pygame as pg

import sys

KUP = 273
KDOWN = 274
KLEFT = 276
KRIGHT = 275
KENTER = 13

def colorize(img,fore,back):
   fsu = pg.Surface(img.get_rect().size, pg.HWSURFACE)
   bsu = pg.Surface(img.get_rect().size, pg.HWSURFACE)

   fsu.fill(fore)
   bsu.fill(back)
   fsu.blit(img, (0,0), None, pg.BLEND_RGB_MULT)
   fsu.set_colorkey(fsu.get_at((0,0)))
   bsu.blit(fsu, (0,0), None, 0)

   return bsu

C_WHITE = (254,254,254)
C_RED = (254,0,0)
C_GREEN = (0,253,0)
C_BLUE = (0,0,253)
C_YELLOW = (253,253,0)
C_CYAN = (0,253,253)
C_MAGENTA = (253,0,253)
C_BLACK = (3,3,3)

COLORPAIRS = {
    0:(C_WHITE,     C_BLACK),
    1:(C_BLACK,     C_WHITE),
    2:(C_GREEN,     C_BLACK),
    3:(C_YELLOW,    C_BLACK),
    4:(C_RED,       C_BLACK),
    5:(C_BLACK,     C_YELLOW),
    6:(C_WHITE,     C_BLUE),
    7:(C_YELLOW,    C_WHITE),
    8:(C_BLUE,      C_BLACK),
    9:(C_WHITE,     C_RED),
    10:(C_MAGENTA,  C_BLACK)
}

class Pad:
    def __init__(self,xsize,ysize):
        self.data = [[[0,0] for _ in range(ysize)] for _ in range(xsize)]
        self.xsize = xsize
        self.ysize = ysize    

    def clear(self):
        for i in range(0,self.xsize):
            for j in range(0,self.ysize):
                self.data[i][j] = [0,0]
    def erase(self):
        self.clear()

    def addch(self,y,x,char,color=0):
        if char == '\n':
            return
        if x in range(0,self.xsize) and y in range(0,self.ysize):
            self.data[x][y] = [ord(char),color]
        else:
            print("WARNING: drawing outside canvas.")
    def addstr(self,y,x,string,color=0):
        i = 0
        for s in string:
            self.addch(y,x+i,s,color)
            i+=1


class Terminal:
    def __init__(self,MX,MY,fontfile):
        pg.init()
        pg.mouse.set_visible(0)

        self.font = pg.image.load(fontfile)
        self.colorpairs = []
        for i in range(0,20):
            if i in COLORPAIRS:
                self.colorpairs.append(colorize(self.font,COLORPAIRS[i][0],COLORPAIRS[i][1]))
            else:
                self.colorpairs.append(self.font)

        print("Font file size: "+str(self.font.get_width())+"x"+str(self.font.get_height()))

        self.tsize = ( self.font.get_width()//16 , self.font.get_height()//16 )

        print("tile size: "+str(self.tsize[0]) + "x" + str(self.tsize[1]))

        self.W = MX
        self.H = MY

        self.SW = MX*self.tsize[0]
        self.SH = MY*self.tsize[1]

        self.screen = pg.display.set_mode((self.SW,self.SH))

        self.stdscr = Pad(self.W,self.H)

    def refresh(self):
        
        self.screen.fill(pg.Color("black"))
        for i in range(self.W):
            for j in range(self.H):
                coords = (i*self.tsize[0] , j*self.tsize[1])
                ch = self.stdscr.data[i][j][0]
                rect = ( ch%16 * self.tsize[0] , ch//16 * self.tsize[1] , self.tsize[0] , self.tsize[1])
                colfont = self.colorpairs[self.stdscr.data[i][j][1]]
                self.screen.blit(colfont,  coords , rect  )
        pg.display.update()

    def blit(self,pad,yp,xp,ys,xs,h,w):
        for i in range(w):
            for j in range(h):
                if not ( (xs+i) in range(self.W) and (ys+j) in range(self.H)):
                    sys.stdout.write("WARNING: blitting outside area.")
                    sys.stdout.flush()
                    continue
                self.stdscr.data[xs+i][ys+j] = pad.data[xp+i][yp+j]


    '''def getch(self):
        done = False
        while not done:
           for event in pg.event.get():
              if event.type == pg.KEYDOWN:
                return event.key'''

    def getch(self):
      key = -1
      while key == -1:
         event = pg.event.wait()
         if event.type == pg.KEYDOWN:    
           key = event.key
           break
      return key

    def getch2(self):

      pg.event.pump()
      keyPress = self.getKeyPress()

      return keyPress 
