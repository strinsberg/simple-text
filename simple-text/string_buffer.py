import string

# Note this is not an efficient implementation of a text editor buffer
# It is used for it's simplicity to get some experience exploreing the
# process and problems involved in writing a command line text editor.
class Buffer:
  """A text editor buffer using an array of strings"""

  def __init__(self):
    self.lines = list()
  
  
  def clear(self):
    """Clear the buffer"""
    self.lines = list()
  
  
  def append_line(self, string):
    """Add a line of text to the end of the buffer"""
    self.lines.append(string)
  
    
  def insert_line(self, string, line_num):
    """Insert a line of text at a given line number"""
    self.lines.insert(line_num, string)
  
    
  def remove_line(self, line_num):
    """Remove a line of text at the given line number"""
    self.lines.pop(line_num)


  def replace_tabs(self, tabwidth):
    """Replaces all tabs with a given number of spaces"""
    spaces = " " * tabwidth
    for i in range(len(self.lines)):
      self.lines[i] = self.lines[i].replace('\t', spaces)
    

  def insert_char(self, char, line, pos):
    """Insert a character in a given line at a given position"""
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos] + char + previous_line[pos:]
  
  
  def append_char(self, char, line):
    """Add a character to the end of a given line"""
    self.lines[line] = self.lines[line] + char
  
  
  def delete_char(self, line, pos):
    """Delete a character at a given line and position"""
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos] + previous_line[pos + 1:]
    
    
  def split_line(self, line, pos):
    """Split a given line into two lines at a given position"""
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos]
    self.insert_line(previous_line[pos:], line + 1)
    

  def join_lines(self, line1, line2):
    """Join a line onto the end of another line"""
    self.lines[line1] += self.lines[line2]
    self.remove_line(line2)
    
    
  def get_char(self, line, pos):
    """Return the character at a given line and position"""
    return self.lines[line][pos]
  
  
  def get_line(self, line):
    """Return a given line of text"""
    return self.lines[line]
  
  
  def get_lines(self):
    """Return the list of lines"""
    return self.lines
  
  
  def line_length(self, line):
    """Return the length of a given line"""
    return len(self.lines[line])
  
  
  def size(self):
    """Get the number of lines"""
    return len(self.lines)
  
  
  def __rep__(self):
    """Return the string representation of the buffer"""
    return "\n".join(self.lines)
    
    
    
    
    
    
