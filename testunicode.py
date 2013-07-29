#coding: utf8

import sys
print(u'╔═╦═╗╓─╥─╖╒═╤═╕┌─┬─┐')
print(u'║ ║ ║║ ║ ║│ │ ││ │ │')
print(u'╠═╬═╣╟─╫─╢╞═╪═╡├─┼─┤')
print(u'║ ║ ║║ ║ ║│ │ ││ │ │')
print(u'╚═╩═╝╙─╨─╜╘═╧═╛└─┴─┘')


import curses

stdscr = curses.initscr()
message = u"hello わたし!"
stdscr.addstr(0, 0, message.encode("utf-8"), curses.A_BLINK)
stdscr.getch() # pauses until a key's hit

