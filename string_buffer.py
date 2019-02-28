# String buffer for text editor
import string

class Buffer:

  def __init__(self):
    self.lines = list()
  
  def clear(self):
    self.lines = list()
  
  def append_line(self, string):
    self.lines.append(string)
    
  def insert_line(self, string, line_num):
    self.lines.insert(line_num, string)
    
  def remove_line(self, line_num):
    self.lines.pop(line_num)

  def replace_tabs(self, tabwidth):
    spaces = " " * tabwidth
    for i in range(len(self.lines)):
      self.lines[i] = self.lines[i].replace('\t', spaces)
    
  def insert_char(self, char, line, pos):
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos] + char + previous_line[pos:]
  
  def append_char(self, char, line):
    self.lines[line] = self.lines[line] + char
  
  def delete_char(self, line, pos):
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos] + previous_line[pos + 1:]
    
  def split_line(self, line, pos):
    previous_line = self.lines[line]
    self.lines[line] = previous_line[:pos]
    self.insert_line(previous_line[pos:], line + 1)
    
  def join_lines(self, line1, line2):
    self.lines[line1] += self.lines[line2]
    self.remove_line(line2)
    
  def get_char(self, line, pos):
    return self.lines[line][pos]
  
  def get_line(self, line):
    return self.lines[line]
  
  def get_lines(self):
    return self.lines
  
  def line_length(self, line):
    return len(self.lines[line])
  
  def size(self):
    return len(self.lines)
  
  def __rep__(self):
    return "\n".join(self.lines)
    
    
    
    
    
    
