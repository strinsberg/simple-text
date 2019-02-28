'''
Curses display for a simple terminal text editor

TODOs

Some may be their own classes or in editor class.
Also many of these are not easy to do so think of them as possible future
  projects to try somehting out. A couple involve parsing and could be
  informative and good practice.

-- Fully comment and clean up source for current working version
-- figure out how to put the main file as a script so that you can open it from
-- -- anywhere. Think about opening and saving if you do this since the 
-- -- current working directory may need to be found.
-- Line numbering
-- Find and replace
-- Undo and redo
-- goto line command
-- New document command
-- Highlight current line
-- More robust communication for actions
-- Command system - get or write own parser
-- Proper handling for tabs
-- Syntax highlighting
-- Figure out mouse moving the cursor

'''
import editor
import string_buffer
import string
import os
import curses


# An implementation of the editor with curses
class Curses_editor:

  def __init__(self, window, filename = None):
    self.window = window
    # Initialize the text editor and buffer
    self.editor = editor.Text_editor(string_buffer.Buffer(), filename)
    self.title = "Teddy"
    self.version = "0.1.0"
    
    # Position of the cursor on the screen
    self.row = 1
    self.column = 0
    
    # The top line of the editor to show on the screen
    self.top_line = 0
    
    # Max available window size
    self.max_rows, self.max_columns = self.window.getmaxyx()
    
    # Whether the editor is running
    self.run = True
    
    # Tab stuff
    self.tabwidth = 4
  
    # If the file has been changed
    self.changed = False
    
  
  def start(self):
    while self.run:
      self.display()
      curses.doupdate()
      self.handle_input()
  
  
  def display(self):
    self.window.clear()
    
    # If the screen is big enough print all relevant information
    if self.max_columns > 20 and self.max_rows > 10:
      self.print_buffer()
      self.print_title_bar()
      self.print_message()
      self.print_coords()
      self.print_menu()
    
    self.scroll()  # Scroll the screen if needed
    self.set_cursor()  # Set the cursor coordinates
    self.window.move(self.row, self.column)  # Place the cursor on screen
    
    self.window.noutrefresh()
  
  
  def print_buffer(self):
    # Loop through lines in the buffer starting at the line that
    # should be at the top of the screen. Keep track of row being drawn to.
    lines = self.editor.buffer.get_lines()
    rows = 1
    for i in range( self.top_line, self.top_line + self.max_rows ):
    
      # Ensures that we don't try to print lines that don't exist
      # Had trouble with scrolling to the bottom and had to add this
      if i >= len(lines):
        return
      
      # Print lines and with custom line wrapping so that it does not overwrite
      # anything on the bottom of the screen when long lines are wrapped
      line = lines[i]
      length = len(line)
      
      for i in range( int(length / self.max_columns) + 1):
        # Print the rows after the first in the line if still on the
        # text area
        self.window.addstr(rows, 0,
            line[self.max_columns * i : self.max_columns * (i + 1)])
            
        # If the number of rows is off the desired drawing area stop
        rows += 1
        if rows > self.max_rows - 4:
          return
  
    
  def print_message(self):
    if self.max_columns > len(self.editor.message):
      self.window.addstr(self.max_rows - 3, 0,
          self.editor.message, curses.A_REVERSE)
    
    
  def print_coords(self):
    ln = self.editor.line
    col = self.editor.pos + 1
    coords = "Ln {}, Col {}".format(ln, col)
    if self.max_columns > len(coords):
      self.window.addstr(
          self.max_rows - 3, self.max_columns - (len(coords) + 2), coords,
          curses.A_REVERSE)
  
  
  def print_menu(self):
    menu = [
      {"key": "^X", "text": "Quit"},
      {"key": "^W", "text": "Write Buffer"},
      {"key": "^O", "text": "Open File"}
    ]
    row = self.max_rows - 1
    length = 0
    for item in menu:
      # Get text for menu items
      key = item["key"]
      text = item["text"]
      
      # Ensure no screen overrun
      if length + len(key) + 1 + len(text) > self.max_columns - 1:
        break
      
      # Display menu items
      self.window.addstr(row, length, key, curses.A_REVERSE)
      length += len(key) + 1
      self.window.addstr(row, length, text)
      length += len(text) + 4
    
  
  def print_title_bar(self):
    if self.changed:
      changes = "***"
    else:
      changes = ""
    text = "     {} v{}      File: {}{}".format(
        self.title, self.version, self.editor.filename, changes)
    text += " " * 150
    if len(text) > self.max_columns:
      text = text[:self.max_columns]
    self.window.addstr(0, 0, text, curses.A_REVERSE)
  
  
  def scroll(self):
    rows = self.rows_from_top()
    while rows > self.max_rows - 4 or (rows < 1 and self.top_line > 0):
      if rows > self.max_rows - 4:
        self.top_line += 1
      elif rows < 1 and self.top_line > 0:
        self.top_line -= 1
      
      rows = self.rows_from_top()
    
  
  def rows_from_top(self):
    all_lines = self.editor.buffer.get_lines()
    sub_lines = all_lines[self.top_line : self.editor.line + 1]
    
    rows = 0
    for i in range( len(sub_lines) ):
      rows += 1 + int( len(sub_lines[i]) / self.max_columns )
      
    return rows
  
  
  def set_cursor(self):
    all_lines = self.editor.buffer.get_lines()
    sub_lines = all_lines[self.top_line : self.editor.line]
    
    rows = 1
    for i in range( len(sub_lines) ):
      rows += 1 + int( len(sub_lines[i]) / self.max_columns )
    
    self.row = rows + int(self.editor.pos / self.max_columns)
    self.column = self.editor.pos % self.max_columns
    
  
  def handle_input(self):
    key = self.window.getch()
    
    ########### Movement keys ################
    if key == curses.KEY_UP:
      self.editor.up(self.max_columns)
      
    elif key == curses.KEY_DOWN:
      self.editor.down(self.max_columns)
      
    elif key == curses.KEY_LEFT:
      self.editor.left()
           
    elif key == curses.KEY_RIGHT:
      self.editor.right()
 
    ########### Insert keys ######################
    elif key == curses.KEY_BACKSPACE:
      self.editor.backspace()

    elif key == curses.KEY_DC:
      self.editor.delete()
      
    elif key == curses.KEY_ENTER or key == ord("\n"):
      self.editor.enter()
      
    elif key == ord("\t"):    
      for i in range(self.tabwidth):
        self.editor.add_char(" ")
      
    elif chr(key) in string.printable:
      self.editor.add_char(chr(key))
    
    ############## Command Keys ##################
    elif key == 23: # ^W
      self.save(False)
      
    elif key == 24: # ^X
      self.quit()
      
    elif key == 15: # ^O
      self.open()
      
    ########### Other events ##############
    elif key == curses.KEY_RESIZE:
      self.max_rows, self.max_columns = self.window.getmaxyx()
      
    
  def get_input(self, prompt):
    # Set up window environment
    curses.echo()
    self.display()
    curses.doupdate()
    
    row = self.max_rows - 2
    self.window.addstr(row, 0, prompt + " ", curses.A_REVERSE)
    string = self.window.getstr(row, len(prompt), self.max_columns)
    curses.noecho()
    return string.decode('ascii')


  def open(self):
    self.row = 1
    filename = self.get_input("File path:")
    if filename != "" and self.editor.open_file(filename):
      self.editor.buffer.replace_tabs(self.tabwidth) 
      self.column = 0
      self.top_line = 0

  
  def save(self, save_as):   
    # If the file has no name ask what name to save it as
    if not self.editor.has_filename() or save_as:
      name = self.get_input("Save as:")
      if name == "":
        self.editor.message = "No filename set. File not Saved!"
      else:
        self.editor.save_as(name)
    else:
      self.editor.save()
  
  
  def quit(self):
    # If the buffer has changed ask if they want to save it
    if self.changed:
      confirm = self.get_input("Write changes to file? (y or n):")
      if confirm in ['y', 'Y']:
        self.save(True)
     
    self.run = False
      
