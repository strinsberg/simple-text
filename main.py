# editor main
# should find a way to make this all modular so that the editor just accepts
# a window instead of creating it's own. This is not too hard, however getting
# it to work without it taking over the whole window while it is running will
# be tricky. It will require having it run or at least only accept input when
# it's focused window is active. May require making a slight change so that
# i create my own window objects that can contain other curses components and
# can update on their own without being tied to the whole thing. Or perhpas
# just make the editor take input from an outside source and forget it
# being completely modular unless I want to run it in its own window.
# that way in the program if the editor window is focused it's get input can
# be called and then it's state refreshed affecting no other windows, but still
# allowing others to be displayed or worked in seperately.
# 
# Other than saving at this point the editor class is generally functional
# the way I want it. Though without any tab mechanism yet I think. though I could
# just keep it to trim tabs for now

import curses
import curses_editor
import sys

def main(stdscr):
  if len(sys.argv) == 2:
    ed = curses_editor.Curses_editor(stdscr, sys.argv[1])
  else:
    ed = curses_editor.Curses_editor(stdscr)
  ed.start()
  

curses.wrapper(main)
