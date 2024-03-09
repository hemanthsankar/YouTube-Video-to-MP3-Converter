from pytube import YouTube
from moviepy.editor import *
import os
import re

# List of YouTube links
links = [
    "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "https://www.youtube.com/watch?v=aJOTlE1K90k",
    "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    "https://www.youtube.com/watch?v=RgKAFK5djSk",
    "https://www.youtube.com/watch?v=hT_nvWreIhg",
    "https://www.youtube.com/watch?v=T3E9Wjbq44E",
    "https://www.youtube.com/watch?v=50VNCymT-Cs",
    "https://www.youtube.com/watch?v=YykjpeuMNEk"
]

# List to store audio clips
audio_clips = []

for link in links:
    # To check whether the link is a valid YouTube link
    if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
        print(f"Error: Invalid YouTube link: {link}")
        continue

    # Extract the video ID from the link
    video_id = None
    if "/watch?v=" in link:
        video_id = link.split("/watch?v=")[1][:11]
    elif "/v/" in link:
        video_id = link.split("/v/")[1][:11]
    elif "youtu.be/" in link:
        video_id = link.split("youtu.be/")[1][:11]

    if not video_id:
        print(f"Error: Unable to extract video ID from link: {link}")
        continue

    # Create a YouTube object and extract the audio stream
    try:
        yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream as a .mp4 file
        audio_file = audio_stream.download()

        # Use moviepy to convert the .mp4 file to a .mp3 file
        audio_clip = AudioFileClip(audio_file)
        audio_clips.append(audio_clip)  # Add the audio clip to the list

        # Remove the original .mp4 file
        os.remove(audio_file)

        print(f"Conversion complete for {link}!")
    except Exception as e:
        print(f"Error for {link}:", e)

# Merge all audio clips into one
merged_audio = concatenate_audioclips(audio_clips)
merged_audio.write_audiofile("merged_audio.mp3")

print("Merging complete!")
