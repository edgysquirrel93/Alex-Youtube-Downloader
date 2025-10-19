import yt_dlp
import os
import sys


downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

target_folder = os.path.join(downloads_path, "YouTubeDownloads")
os.makedirs(target_folder, exist_ok=True)

print("Disclaimer: This tool is a user-friendly interface for yt-dlp, an open-source media downloader.\n"
      "  It is intended for personal, lawful use only.\n"
      "  I do not condone or take responsibility for any misuse, including downloading copyrighted or inappropriate content.\n"
      "  Users are responsible for complying with local laws and platform terms of service.\n")
print("Youtube downloader tool")
print("Made by Alex Albury")
print("")

v_or_m = input("Video or Audio? ").strip().lower()
url = input("Enter YouTube URL: ")

#Progress Bar
class MyLogger:
    def debug(self, msg):
        pass  # Suppress debug output

    def warning(self, msg):
        print(f"Warning: {msg}")

    def error(self, msg):
        print(f"Error: {msg}")

    def info(self, msg):
        print(msg)

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        sys.stdout.write(f"\rDownloading: {percent} at {speed}, ETA: {eta}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\nDownload finished. Converting...")

ydl_opts = {
    'logger': MyLogger(),
    'progress_hooks': [progress_hook],
    'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
}

if v_or_m == "audio":
    ydl_opts = {
        'format': 'bestaudio/best',
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
        'force_generic_extractor': False,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
    }
elif v_or_m == "video":
  ydl_opts = {
      'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
      'merge_output_format': 'mp4',
      'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
      'http_headers': {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
      }
  }
else:
  print("Invalid choice. Please enter 'Video' or 'Audio'.")
  exit()

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("\nDownload complete!")