from shutil import copyfile
from distutils.dir_util import copy_tree
import os
import json
from pathlib import Path


class Backup_File:
    def __init__(self):
        self.filename = '.backup.json'
        try:
            self.open_file()
        except FileNotFoundError:
            self.backup = {
                'File': [],
                'Folder': [],
                'ignore': []
            }
        self.set_backup_location()

    def add_items_to_backup(self, file_path):
        if os.path.isdir(file_path):
            file_type = 'Folder'
        else:
            file_type = 'File'

        new_file = {
            'name': file_path.split('/')[-1],
            'path': file_path
        }

        if new_file not in self.backup[file_type]:
            self.backup[file_type].append(new_file)
            self.save_settings()
            return True
        return False

    def check_empty_configuration(self):
        """
        Description:
            Checks if the self.backup variable is an empty configuration.
        Returns:
            <Bool> True if the config is empty and False if it has contents
        """
        for config in self.backup:
            if self.backup[config] != []:
                return False
        return True

    def check_modify_time(self, file_info, timestamp):
        """
        Description:
            Checks if there is a newer version of the file to be backed up
        Args:
            file_info <dict>: The file configuration in self.backup
                e.g {
                    'name': 'file.txt',
                    'path': '/Users/username/Desktop/file.txt',
                    'last_modified': 1517168935.533991
                }
            timestamp <float/int>: the timestamp of the file to be backup
        Returns:
            <Bool> True if the file should be copied or False if not
        """
        if 'last_modified' in file_info:
            if file_info['last_modified'] < timestamp:
                return True
        else:
            return True
        return False

    def copy_files(self):
        for file_info in self.backup['File'] + self.backup['Folder']:

            timestamp = os.stat(file_info['path']).st_mtime
            if file_info['path'] not in self.backup['ignore'] and \
               self.check_modify_time(file_info, timestamp):

                if os.path.isfile(file_info['path']):
                    copyfile(
                        file_info['path'], self.dir_path + file_info['name'])
                else:
                    copy_tree(
                        file_info['path'], self.dir_path + file_info['name'])
                file_info['last_modified'] = timestamp

                print('{} was copied to {}'.format(
                    file_info['name'], self.dir_path))
            else:
                print('{} wasn\'t copied'.format(file_info['name']))
        self.save_settings()

    def delete_from_backup(self, file_path, file_type):
        for files in self.backup[file_type]:
            if file_path == files['path']:
                self.backup[file_type].remove(files)
        self.save_settings()

    def get_config_contents(self):
        return self.backup

    def ignore_files(self, item):
        if item not in self.backup['ignore']:
            self.backup['ignore'].append(item)
            self.save_settings()

    def open_file(self):
        with open(self.filename, 'r') as fh:
            self.backup = json.load(fh)

    def run_setup(self):
        filename = Path(self.filename)
        if not self.check_empty_configuration():
            self.copy_files()
        elif filename.exists():
            self.open_file()
        else:
            print('You need to create a configuration first!')

    def set_backup_location(self, location=None):
        if location:
            self.backup['backup_location'] = self.dir_path = '{}/'.format(
                location)
            self.save_settings()
        else:
            self.dir_path = '{}/'.format(os.getcwd())
            if 'backup_location' in self.backup:
                if os.path.exists(self.backup['backup_location']):
                    self.dir_path = self.backup['backup_location']

    def save_settings(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.backup, fh)
        print('Config file created')


if __name__ == "__main__":
    bf = Backup_File()
    bf.open_file()
