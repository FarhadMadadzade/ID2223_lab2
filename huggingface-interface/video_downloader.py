import urllib.request
import requests
from bs4 import BeautifulSoup
from pytube import YouTube


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("No video exists for the given date range.")
            return None
        else:
            print(f"An error occurred while getting the webpage: {e}")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def download_video1(date):
    # Get the webpage
    url = f"https://www.riksdagen.se/sv/sok/?avd=webbtv&from={date}&tom={date}&doktyp=kam-vo"

    soup = get_response(url)
    # Find the download link
    try:
        dateparse = date.replace("-", "")
        video_page = [
            a["href"]
            for a in soup.find_all("a", href=True)
            if a.get("aria-label") and dateparse in a["href"]
        ][0]
        # go to video_page and get all links
        soup = get_response(video_page)
        video_link = [
            a["href"]
            for a in soup.find_all("a", href=True)
            if a["href"].startswith("https://mhdownload.riksdagen.se")
        ][0]
        print(video_link)
    except IndexError:
        print("No video exists for the given date range.")
        return None

    # Download the video
    video_path = f"video_{date}.mp4"
    try:
        urllib.request.urlretrieve(video_link, video_path)
        return video_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None


def download_youtube_video(url):
    try:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video_path = video.download()
        print(f"Video downloaded successfully.")
        return video_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
