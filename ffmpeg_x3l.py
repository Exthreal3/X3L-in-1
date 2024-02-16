"""_summary_"""

import subprocess
import queue
import threading
import re
import webbrowser
import os
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from os import system
import sys
import tkinter.filedialog




class FormFFmpeg():
    def __init__(self):
        """_summary_"""
        ### TKINTER SETUP ###
        self.root = tk.Tk()
        self.root.title("X3L | ffmpeg")
        self.root.geometry("720x480")
        self.root.resizable(False, False)

        ### WIDGETS ###
        # Labels #
        self.title_label = tk.Label(self, text="")

        # Entries #
        # Radios #
        # Buttons #
        self.button_return = tk.Button(self, text="Return", command=self.return_app)
        self.button_browse = tk.Button(self, text="Browse", command=self.select_directory)

        # Miscellaneous #
        self.button_return.place(x=60, y=440, anchor="center")
        self.button_browse.place(x=360, y=120, anchor="center")

        # Initialize selected directory to None
        self.selected_directory = None

        ffmpeg = FormFFmpeg()
        # Loop through all .mp4 files in the selected directory
        for input_video in os.listdir(self.selected_directory):
            if input_video.endswith(".mp4"):
                # Check if the file is a regular file
                if os.path.isfile(os.path.join(ffmpeg.selected_directory, input_video)):
                    # Extract the file name (without extension) to use as the output directory name
                    output_directory = os.path.join(ffmpeg.selected_directory, os.path.splitext(input_video)[0])

                    # Create a new output directory for each input video
                    os.makedirs(output_directory, exist_ok=True)

                    # Use ffmpeg to create 15-second segments
                    command = [
                        "ffmpeg", "-i", os.path.join(ffmpeg.selected_directory, input_video), "-c", "copy", "-f", "segment",
                        "-segment_time", "15", "-reset_timestamps", "1", "-map", "0", os.path.join(output_directory, "clip_%03d.mp4")
                    ]
                    subprocess.run(command, check=True)


    def return_app(self):
        """_summary_"""
        self.root.deiconify()
        self.root.destroy()

    def select_directory(self):
        """_summary_"""
        self.selected_directory = tkinter.filedialog.askdirectory(title="Select a directory")



