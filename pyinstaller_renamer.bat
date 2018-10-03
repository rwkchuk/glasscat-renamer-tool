echo %cd%
PyInstaller -y -F --noconsole --distpath="." --paths=C:\Python27amd64\Lib\site-packages\PyQt4 --hidden-import=PyQt4 renamer.py
pause