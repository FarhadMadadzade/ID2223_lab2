from transformers import pipeline
import gradio as gr
import time
from video_downloader import download_video1, download_youtube_video
from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import datetime
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import re

pipe = pipeline("automatic-speech-recognition", model="Artanis1551/whisper_swedish")


def process_video1(date):
    # If the date is not in YYYY-MM-DD format, return an error message
    date_pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
    if not date_pattern.match(date):
        video_path = download_youtube_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        transcription = "Please enter a date in the format YYYY-MM-DD."
        return video_path, transcription
    try:
        video_path = download_video1(date)

        # Get the duration of the video
        video = VideoFileClip(video_path)
        duration = video.duration

        # If the video is longer than 30 seconds, only take the first 30 seconds
        if duration > 30:
            video_path = f"short_{date}.mp4"
            ffmpeg_extract_subclip(video_path, 0, 30, targetname=video_path)

        # Extract audio from the video
        audio_path = f"audio_{date}.wav"
        AudioFileClip(video_path).write_audiofile(audio_path)

        # Split the audio into chunks
        audio = AudioSegment.from_wav(audio_path)
        chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)

        # Transcribe each chunk
        transcription = ""
        for i, chunk in enumerate(chunks):
            chunk.export(f"chunk{i}.wav", format="wav")
            with open(f"chunk{i}.wav", "rb") as audio_file:
                audio = audio_file.read()
            transcription += pipe(audio)["text"] + "\n "
            os.remove(f"chunk{i}.wav")

        # Remove the audio file
        os.remove(audio_path)
    except:
        video_path = download_youtube_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        transcription = "No decision was made on this date."

    return video_path, transcription


iface = gr.Interface(
    fn=process_video1,
    inputs=[
        gr.inputs.Textbox(label="Date with format YYYY-MM-DD"),
    ],
    outputs=[
        gr.outputs.Video(),
        gr.Textbox(lines=100, max_lines=100, interactive=True),
    ],
    title="Transcribe Swedish Parliament Decisions",
    description="This app transcribes the top Swedish Parliament decision"
    + " video from the given date. Only the first 30 seconds of the "
    + "video will be used if it is longer than that.",
)

iface.launch()
