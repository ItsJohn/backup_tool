from tkinter import *
from tkinter import ttk, filedialog
import os
import json
from Backup_File import Backup_File


class Create_Window:
    def __init__(self, parent):

        self.bf = Backup_File()

        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background='#334353')
        self.f1 = ttk.Frame(
            self.parent, style='My.TFrame', padding=(3, 3, 12, 12))

        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))

        self.item_backup_label = ttk.Label(
            self.f1, text="Select the items to backup")
        self.folder_button = ttk.Button(
            self.f1, text='Pick Folder', command=self.open_folder_dialogue)
        self.file_button = ttk.Button(
            self.f1, text='Pick Files', command=self.open_file_dialogue)

        self.ignore_label = ttk.Label(
            self.f1, text="Select the items to ignore (Optional)")
        self.ignore_folder_button = ttk.Button(
            self.f1, text='Pick Folder',
            command=self.open_ignore_folder_dialogue)
        self.ignore_file_button = ttk.Button(
            self.f1, text='Pick Files', command=self.open_ignore_file_dialogue)

        backup_text = "Backup location: {}".format(self.bf.dir_path)
        self.backup_loc_label = ttk.Label(self.f1, text=backup_text)
        self.backup_loc_button = ttk.Button(
            self.f1, text="Select backup location",
            command=self.select_backup_location)

        self.save_button = ttk.Button(
            self.f1, text="Save Config", command=self.bf.copy_files)
        self.run_button = ttk.Button(
            self.f1, text="Run Backup", command=self.bf.run_setup)

        # TODO: Get this working
        self.progress_bar = ttk.Progressbar(
            self.f1, orient=HORIZONTAL, length=200, mode='determinate')

        self.tree_column_names = ['Name', 'Path', 'Type', 'Size']
        self.backup_tree = ttk.Treeview(
            self.f1, columns=self.tree_column_names, show="headings")
        self.setup_tree()

        self.delete_button = ttk.Button(
            self.f1,
            text="Delete from backup",
            command=self.delete_from_tree)

        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))
        self.item_backup_label.grid(column=1, row=0, columnspan=2, padx=5)
        self.folder_button.grid(column=1, row=1, pady=5, padx=5, sticky='E')
        self.file_button.grid(column=2, row=1, pady=5, padx=5, sticky='W')
        self.ignore_label.grid(column=1, row=2, columnspan=2, padx=5)
        self.ignore_folder_button.grid(
            column=1, row=3, pady=5, padx=5, sticky='E')
        self.ignore_file_button.grid(
            column=2, row=3, pady=5, padx=5, sticky='W')
        self.backup_loc_label.grid(column=1, row=4, columnspan=2, pady=5)
        self.backup_loc_button.grid(column=1, row=5, columnspan=2, pady=5)
        self.save_button.grid(column=1, row=6, pady=5, padx=5, sticky='E')
        self.run_button.grid(column=2, row=6, pady=5, padx=5, sticky='W')
        self.progress_bar.grid(column=1, row=7, columnspan=2, pady=5)
        self.backup_tree.grid(column=1, row=8, columnspan=2, pady=5)
        self.delete_button.grid(column=1, row=9, columnspan=2, pady=5)

        # added resizing configs
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=3)
        self.f1.columnconfigure(1, weight=3)
        self.f1.columnconfigure(2, weight=3)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(1, weight=1)

    def add_to_tree(self, file_path, tags=tuple()):
        if os.path.isdir(file_path):
            file_type = 'Folder'
        else:
            file_type = 'File'
        filename = file_path.split('/')[-1]
        size = os.path.getsize(file_path)
        self.backup_tree.insert('', 'end', values=(
            filename, file_path, file_type, size), tags=tags)

    def delete_from_tree(self):
        tree_ids = self.backup_tree.selection()
        for tree_id in tree_ids:
            name, file_path, file_type, size = self.backup_tree.item(
                tree_id)['values']
            self.bf.delete_from_backup(file_path, file_type)
            self.backup_tree.delete(tree_id)

    def open_file_dialogue(self):
        files = filedialog.askopenfilenames()
        for file_path in files:
            if self.bf.add_items_to_backup(file_path):
                self.add_to_tree(file_path)

    def open_folder_dialogue(self):
        folder = filedialog.askdirectory()
        if self.bf.add_items_to_backup(folder):
            self.add_to_tree(folder)

    def open_ignore_file_dialogue(self):
        files = filedialog.askopenfilenames()
        for file_path in files:
            self.add_to_tree(file_path, ('ignore',))
            self.bf.ignore_files(file_path)

    def open_ignore_folder_dialogue(self):
        folder = filedialog.askdirectory()
        self.add_to_tree(folder, ('ignore',))
        self.bf.ignore_files(folder)

    def select_backup_location(self):
        backup_location = filedialog.askdirectory()
        self.bf.set_backup_location(backup_location)
        self.backup_loc_label['text'] = "Backup location: {}/".format(
            backup_location)

    def setup_tree(self):
        for column in self.tree_column_names:
            self.backup_tree.heading(column, text=column)
        file_contents = self.bf.get_config_contents()
        self.backup_tree.tag_configure('ignore', background='orange')
        if not self.bf.check_empty_configuration():
            for content in file_contents['File'] + file_contents['Folder']:
                self.add_to_tree(content['path'])
            for content in file_contents['ignore']:
                self.add_to_tree(content, ('ignore',))
