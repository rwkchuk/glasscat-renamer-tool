''' main file for the renamer tool '''
import gui_helper as gui
import sys
import subprocess
import file_helper as fh

def main():
    app = gui.QtGui.QApplication(sys.argv)

    #object that holds and handles files
    renmaer_data = fh.file_renamer()
    #object that shows the files and takes in input
    window = gui.main_window('renamer', renmaer_data)

    #used for testing purposes
    #subprocess.Popen(r'explorer /root,"D:\"')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()