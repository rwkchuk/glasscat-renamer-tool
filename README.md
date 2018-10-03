# glasscat-renamer-tool
all files for the renamer tool except for the exe

The renamer tool was made by artist request. The artists were frustrated with substance designer use. They hated having to rename
  each texture individually either in UE4 or the file browser. So the renamer tool allows them to do just that for many files and
  folders. All they need to do is drag and drop to start editing.

The pyinstaller_renamer.bat is set up to create an exe for artist use. It creates a just the exe for easy distributing and has no
  debug window when in use.

The renamer.py kicks off the application.
The file_helper.py only contains methods used to modify file names and stores file names and paths.
The gui_helper handles input and call the file_helper.py when needed.
The style_holder.py has strings used by PyQt to update the styles for various sections of the gui.
