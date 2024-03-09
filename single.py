from pytube import YouTube
from moviepy.editor import *
import re

link = input("Enter the YouTube link: ")

if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
    print("Error: Invalid YouTube link")
    exit()

video_id = None
if "/watch?v=" in link:
    video_id = link.split("/watch?v=")[1][:11]
elif "/v/" in link:
    video_id = link.split("/v/")[1][:11]
elif "youtu.be/" in link:
    video_id = link.split("youtu.be/")[1][:11]

if not video_id:
    print("Error: Unable to extract video ID from link")
    exit()

try:
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    audio_stream = yt.streams.filter(only_audio=True).first()

    audio_file = audio_stream.download()

    audio_clip = AudioFileClip(audio_file)
    audio_clip.write_audiofile(audio_file[:-4] + ".mp3")

    os.remove(audio_file)

    print("Conversion complete!")
except Exception as e:
    print("Error:", e)
