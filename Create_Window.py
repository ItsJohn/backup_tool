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

        self.folder_label = ttk.Label(
            self.f1, text="Select the folder to backup, One at a time")
        self.folder_button = ttk.Button(
            self.f1, text='Pick Folder', command=self.open_folder_dialogue)

        self.file_label = ttk.Label(self.f1, text="Select the files to backup")
        self.file_button = ttk.Button(
            self.f1, text='Pick Files', command=self.open_file_dialogue)

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
        self.folder_label.grid(column=1, row=0, columnspan=2, padx=5)
        self.folder_button.grid(column=1, row=1, columnspan=2, pady=5, padx=5)
        self.file_label.grid(column=1, row=2, columnspan=2, padx=5)
        self.file_button.grid(column=1, row=3, columnspan=2, pady=5, padx=5)
        self.save_button.grid(column=1, row=4, pady=5, padx=5)
        self.run_button.grid(column=2, row=4, pady=5, padx=5)
        self.progress_bar.grid(column=1, row=5, columnspan=2, pady=5)
        self.backup_tree.grid(column=1, row=6, columnspan=2, pady=5)
        self.delete_button.grid(column=1, row=7, columnspan=2, pady=5)

        # added resizing configs
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=3)
        self.f1.columnconfigure(1, weight=3)
        self.f1.columnconfigure(2, weight=3)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(1, weight=1)

    def open_file_dialogue(self):
        files = filedialog.askopenfilenames()
        self.add_to_tree(files, 'File')
        self.bf.add_files(files)

    def open_folder_dialogue(self):
        folder = filedialog.askdirectory()
        self.add_to_tree([folder], 'Folder')
        self.bf.add_folder(folder)

    def setup_tree(self):
        for column in self.tree_column_names:
            self.backup_tree.heading(column, text=column)

    def add_to_tree(self, files, file_type):
        for file_path in files:
            filename = file_path.split('/')[-1]
            size = os.path.getsize(file_path)
            self.backup_tree.insert('', 'end', values=(
                filename, file_path, file_type, size))

    def delete_from_tree(self):
        tree_ids = self.backup_tree.selection()
        for tree_id in tree_ids:
            name, file_path, file_type, size = self.backup_tree.item(
                tree_id)['values']
            self.bf.delete_from_backup(file_path, file_type)
            self.backup_tree.delete(tree_id)
