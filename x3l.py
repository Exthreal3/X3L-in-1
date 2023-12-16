

import tkinter as tk
from tkinter import ttk
import subprocess
import queue
import threading
import re
from os import system
from tkinter.ttk import Progressbar
import webbrowser

class X3L(tk.Tk):
    def __init__(self):
        super().__init__()
        
        ### TKINTER SETUP ###
        self.title("X3L App Launcher")
        self.geometry("720x480")
        self.resizable(False, False)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x3l_width  = 720
        self.x3l_height = 480
        self.x_offset = (self.screen_width - self.x3l_width) // 6
        self.y_offset = (self.screen_height - self.x3l_height) // 4
        self.geometry(f'{self.x3l_width}x{self.x3l_height}+{self.x_offset}+{self.y_offset}') 

        self.lastClickX = 0
        self.lastClickY = 0
        ### BUTTONS ###
        button_ytdlp = tk.Button(
            self, 
            text        = "yt-dlp", 
            command     = self.launch_ytdlp)
        button_gptpdf = tk.Button(
            self, 
            text        = "gptpdf", 
            command     = self.launch_gptpdf)
        button_exit = tk.Button(
            self, 
            text        = "Exit", 
            command     = self.destroy)
        
        ### PLACEMENTS ###
        button_ytdlp.place(
            x       = 360,
            y       = 30,
            anchor  = "center")
        button_gptpdf.place(
            x       = 360,
            y       = 60,
            anchor  = "center")
        button_exit.place(
            x       = 360,
            y       = 90,
            anchor  = "center")

        def SaveLastClickPos(event):
            global lastClickX, lastClickY
            lastClickX = event.x
            lastClickY = event.y

        def Dragging(event):
            x, y = event.x - lastClickX + self.winfo_x(), event.y - lastClickY + self.winfo_y()
            self.geometry('+%s+%s' % (x, y))

        self.bind('<Button-1>', SaveLastClickPos)
        self.bind('<B1-Motion>', Dragging)

        
    def launch_ytdlp(self):
        self.withdraw()
        YtdlpApp(self)

    def launch_gptpdf(self):
        self.withdraw()
        GptpdfApp(self)
        
        
class YtdlpApp(tk.Toplevel):
    def __init__(self, main_app):
        super().__init__()
        
        ### TKINTER SETUP ###
        self.main_app = main_app
        self.title("X3L | yt-dlp")
        self.geometry("720x480")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x3l_width  = 720
        self.x3l_height = 480
        self.x_offset = (self.screen_width - self.x3l_width) // 2
        self.y_offset = (self.screen_height - self.x3l_height) // 2
        self.geometry(f'{self.x3l_width}x{self.x3l_height}+{self.x_offset}+{self.y_offset}') 

        self.lastClickX = 0
        self.lastClickY = 0

        def SaveLastClickPos(event):
            global lastClickX, lastClickY
            lastClickX = event.x
            lastClickY = event.y

        def Dragging(event):
            x, y = event.x - lastClickX + self.winfo_x(), event.y - lastClickY + self.winfo_y()
            self.geometry('+%s+%s' % (x, y))

        self.bind('<Button-1>', SaveLastClickPos)
        self.bind('<B1-Motion>', Dragging)


        ### WIDGETS ###
        # Labels #
        self.title_label            = tk.Label(
            self, 
            text        = "")
        
        # Entries #
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
        self.console                = tk.Text(
            self, 
            height      = 5, 
            state       = tk.DISABLED)
        self.download_queue         = queue.Queue()
        self.download_thread        = threading.Thread(
            target  = self.process_queue)
        self.download_thread.daemon = True
        self.url_type               = tk.StringVar(
            value       = "youtube")
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
        self.console.place(
            x       = 360,
            y       = 300,
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
   
    def return_app(self):
        
        self.main_app.deiconify()
        self.destroy()
        
    def download(self):
        url                     = self.url_entry.get()
        url_type                = self.url_type.get()

        if url_type == 'youtube':
            self.download_youtube(url)
        elif url_type == 'patreon':
            self.download_patreon(url)
        
    def download_youtube(self, url):
        url = self.url_youtube.get()
        command = f"yt-dlp --newline {url}"
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, f"Added to Queue: {url}\n")
        self.console.config(state=tk.DISABLED)
        self.download_queue.put(command)

    def download_patreon(self, url):
        
        if not url.startswith('https://www.patreon.com/'):
            print("Invalid Patreon URL")
            return        
        
        patreon                 = self.url_patreon.get()
        command                 = f"yt-dlp --cookies-from-browser brave --newline {patreon}"
        
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, f"Added to Queue: {patreon}\n")
        self.console.config(state=tk.DISABLED)
        self.download_queue.put(command)

    def process_queue(self):
        try:
            command = self.download_queue.get_nowait()
        except queue.Empty:
            self.after(100, self.process_queue)
            return

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        def check_output():
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
                return_code = process.poll()
                if return_code is not None:
                    self.console.config(state=tk.NORMAL)
                    self.console.delete("1.0", tk.END)
                    self.console.config(state=tk.DISABLED)
                    if return_code != 0:
                        self.console.insert(tk.END, f"Error: {process.stderr.read().decode()}")
                        self.console.see(tk.END)
                    self.download_queue.task_done()
                    self.after(100, self.process_queue)
                    
        check_output()

    def open_downloads_folder(self):
        webbrowser.open("/home/zel")
    
    
class GptpdfApp(tk.Toplevel):
    def __init__(self):
        pass

    pass

if __name__ == "__main__":
    app = X3L()
    app.mainloop()