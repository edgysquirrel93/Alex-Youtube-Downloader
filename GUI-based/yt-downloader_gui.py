import yt_dlp
import os
import threading
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
target_folder = os.path.join(downloads_path, "YouTubeDownloads")
os.makedirs(target_folder, exist_ok=True)

root = tk.Tk()
root.title("Alex's youtube downloader")
root.geometry("800x600")  # just for demo

# Create a container frame
container = tk.Frame(root)
container.pack(fill="both", expand=True)  # this centers the frame in the window

inner = tk.Frame(container)
inner.place(relx=0.5, rely=0.5, anchor="center")
disclaimer_text = (
    "Disclaimer: This tool is a user-friendly interface for yt-dlp, an open-source media downloader.\n"
    "It is intended for personal, lawful use only. I do not condone or take responsibility for any misuse,\n"
    "including downloading copyrighted or inappropriate content.\n"
    "Users are responsible for complying with local laws and platform terms of service."
)

tk.Label(
    inner,
    text=disclaimer_text,
    wraplength=600,       # wrap text at 600px
    justify="left",       # left-align text
    fg="gray"             # subtle color
).pack(pady=10)

# Now put all your widgets inside the container
tk.Label(inner, text="Enter YouTube URL:").pack(pady=5)
url_var = tk.StringVar()
url_entry = tk.Entry(inner, width=50, textvariable=url_var)
url_entry.pack(pady=5)

choice_var = tk.StringVar(value="video")
tk.Radiobutton(inner, text="Video", variable=choice_var, value="video").pack(anchor="w")
tk.Radiobutton(inner, text="Audio", variable=choice_var, value="audio").pack(anchor="w")

progress = ttk.Progressbar(inner, length=300, mode="determinate")
progress.pack(pady=10)

status_var = tk.StringVar(value="Idle")
tk.Label(inner, textvariable=status_var).pack(pady=5)

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)

def resize_fonts(event):
    # Scale font size based on window height
    new_size = max(10, event.height // 40)
    default_font.configure(size=new_size)

root.bind("<Configure>", resize_fonts)

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip().replace('%','')
        try:
            progress['value'] = float(percent)
        except ValueError:
            pass
        status_var.set(f"Downloading: {d.get('_percent_str','')} ETA: {d.get('_eta_str','')}")
        root.update_idletasks()
    elif d['status'] == 'finished':
        status_var.set("Download finished. Converting...")

def start_download():
    url = url_entry.get().strip()
    v_or_m = choice_var.get()

    if not url:
        status_var.set("Please enter a URL")
        return

    # Build options
    if v_or_m == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }

    def run():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_var.set("Download complete!")

    threading.Thread(target=run, daemon=True).start()

tk.Button(inner, text="Start Download", command=start_download).pack(pady=10)

root.mainloop()