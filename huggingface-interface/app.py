from transformers import pipeline
import gradio as gr
from video_downloader import download_video, download_youtube_video
from moviepy.editor import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from pydub import AudioSegment
import re

pipe = pipeline("automatic-speech-recognition", model="Artanis1551/whisper_romanian")


def process_video(date):
    # If the date is not in YYYY-MM-DD format, return an error message
    date_pattern = re.compile(r"\b\d{4}\d{2}\d{2}\b")
    if not date_pattern.match(date):
        video_path = download_youtube_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        transcription = "Please enter a date in the format YYYY-MM-DD."
        return video_path, transcription
    try:
        # Download the video
        video_path = download_video(date)

        # Extract the first 30 seconds of the video
        short_video_path = f"short_{date}.mp4"
        ffmpeg_extract_subclip(video_path, 0, 30, targetname=short_video_path)
        video_path = short_video_path

        # Extract audio from the short video
        audio_path = f"audio_{date}.wav"
        AudioFileClip(short_video_path).write_audiofile(audio_path)
        audio = AudioSegment.from_wav(audio_path)

        with open(audio_path, "rb") as audio_file:
            audio = audio_file.read()
        transcription = pipe(audio)["text"]
        # Remove the audio file
        os.remove(audio_path)
    except:
        video_path = download_youtube_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        transcription = "No decision was made on this date."

    return video_path, transcription


iface = gr.Interface(
    fn=process_video,
    inputs=gr.inputs.Textbox(label="Date with format YYYYMMDD"),
    outputs=[
        gr.outputs.Video(),
        gr.Textbox(lines=100, max_lines=100, interactive=True),
    ],
    title="Romanian Transcription Test",
    description="This app transcribes videos from the Romanian Parliament"
    + " on a given date. Only the first 30 seconds of the "
    + "video will be used if it is longer than that.",
)

iface.launch()
