import urllib.request
from pytube import YouTube
import os
import glob


def download_video(date):
    # Delete any existing .mp4 files
    for mp4_file in glob.glob("*.mp4"):
        os.remove(mp4_file)

    year = date[:4]
    url = f"https://www.cdep.ro/u02/comisii/{year}/cp46_{date}.mp4"
    try:
        urllib.request.urlretrieve(url, f"video_{date}.mp4")
        print("Video downloaded successfully.")
        return f"video_{date}.mp4"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No video exists for the given date.")
        else:
            print(f"An error occurred while downloading the video: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def download_youtube_video(url):
    try:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video_path = video.download()
        print(f"Video downloaded successfully.")
        return video_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")


download_video("20230503")
