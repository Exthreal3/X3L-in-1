

import ytdlp
import gptpdf
import tkinter as tk
import subprocess
import queue
import threading
import re
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from os import system


class X3L(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("X3L App Launcher")
        self.geometry("720x480")
        self.resizable(False, False)
        button_ytdlp = tk.Button(X3L, text="yt-dlp", command=self.launch_ytdlp)
        button_gptpdf = tk.Button(X3L, text="gptpdf", command=self.launch_gptpdf)
        button_exit = tk.Button(X3L, text="Exit", command=exit)
        button_ytdlp.place(x=360,y=30,anchor='center')
        button_gptpdf.place(x=360,y=60,anchor='center')
    
    def launch_ytdlp(self):
        # Replace this with code to launch App 1
        app1_window = tk.Toplevel(self)
        app1_window.title("App 1")
        label = tk.Label(app1_window, text="This is App 1")
        label.pack(padx=20, pady=20)

        def download_youtube():
            url = url_entry.get()
            command = f"yt-dlp --newline {url}"
            console.config(state=tk.NORMAL)
            console.insert(tk.END, f'Added to Queue: {url}\n')
            console.config(state=tk.DISABLED)
            download_queue.put(command)

        def download_patreon():
            patreon = url_patreon.get()
            command = f"yt-dlp --cookies-from-browser brave --newline {patreon}"
            console.config(state=tk.NORMAL)
            console.insert(tk.END, f'Added to Queue: {patreon}\n')
            console.config(state=tk.DISABLED)
            download_queue.put(command)

        def process_queue():
            try:
                command = download_queue.get_nowait()
            except queue.Empty:
                ytdlp.after(100, process_queue)
                return

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            def check_output():
                output = process.stdout.readline().decode()
                if output:
                    match = re.search(r'\[download\]\s+(?P<percent>\d+\.\d)%', output)
                    if match:
                        percent = float(match.group('percent'))
                        progress['value'] = percent

                    match = re.search(r'\[download\]\s+Destination:\s+(?P<title>.*)', output)
                    if match:
                        title = match.group('title')
                        title_label['text'] = f'Downloading: {title}'

                    ytdlp.after(100, check_output)
                else:
                    return_code = process.poll()
                    if return_code is not None:
                        console.config(state=tk.NORMAL)
                        console.delete('1.0', tk.END)
                        console.config(state=tk.DISABLED)
                        if return_code != 0:
                            console.insert(tk.END, f'Error: {process.stderr.read().decode()}')
                            console.see(tk.END)
                        download_queue.task_done()
                        process_queue()

            check_output()

        def open_downloads_folder():
            system('dolphin $HOME')

        ytdlp = tk.Tk()
        ytdlp.title("YT-DLP Downloader")
        ytdlp.geometry("720x480")
        ytdlp.resizable(False, False)
        ytdlp.attributes("-topmost", True)

        url_entry = tk.Entry(ytdlp, width=50)
        download_button = tk.Button(ytdlp, text="Download Youtube", command=download_youtube)

        url_entry.place(x=360,y=30,anchor='center')
        download_button.place(x=360,y=60,anchor='center')

        url_patreon = tk.Entry(ytdlp, width=50)
        button_patreon = tk.Button(ytdlp, text="Patreon", command=download_patreon)

        url_patreon.place(x=360,y=120,anchor='center')
        button_patreon.place(x=360,y=150,anchor='center')

        title_label = tk.Label(ytdlp, text='')
        title_label.place(x=360,y=180,anchor='center')

        progress = Progressbar(ytdlp, length=100, mode='determinate')
        progress.place(x=360,y=210,anchor='center')

        open_folder_button = tk.Button(ytdlp, text="Open Downloads Folder", command=open_downloads_folder)
        open_folder_button.place(x=360,y=240,anchor='center')

        console = tk.Text(ytdlp, height=5, state=tk.DISABLED)
        console.place(x=360,y=300,anchor='center')

        download_queue = queue.Queue()
        download_thread = threading.Thread(target=process_queue)
        download_thread.daemon = True
        download_thread.start()

    def launch_gptpdf(self):
        # Replace this with code to launch App 2
        app2_window = tk.Toplevel(self)
        app2_window.title("ChatGPT to PDF")
    
    
if __name__ == "__main__":
    app = X3L()
    app.mainloop()