import string
import curses
import string_buffer


class Text_editor:
  """A text editor class that keeps track of the buffer and cursor position"""

  def __init__(self, text_buffer, filename = None):
    self.buffer = text_buffer  # The buffer to hold the text
    
    # Set initial values to the buffer in case there is no file or it
    # fails to load
    self.filename = "untitled"
    self.buffer.append_line("")
    
    
    # If a filename is given attempt to add its contents to the buffer
    if filename:
      self.open_file(filename)

    # Position in buffer
    self.line = 0
    self.pos = 0
    
    # Other variables
    self.has_changes = False  # Have changes been made to the buffer
    self.message = ""  # To keep track of any editor information messages
  
  
  def open_file(self, filename):
    """Open a file with a given file name and add its contents to the buffer"""
    try:
      with open(filename, 'r') as f:
        self.buffer.clear()
        self.filename = filename
        self.line = 0
        self.pos = 0
        
        # Add each line from the file to the buffer.  Trim "\n".
        # Buffer also converts tabs to spaces.
        for line in f:
          self.buffer.append_line( line.strip("\n") )
        
        self.has_changes = False
        self.message = "Succesfully opened: '{}'".format(filename)
        return True
    except:
      self.message = "Error opening file: '{}'".format(filename)
      return False

  
  def save(self):
    """Save the buffer contents"""
    return self.save_as(self.filename)
      

  def save_as(self, filename):
    """Save the buffer contents in a file with the given filename"""
    # Join together the buffer contents so it can be written to a file
    contents = ""
    for line in self.buffer.get_lines():
        contents += line + '\n'
        
    # Attempt to open or create the file and write the contents to it
    try:
      with open(filename, 'w') as f:
        f.write(contents)
        self.filename = filename
        self.has_changes = False
        self.message = "Succesfully saved: '{}'".format(filename)
        return True
    except:
      self.message = "Error writing file. File not saved!"
      return False
  

  def has_filename(self):
    """Return weather or not a file name has been set"""
    if self.filename == "untitled":
      return False
    else:
      return True
  

  def add_char(self, char):
    """Add a character to the buffer at the cursors current position"""
    if self.pos >= self.line_length():
      self.buffer.append_char(char, self.line)
    else:
      self.buffer.insert_char(char, self.line, self.pos)
    
    self.pos += 1
    self.has_changes = True


  def backspace(self):
    """Delete the character behind the cursor or join line to the one above"""
    # If the position is at the beggining of a line that is not the first
    # line then join the line to the end of the line above it.
    if self.pos == 0 and self.line > 0:
      self.pos = self.buffer.line_length(self.line - 1)
      self.buffer.join_lines(self.line - 1, self.line)
      self.line -= 1
    elif not (self.pos == 0 and self.line == 0):
      # Delete the character before the cursor and move the position back 1
      self.buffer.delete_char(self.line, self.pos - 1)
      self.pos -= 1
    
    self.has_changes = True

  
  def delete(self):
    """Delete the character under the cursor"""
    # If the position in the buffer is on a char
    if self.pos < self.buffer.line_length(self.line):
      self.buffer.delete_char(self.line, self.pos)
      self.has_changes = True
  
    
  def enter(self):
    """Move cursor down to the next line. Split current line if in middle."""
    if self.pos < self.line_length():
      # If the position is not at the end of the line split the line
      self.buffer.split_line(self.line, self.pos)
    else:
      self.buffer.insert_line("", self.line + 1)
    
    self.line += 1
    self.pos = 0
    self.has_changes = True
  
  
  
  # Move the position in the buffer up. If wrap is set as a number of columns
  # the position will follow word wrapping rules.
  def up(self, wrap = None):
    """Move the cursor up a line or within the line if a wrap width is given"""
    len_current = self.line_length()
    
    # If there is line wrapping
    if wrap:
    
      # If the position is in the top wrap of the line move it into the
      # last wrap of the line above it. Take into account shorter lines
      if self.pos < wrap and self.line > 0:
        len_next = self.line_length(-1)
        wraps_next = int(len_next / wrap)
        columns_next = len_next % wrap
        self.line -= 1
        if self.pos > columns_next:
          self.pos = (wraps_next * wrap) + columns_next
        else:
          self.pos = (wraps_next * wrap) + self.pos
        
      # If the position is in the wraps of the current line
      elif self.pos >= wrap:
        self.pos = self.pos - wrap
      
    # If there is no line wrapping move to the same position or lower in
    # the next line up.
    elif self.line > 0:
      len_next = self.line_length(-1)
      self.line -= 1
      if self.pos > len_next:
        self.pos = len_next


  def down(self, wrap = None):
    """Move the cursor down a line or within the line if wrap width is given"""
    len_current = self.line_length()
    
    # If there is line wrapping
    if wrap:
      wraps_current = int(len_current / wrap)
      columns_current = len_current % wrap
      
      # If the position is not in the bottom wrap of the line move it down a
      # wrap. Take into account shorter wraps below.
      if len_current > wrap and self.pos < wraps_current * wrap:
        pos_wrap = int(self.pos / wrap)
        if pos_wrap + 1 == wraps_current and self.pos % wrap > columns_current:
          self.pos = (wraps_current * wrap) + columns_current
        else:
          self.pos = self.pos + wrap
      
      # If the position is in the bottom wrap move it to the first wrap of
      # the next line. Take into acount shorter lines below.
      elif self.line < self.buffer.size() - 1:
        len_next = self.line_length(1)
        self.line += 1
        if self.pos % wrap > len_next:
          self.pos = len_next
        else:
          self.pos = self.pos % wrap
        
    # If no wrapping is being done move the line down one and adjust the
    # position if the next line is shorter.
    elif self.line < self.buffer.size() - 1:
      len_next = self.line_length(1)
      self.line += 1
      if self.pos > len_next:
        self.pos = len_next
  
  
  # Does not move to the next line if end of line is reached.
  def left(self):
    """Move the cursor left once. Won't move down if line end is reached"""
    if self.pos > 0:
      self.pos -= 1
  
  
  # Does not move to next line yet.
  def right(self):
    """Move cursor right once. Wont move up if line begin is reached"""
    if self.pos < self.buffer.line_length(self.line):
      self.pos += 1
  
  
  # Caller is responsible for not calling it with out of range lines
  def line_length(self, dLine = 0):
    """Return the length of the current line or a line a given offset"""
    return self.buffer.line_length(self.line + dLine)