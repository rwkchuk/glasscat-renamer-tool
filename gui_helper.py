''' This file contains the gui structure and event handling of the renamer tool'''
import sys
from PyQt4 import QtCore, QtGui
from style_holder import *


class main_window(QtGui.QMainWindow):
    ''' the main window for the gui which also holds logic for events '''
    def __init__(self, app_name = None, renamer_data = None, *args):
            super(main_window, self).__init__(*args)

            #keep access to the data holder
            self.renamer_data = renamer_data

            #set base settings for the main window
            self.setGeometry(100,100,850,500)
            self.setWindowTitle(app_name)
            self.show()
            self.setAcceptDrops(True)

            #layouts for main wiondow
            self.main_layout = QtGui.QVBoxLayout()
            self.main_widget = QtGui.QWidget()
            self.main_widget.setStyleSheet(styles.main_window)
            self.setCentralWidget(self.main_widget)
            self.main_widget.setLayout(self.main_layout)

            #setting the view section that shows added files and potential changes
            self.view = view_widget()
            self.main_layout.addWidget(self.view)

            #setting the list for file widgets which will populate the view section
            self.file_widgets = []

            #setting the edit section for editing files listed in the view section
            self.edit = edit_widget()
            self.main_layout.addWidget(self.edit)

            #bind signals
            self.edit.find_text_field.editingFinished.connect(lambda find_text=self.edit.find_text_field.text(),replace_text=self.edit.replace_text_field.text() : self.update_old_view(find_text))
            self.edit.replace_text_field.editingFinished.connect(self.update_new_view)
            self.view.btn_finalize.clicked.connect(self.finalize_edits)

    def dragEnterEvent(self, e):
        ''' called when something dragged enters the main widget '''
        ''' when this happens check the dragged elements for file paths
        and pass it along '''
        if e.mimeData().hasUrls:
            e.accept()
            #printing for testing purposes
            for u in e.mimeData().urls():
                print u.toLocalFile()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        ''' called when something dragged is moved within the main widget '''
        ''' pass along data that has file paths '''
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        ''' called when something dragged is dropped within the main widget '''
        ''' pass along data that has file paths and process that data to
        populate the files visable in the view section and the data we want to
        store for those files '''
        if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                #add the path to the data
                path = str(url.toLocalFile())
                self.renamer_data.add_file_data(path)

            #update the gui
            for i in self.renamer_data.files_to_edit:
                self.add_file_widget(i)
        else:
            e.ignore()

    def finalize_edits(self):
        ''' when edits are finished reset the gui and data for the files '''
        #tell renamer to make changes to the actual files with the data
        self.renamer_data.update_system_with_data()
        #clear the data for the files
        self.renamer_data.files_to_edit = []
        #clear the gui of the files
        for i in self.file_widgets:
            i.deleteLater()
        self.file_widgets = []
        pass

    def add_file_widget(self, data):
        ''' when a file is added do some checks then add it to the gui '''
        for i in self.file_widgets:
            if i.current_name == data.name_current:
                #printing for testing purposes
                '''NOTE could add this info to the gui but wasn't needed
                based on artist feedback '''
                print '{} already visable'.format(i.current_name)
                return
        #add the file widget to the lsit and the layout
        temp_view_file = view_file_widget(self, data.name_current, data.name_new)
        self.file_widgets.append(temp_view_file)
        self.view.main_layout.addWidget(temp_view_file)
        #bind the remove button to it's method
        temp_view_file.btn_remove.clicked.connect(lambda : self.remove_file_widget(temp_view_file.current_name))
        pass

    def update_new_view(self):
        ''' when the replace line edit is updated update the file widgets and data '''
        #get the find text and replace text
        find_text = self.edit.find_text_field.text()
        replace_text = self.edit.replace_text_field.text()
        #update the data for the files
        self.renamer_data.update_names(find_text, replace_text)
        #update the labels for the file widgets to refelct data change
        for i in self.renamer_data.files_to_edit:
            for j in self.file_widgets:
                if(i.name_current == j.current_name):
                    j.name_new_label.setText(i.name_new)
        pass

    def remove_file_widget(self, current_name):
        ''' When the remove button is clicked update the data and the gui '''
        #printing for testing purposes
        print current_name
        temp = None
        #remove the file data
        for i in self.renamer_data.files_to_edit:
            if(i.name_current == current_name):
                temp = i
                #printing for testing purposes
                print i
        self.renamer_data.remove_file_data(temp)
        #remove the file widget
        for i in self.file_widgets:
            if i.current_name == current_name:
                temp = i
        #printing for testing purposes
        print temp
        temp.deleteLater()
        self.file_widgets.remove(temp)
        pass


