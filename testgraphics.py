import graphics
from random import *

term = graphics.Terminal(20,10,"terminal12x12_gs_ro.png")

pad = graphics.Pad(10,10)

for i in range(10):
    for j in range(10):
        pad.addch(i,j,'a',0)

term.blit(pad,0,0,3,0,5,5)

term.refresh()

raw_input()
