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

        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))  # added sticky

        self.folder_label = ttk.Label(
            self.f1, text="Select the folder to backup, One at a time")
        self.folder_button = ttk.Button(
            self.f1, text='Pick Folder', command=self.open_folder_dialogue)

        self.file_label = ttk.Label(self.f1, text="Select the files to backup")
        self.file_button = ttk.Button(
            self.f1, text='Pick Files', command=self.open_file_dialogue)

        self.save_button = ttk.Button(
            self.f1, text="Save Config", command=self.bf.save_settings)
        self.run_button = ttk.Button(
            self.f1, text="Run Backup", command=self.bf.run_setup)

        # TODO: Get this working
        self.progress_bar = ttk.Progressbar(
            self.f1, orient=HORIZONTAL, length=200, mode='determinate')

        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))
        self.folder_label.grid(column=1, row=0, columnspan=2, padx=5)
        self.folder_button.grid(column=1, row=1, columnspan=2, pady=5, padx=5)
        self.file_label.grid(column=1, row=2, columnspan=2, padx=5)
        self.file_button.grid(column=1, row=3, columnspan=2, pady=5, padx=5)
        self.save_button.grid(column=1, row=4, pady=5, padx=5)
        self.run_button.grid(column=2, row=4, pady=5, padx=5)
        self.progress_bar.grid(column=1, row=5, columnspan=2, pady=5)

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
        self.bf.add_files(files)

    def open_folder_dialogue(self):
        folder = filedialog.askdirectory()
        self.bf.add_folder(folder)
