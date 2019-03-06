import curses
import curses_editor
import sys


def main(stdscr):
  """Create the editor and run it"""
  
  # If the program is run with a filename argument pass it to the editor
  if len(sys.argv) == 2:
    ed = curses_editor.Curses_editor(stdscr, sys.argv[1])
  else:
    ed = curses_editor.Curses_editor(stdscr)
  
  # Run the editor
  ed.start()
  

# Wrap the program so curses will exit properly if there is an error
if __name__ == "__main__":
  curses.wrapper(main)
