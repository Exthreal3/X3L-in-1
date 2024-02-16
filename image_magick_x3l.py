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

class FormImageMagick():
    
    def ffmpeg_form(self):
        
        self.root.destroy()
        from ffmpeg_x3l import FormFFmpeg
        new_form = FormFFmpeg
    
    def yt_dlp_form(self):
        
        self.root.destroy()
        from yt_dlp_x3l import FormYtDlp
        new_form = FormYtDlp
    
    def x3l_form(self):

        self.root.destroy()
        from x3l import X3L
        new_form = X3L

    def __init__(self, master):
        self.root               = tk.Tk()
        self.root.geometry("720x480")
        self.root.resizable(False, False)
        self.root.title("X3L | Image Magick")
        # ^^^ # Form Declaration #
        self.root.mainloop()
