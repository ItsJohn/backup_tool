from shutil import copyfile
from distutils.dir_util import copy_tree
import os
import json


class Backup_File:
    def __init__(self):
        self.filename = '.backup.json'
        self.dir_path = os.getcwd() + '/'
        self.backup = {
            'single_files': [],
            'folders': [],
            'ignore': []
        }

    def copy_files(self):
        # TODO: Add last modified into json here
        for files in self.backup['single_files'] + self.backup['folders']:

            last_modified = os.stat(files['path']).st_mtime

            if files['name'] not in self.backup['ignore'] and \
               files['last_modified'] < last_modified:

                if os.path.isfile(files['path']):
                    copyfile(files['path'], self.dir_path + files['name'])
                else:
                    copy_tree(files['path'], self.dir_path + files['name'])

                print('{} was copied to {}'.format(
                    files['name'], self.dir_path))
            else:
                print('{} wasn\'t copied'.format(files['name']))

    def open_file(self):
        with open(self.filename, 'r') as fh:
            self.backup = json.load(fh)
        self.copy_files()

    def add_files(self, files):
        file_list = list()

        for file_path in files:
            self.backup['single_files'].append({
                'name': file_path.split('/')[-1],
                'path': file_path,
                'last_modified': os.stat(file_path).st_mtime
            })

    def add_folder(self, folder):
        self.backup['folders'].append({
            'name': folder.split('/')[-1],
            'path': folder,
            'last_modified': os.stat(folder).st_mtime
        })

    def save_settings(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.backup, fh)
        self.copy_files()

    def run_setup(self):
        if os.path.isfile(self.filename):
            self.open_file()


if __name__ == "__main__":
    bf = Backup_File()
    bf.open_file()
