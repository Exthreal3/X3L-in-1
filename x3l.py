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
class X3L(tk.Tk):
    """_summary_"""
    def __init__(self):
        super().__init__()

        ### TKINTER SETUP ###
        self.title("X3L App Launcher")
        self.geometry("720x480")
        self.resizable(False, False)

        ### BUTTONS ###
        button_ytdlp = tk.Button(
            self,
            text        = "yt-dlp",
            command     = self.launch_ytdlp)
        button_gptpdf = tk.Button(
            self,
            text        = "GPT-PDF",
            command     = self.launch_gptpdf)
        button_ffmpeg = tk.Button(
            self,
            text        = "FFmpeg",
            command     = self.launch_ffmpeg)
        button_exit = tk.Button(
            self,
            text        = "Exit",
            command     = self.destroy)

        ### PLACEMENTS ###
        button_ytdlp.place(
            x       = 70,
            y       = 30,
            anchor  = "center")
        button_ffmpeg.place(
            x       = 160,
            y       = 30,
            anchor  = "center")
        button_gptpdf.place(
            x       = 255,
            y       = 30,
            anchor  = "center")
        button_exit.place(
            x       = 690,
            y       = 20,
            anchor  = "center")

    def launch_ytdlp(self):
        """_summary_"""
        self.withdraw()
        YtdlpApp(self)

    def launch_gptpdf(self):
        """_summary_"""
        self.withdraw()
        GptpdfApp(self)

    def launch_ffmpeg(self):
        """_summary_

        Args:
            input_directory (_type_): _description_
            output_parent_directory (_type_): _description_
        """
        self.withdraw()
        ffmpeg = Ffmpeg(self)
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


class YtdlpApp(tk.Toplevel):
    """_summary_"""
    def __init__(self, main_app):
        super().__init__()

        ### TKINTER SETUP ###
        self.main_app = main_app
        self.title("X3L | yt-dlp")
        self.geometry("720x480")
        self.resizable(False, False)

        ### WIDGETS ###
        # Labels #
        self.title_label            = tk.Label(
            self,
            text        = "")

        # Entries #
        self.url_type               = tk.StringVar(
            value       = "youtube")
        self.url_entry              = tk.Entry(
            self,
            width       = 50)


        # Radios #
        self.radio_youtube          = tk.Radiobutton(
            self, 
            text        = "Youtube", 
            variable    = self.url_type, 
            value       = "youtube")
        self.radio_patreon          = tk.Radiobutton(
            self, 
            text        = "Patreon", 
            variable    = self.url_type, 
            value       = "patreon")

        # Buttons #
        self.download_button        = tk.Button(
            self,
            text        = "Download",
            command     = self.download)
        self.open_folder_button     = tk.Button(
            self, 
            text        = "Open Downloads Folder", 
            command     = self.open_downloads_folder)
        button_return                 = tk.Button(
            self, 
            text        = "Return", 
            command     = self.return_app)

        # Miscellaneous #
        self.progress               = Progressbar(
            self, 
            length      = 100,
            mode        = "determinate")
        self.download_queue         = queue.Queue()
        self.download_thread        = threading.Thread(
            target  = self.process_queue)
        self.download_thread.daemon = True

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

        self.after(100, self.process_queue)

    def return_app(self):
        """_summary_"""
        self.main_app.deiconify()
        self.destroy()

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
            self.after(100, self.process_queue)
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

                self.after(100, check_output)
            else:
                if not process_finished:
                    return_code = process.poll()
                    if return_code is not None:
                        process_finished = True
                        self.download_queue.task_done()
                    self.after(100, self.process_queue)

        check_output()

    def open_downloads_folder(self):
        """_summary_"""
        webbrowser.open("/mnt/sda4")

class GptpdfApp(tk.Toplevel):
    """_summary_"""
    def __init__(self, main_app):
        super().__init__()
        
        ### TKINTER SETUP ###
        self.main_app = main_app
        self.title("X3L | ChatGPT-PDF")
        self.geometry("720x480")
        self.resizable(False, False)

        ### WIDGETS ###
        # Labels #
        self.title_label            = tk.Label(
            self, 
            text        = "")
        
        # Entries #
        # Radios #
        # Buttons #
        button_return                 = tk.Button(
            self, 
            text        = "Return", 
            command     = self.return_app)
        
        # Miscellaneous #
        button_return.place(
            x       = 60,
            y       = 440,
            anchor  = "center")

    def return_app(self):
        """_summary_"""
        self.main_app.deiconify()
        self.destroy()

class Ffmpeg(tk.Toplevel):
    def __init__(self, main_app):
        super().__init__()

        ### TKINTER SETUP ###
        self.main_app = main_app
        self.title("X3L | ffmpeg")
        self.geometry("720x480")
        self.resizable(False, False)

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

    def return_app(self):
        """_summary_"""
        self.main_app.deiconify()
        self.destroy()    

    def select_directory(self):
        """_summary_"""
        self.selected_directory = tkinter.filedialog.askdirectory(title="Select a directory")


if __name__ == "__main__":
    app = X3L()
    app.mainloop()
