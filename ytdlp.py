
class Ytdlp:
    

    pass


import tkinter as tk
import subprocess
import queue
import threading
import re
from tkinter.ttk import Progressbar
from os import system

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



def run():
    ytdlp.mainloop()