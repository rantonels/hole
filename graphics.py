import sys
import time

try:
    import pygame as pg
except ImportError:
    print("Pygame was not found. The pygame module is needed for Graphical/Standalone mode (the only mode possible on Windows.) Install it.")
    sys.exit()


KUP = 273
KDOWN = 274
KLEFT = 276
KRIGHT = 275
KENTER = 13

def colorize(img,fore,back):
   '''fsu = pg.Surface(img.get_rect().size, pg.HWSURFACE)
   bsu = pg.Surface(img.get_rect().size, pg.HWSURFACE)

   fsu.fill(fore)
   bsu.fill(back)
   fsu.blit(img, (0,0), None, pg.BLEND_RGB_MULT)
   fsu.set_colorkey(fsu.get_at((0,0)))
   bsu.blit(fsu, (0,0), None, 0)

   return bsu'''

   o = img.copy()
   o.set_palette([back,fore])
   return o.convert()

_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def rgb(triplet):
    return (_HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]])

def triplet(rgb, lettercase=LOWERCASE):
    return format((rgb[0]<<16 | rgb[1]<<8 | rgb[2]), '06'+lettercase)

'''rxvt*color0: #2B2B2B
urxvt*color1: #870000
urxvt*color2: #5F875F
urxvt*color3: #875F00
urxvt*color4: #005FAF
urxvt*color5: #5F5F87
urxvt*color6: #008787
urxvt*color7: #818181'''


C_WHITE = rgb('eeeecc')
C_RED = rgb('bb0000')
C_GREEN = rgb('00bb10')
C_BLUE = rgb('005faf')
C_YELLOW = rgb('ddbb00')
C_CYAN = (0,253,253)
C_MAGENTA = (253,0,253)
C_BLACK = (3,3,3)



def numberize(norc):
    if isinstance(norc,int):
        return norc
    else:
        return ord(norc)

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
            self.data[x][y] = [numberize(char),color]
        else:
            print("WARNING: drawing outside canvas.")
    def addstr(self,y,x,string,color=0):
        i = 0
        for s in string:
            self.addch(y,x+i,s,color)
            i+=1


class Terminal:
    def __init__(self,MX,MY,fontfile,tilesetfile):
        pg.init()


        pg.mouse.set_visible(0)

        pg.key.set_repeat(250, 10)

        self.font = pg.image.load(fontfile)
        self.tileset = pg.image.load(tilesetfile)

        print("Font file size: "+str(self.font.get_width())+"x"+str(self.font.get_height()))

        self.tsize = ( self.font.get_width()//16 , self.font.get_height()//16 )

        print("tile size: "+str(self.tsize[0]) + "x" + str(self.tsize[1]))

        self.W = MX
        self.H = MY

        self.SW = MX*self.tsize[0]
        self.SH = MY*self.tsize[1]

        flags = pg.HWSURFACE | pg.DOUBLEBUF

        self.screen = pg.display.set_mode((self.SW,self.SH),flags)

        self.font = self.font
        self.tileset = self.tileset.convert()
        
        print("extracting colours...")
        (C_WHITE,C_RED,C_GREEN,C_BLUE,C_YELLOW,C_CYAN,C_MAGENTA,C_BLACK) = tuple( 
            [ self.tileset.get_at( (i,0) )[0:3] for i in range(0,8) ] 
        )

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
          10:(C_MAGENTA,  C_BLACK),
          11:(C_WHITE,    C_YELLOW),
          12:(C_YELLOW,   C_RED),
          13:(C_BLACK,    C_MAGENTA),
          14:(C_MAGENTA,  C_GREEN),
          15:(C_WHITE,    C_BLUE),
          16:(C_BLUE,     C_YELLOW),
          18:(C_CYAN,     C_BLACK),
          19:(C_BLACK,    C_BLUE)
        }
        print("generating colorpairs...")
        self.colorpairs = []
        for i in range(0,22 + 64):
            if i in COLORPAIRS:
                self.colorpairs.append(colorize(self.font,COLORPAIRS[i][0],COLORPAIRS[i][1]))
            else:
                self.colorpairs.append(self.font)


        self.stdscr = Pad(self.W,self.H)

        self.ignorepairs = [0]

    def refresh(self):
       
        self.screen.fill(pg.Color("black"))
        for i in range(self.W):
            for j in range(self.H):
                coords = (i*self.tsize[0] , j*self.tsize[1])
                ch = self.stdscr.data[i][j][0]
                if ch == ord(' ') and self.stdscr.data[i][j][1] in self.ignorepairs:
                    continue
                if ch < 127:
                    rect = ( ch%16 * self.tsize[0] , ch//16 * self.tsize[1] , self.tsize[0] , self.tsize[1])
                    colfont = self.stdscr.data[i][j][1]
                    self.screen.blit(self.colorpairs[colfont],  coords , rect  )
                else:
                    tn = ch-127
                    rect = ( tn%32 * self.tsize[0], tn//32 * self.tsize[1], self.tsize[0] , self.tsize[1] )
                    self.screen.blit(self.tileset, coords, rect)
        pg.display.flip()


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
