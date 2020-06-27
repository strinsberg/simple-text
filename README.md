# Simple Text
A very basic terminal text editor.

I made this to learn a little about the challenges of building a text editor and a more involved python program.
As a result I used a very inefficient implementation for my buffer. It is a list of strings.
This is extra bad in python since strings are immutable, but for a learning experience it did the trick.

# Features
- Basic editing of text files
- Saving and loading
- Line wrapping
- Prompt when quitting with unsaved changes
- Some screen resizing

# Limitaitons
- **Converts all tabs to 4 spaces**. So be careful not to edit and save anything you need tabs in.
- Cursor movement left and right won't move to previous or next line
- Pretty much anything else your prefered text editor does

# Try it out
If you want to give it a try just download the source. Open a terminal in the created directoryand run
```
python3 simple_text.py
```

On windows you will need to install the `windows-curses` module to run the program.
```
pip install windows-curses
```

