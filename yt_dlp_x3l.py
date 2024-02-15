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

class FormYtDlp():
    """_summary_"""
    def yt_dlp_form(self):
        """_summary_"""
        self.root.destroy()
        from yt_dlp_x3l import FormYtDlp
        new_form = FormYtDlp
    
    def ffmpeg_form(self):
        
        self.root.destroy()
        from ffmpeg_x3l import FormFFmpeg
        new_form = FormFFmpeg
    
    def imagemagick_form(self):

        self.root.destroy()
        from image_magick_x3l import FormImageMagick
        new_form = FormImageMagick

    def x3l_form(self):

        self.root.destroy()
        from x3l import X3L
        new_form = X3L


    def return_app(self): ## DONE ##
        """_summary_"""
        self.root.deiconify()
        self.root.destroy()

    def download(self):
        """_summary_"""
        url = self.url_entry.get()
        urls = self.url_entry.get().split('\n')
        url_type = self.url_type.get()

        for url in urls:
            if url_type == 'youtube':
                self.download_youtube(url)
            elif url_type == 'patreon':
                self.download_patreon(url)

    def download_youtube(self, urls):
        """_summary_"""
        command = f"yt-dlp -f mp4 --newline {urls}"
        self.download_queue.put((command, urls))

    def download_patreon(self, urls):
        """_summary_"""
        command = f"yt-dlp --cookies-from-browser brave -f mp4 --newline {urls}"
        self.download_queue.put((command, urls))

    def process_queue(self):
        """_summary_"""
        try:
            command, urls = self.download_queue.get_nowait()
        except queue.Empty:
            self.root.after(100, self.process_queue)
            return

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process_finished = False

        def check_output():
            nonlocal process_finished
            output = process.stdout.readline().decode()
            if output:
                match = re.search(r"\[download\]\s+(?P<percent>\d+\.\d)%", output)
                if match:
                    percent = float(match.group("percent"))
                    self.progress["value"] = percent

                match = re.search(r"\[download\]\s+Destination:\s+(?P<title>.*)", output)
                if match:
                    title = match.group("title")
                    self.title_label["text"] = f"Downloading: {title}"

                self.root.after(100, check_output)
            else:
                if not process_finished:
                    return_code = process.poll()
                    if return_code is not None:
                        process_finished = True
                        self.download_queue.task_done()
                    self.root.after(100, self.process_queue)

        check_output()

    def open_downloads_folder(self):
        """_summary_"""
        webbrowser.open("/mnt/sda4")



    def __init__(self):

        ### TKINTER SETUP ###
        self.root = tk.Tk()
        self.root.geometry("720x480")
        self.root.title("X3L | yt-dlp")
        self.root.resizable(False, False)

        ### WIDGETS ###
        # Labels #
        self.title_label            = tk.Label(
            self.root,
            text        = "")

        # Entries #
        self.url_type               = tk.StringVar(
            value       = "youtube")
        self.url_entry              = tk.Entry(
            self.root,
            width       = 50)

        # Radios #
        self.radio_youtube          = tk.Radiobutton(
            self.root, 
            text        = "Youtube", 
            variable    = self.url_type, 
            value       = "youtube")
        self.radio_patreon          = tk.Radiobutton(
            self.root, 
            text        = "Patreon", 
            variable    = self.url_type, 
            value       = "patreon")

        # Buttons #
        self.download_button        = tk.Button(
            self.root,
            text        = "Download",
            command     = self.download)
        self.open_folder_button     = tk.Button(
            self.root, 
            text        = "Open Downloads Folder", 
            command     = self.open_downloads_folder)
        button_return                 = tk.Button(
            self.root, 
            text        = "Return", 
            command     = self.return_app)

        # Miscellaneous #
        self.progress               = Progressbar(
            self.root, 
            length      = 100,
            mode        = "determinate")
        self.download_queue         = queue.Queue()
        self.download_thread        = threading.Thread(
            target  = self.process_queue)
        self.download_thread.daemon = True

        # Start download thread #
        self.download_thread.start()


        ### PLACEMENTS ###
        # Labels #
        self.title_label.place(
            x       = 360,
            y       = 180,
            anchor  = "center")

        # Entries #
        self.url_entry.place(
            x       = 360, 
            y       = 30, 
            anchor  = "center")

        # Miscellaneous #
        self.progress.place(
            x       = 360,
            y       = 210,
            anchor  = "center")

        # Radios #
        self.radio_youtube.place(
            x       = 200, 
            y       = 60, 
            anchor  = "center")
        self.radio_patreon.place(
            x       = 520, 
            y       = 60, 
            anchor  = "center")

        # Buttons #
        self.open_folder_button.place(
            x       = 360,
            y       = 240,
            anchor  = "center")
        self.download_button.place(
            x       = 360, 
            y       = 90, 
            anchor  = "center")
        button_return.place(
            x       = 60,
            y       = 440,
            anchor  = "center")

        self.root.after(100, self.process_queue)
        self.root.mainloop()
