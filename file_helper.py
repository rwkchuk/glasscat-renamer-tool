''' this set of python modules helps to manipulate files but manly renameing '''
import sys
import os

class file_data:
    ''' holds info about files for the renamer tool '''
    def __init__(self, name_current='',file_path='', *args, **kwargs):
        self.name_current = name_current
        self.name_new = self.name_current
        self.file_path = file_path


class file_renamer:
    ''' collections and methods to aid file renaming '''
    def __init__(self, *args, **kwargs):
        self.files_to_edit = []

    #adding to old list
    def add_file_data(self, path):
        '''take a file path and make a file_data thats added to files_to_edit'''
        if(self.check_for_existing_file_data(path)):
            print '{} already stored'.format(path)
            return
        temp_file_data = file_data(os.path.basename(path), path)
        self.files_to_edit.append(temp_file_data)
        pass

    #remove from old list
    def remove_file_data(self, data):
        '''take in an old name and remove that from the files_to_edit'''
        print data
        self.files_to_edit.remove(data)
        pass

    #check for duplicate
    def check_for_existing_file_data(self, path):
        '''take in file name and check against name_current'''
        for i in self.files_to_edit:
            if i.file_path == path:
                return True
        return False

    #check if file cant be edited
    #TODO maybe check status and not editability maybe in file_handler
    def check_for_file_editability(self):
        '''take in file_data and check os for status'''
        pass

    def update_system_with_data(self):
        for i in self.files_to_edit:
            old_path = i.file_path
            print old_path
            new_path = i.file_path.replace(i.file_path.split('/')[-1], i.name_new)
            print new_path
            os.rename(old_path, new_path)

    #need to traverse files_to_edit and edit each name_new
    def update_names(self, find_text, replace_text):
        '''take in string modifier and use against name_old for each file'''
        for i in self.files_to_edit:
            text = str.partition(i.name_new,'.')
            print text
            print find_text + '___' + replace_text
            new_name = text[0].replace(find_text, replace_text)
            print new_name + '---'
            i.name_new = new_name+text[1]+text[2]
        pass


class file_handler:
    ''' used for finding and manipulating files in the system '''
    def __init__(self, *args, **kwargs):
        #TODO might need for environment variables and paths and junk
        pass

    #TODO I need to know what the gui needs to display files

    #update file
    #check file status