class view_widget(QtGui.QWidget):
    ''' class that represents the view section of the gui '''
    def __init__(self, *args):
            super(view_widget, self).__init__(*args)

            #setting a container widget for the scroll bar
            self.widget = QtGui.QWidget()
            self.main_layout = QtGui.QVBoxLayout()
            self.main_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
            self.main_layout.addStretch()
            self.widget.setLayout(self.main_layout)

            #setting up scroll bar
            self.scroll_area = QtGui.QScrollArea()
            self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scroll_area.setWidget(self.widget)
            self.scroll_area.setWidgetResizable(True)

            #making labels that lay above the scroll bar
            self.scroll_layout = QtGui.QVBoxLayout()
            self.scroll_layout.setAlignment(QtCore.Qt.AlignHCenter)
            self.name_label = QtGui.QLabel('Drag and Drop files to start renaming!')
            self.name_label.setStyleSheet(styles.title_labels)
            self.name_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label = QtGui.QLabel("!!!Make sure any files your trying to edit arn't open in another program!!!")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label.setStyleSheet(styles.warning_label)
            #adding the finalize button
            self.btn_finalize = QtGui.QPushButton('Finalize Edits')
            self.btn_finalize.setStyleSheet(styles.btn_finalize)
            self.btn_finalize.setMaximumWidth(120)

            #adding widgets
            self.scroll_layout.addWidget(self.name_label)
            self.scroll_layout.addWidget(self.description_label)
            self.scroll_layout.addWidget(self.btn_finalize)
            self.scroll_layout.addWidget(self.scroll_area)

            self.setLayout(self.scroll_layout)

            #setting the style sheet for the view section
            self.setStyleSheet(styles.view_widget)


class edit_widget(QtGui.QWidget):
    ''' class that represents the edit section of the gui '''
    def __init__(self, *args):
            super(edit_widget, self).__init__(*args)

            #setting main layout and header label for the section
            self.main_layout = QtGui.QVBoxLayout()
            self.setLayout(self.main_layout)
            self.name_label = QtGui.QLabel('Edit Options')
            self.name_label.setStyleSheet(styles.title_labels)
            self.name_label.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.addWidget(self.name_label)

            #setting up a layout for part of the edit section that contains
            #interactable widgets
            self.replace_widget = QtGui.QWidget()
            self.edit_layout = QtGui.QHBoxLayout()
            self.replace_widget.setLayout(self.edit_layout)

            #setting individual layouts for label line edit pairs
            self.find_layout = QtGui.QVBoxLayout()
            self.replace_layout = QtGui.QVBoxLayout()
            self.edit_layout.addLayout(self.find_layout)
            self.edit_layout.addLayout(self.replace_layout)

            #setting descriptive labels
            self.find_label = QtGui.QLabel('Find below text in old file names')
            self.replace_label = QtGui.QLabel('Replace found text with this text')
            self.find_layout.addWidget(self.find_label)
            self.replace_layout.addWidget(self.replace_label)

            #setting line edits and style sheets
            self.find_text_field = QtGui.QLineEdit()
            self.replace_text_field = QtGui.QLineEdit()
            self.find_text_field.setStyleSheet(styles.text_field)
            self.replace_text_field.setStyleSheet(styles.text_field)
            self.find_layout.addWidget(self.find_text_field)
            self.replace_layout.addWidget(self.replace_text_field)

            self.main_layout.addWidget(self.replace_widget)

            #setting style sheet for the edit section
            self.setStyleSheet(styles.edit_widget)


class view_file_widget(QtGui.QWidget):
    ''' class that represents the files for the gui '''
    def __init__(self, main, current_name, new_name, *args):
            super(view_file_widget, self).__init__(*args)

            self.current_name = current_name
            self.new_name = new_name

            #setting main layout and remove button
            self.main_layout = QtGui.QHBoxLayout()
            self.setLayout(self.main_layout)
            self.btn_remove = QtGui.QPushButton("Don't Edit This")
            self.btn_remove.setMaximumWidth(100)
            self.btn_remove.setMinimumWidth(100)
            self.btn_remove.setStyleSheet(styles.btn_remove)
            self.main_layout.addWidget(self.btn_remove)

            #setting the label for current name that can be highlighted
            self.name_current_label = QtGui.QLabel(current_name)
            self.name_current_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            self.main_layout.addWidget(self.name_current_label)

            #setting the label for new name that will update later
            self.name_new_label = QtGui.QLabel(new_name)
            self.main_layout.addWidget(self.name_new_label)

            #setting style sheet for view widgets
            self.setStyleSheet(styles.view_file_widget)