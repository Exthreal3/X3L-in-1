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

class X3L():
    """_summary_"""
    def x3l_form(self):
        """_summary_"""
        self.root.destroy()
        from x3l import X3L
        new_form = X3L
    
    def ffmpeg_form(self):
        
        self.root.destroy()
        from ffmpeg_x3l import FormFFmpeg
        new_form = FormFFmpeg
    
    def yt_dlp_form(self):
        
        self.root.destroy()
        from yt_dlp_x3l import FormYtDlp
        new_form = FormYtDlp
    
    def imagemagick_form(self):

        self.root.destroy()
        from image_magick_x3l import FormImageMagick
        new_form = FormImageMagick

    
    def __init__(self):
        ### TKINTER SETUP ###
        self.root = tk.Tk()
        self.root.title("X3L")
        self.root.geometry("720x480")
        self.root.resizable(False, False)

        ### BUTTONS ###
        button_ytdlp = tk.Button(
            self.root,
            text        = "yt-dlp",
            command     = self.yt_dlp_form)
        button_gptpdf = tk.Button(
            self.root,
            text        = "GPT-PDF ( FIX )",
            command     = self.yt_dlp_form)
        button_ffmpeg = tk.Button(
            self.root,
            text        = "FFmpeg",
            command     = self.ffmpeg_form)
        button_exit = tk.Button(
            self.root,
            text        = "Exit",
            command     = self.root.destroy)

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
        self.root.mainloop()

class GptpdfApp():
    """_summary_"""
    def __init__(self,):       
        ### TKINTER SETUP ###
        self.root = tk.Tk()
        self.root.title("X3L | ChatGPT-PDF")
        self.root.geometry("720x480")
        self.root.resizable(False, False)

        ### WIDGETS ###
        # Labels #
        self.title_label            = tk.Label(
            self.root,
            text        = "")
        
        # Entries #
        # Radios #
        # Buttons #
        button_return                 = tk.Button(
            self.root,
            text        = "Return", 
            command     = self.return_app)

        # Miscellaneous #
        button_return.place(
            x       = 60,
            y       = 440,
            anchor  = "center")

    def return_app(self):
        """_summary_"""
        self.root.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    X3L()
