import os
import csv
import torch
from pytube import YouTube
from transformers import pipeline, GenerationConfig


whisperPretrainedModel = "openai/whisper-small"
whisperModel = "Jingmiao/whisper-small-zh_tw"


def ___downloadAudioFile(videoId, outputDirectory):
    url = f"https://youtube.com/watch?v={videoId}"
    audio = YouTube(url).streams.get_audio_only()
    audioFilePath = audio.download(
        output_path=outputDirectory, filename=f"{videoId}.mp3"
    )
    return audioFilePath


def __getDirectoryPrefix(metadataFilePath):
    return os.path.splitext(metadataFilePath)[0]


def downloadAudio(metadataFilePath):
    with open(metadataFilePath, "r", encoding="utf-8") as metadataFile:
        metadata = list(csv.reader(metadataFile))[1:]

    audioDirectory = os.path.join(
        "data", __getDirectoryPrefix(metadataFilePath) + "_" + "audio"
    )

    if not os.path.exists(audioDirectory):
        os.makedirs(audioDirectory)
        print(f"Directory '{audioDirectory}' created.")
    else:
        print(f"Directory '{audioDirectory}' already exists.")

    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        audioFilePath = os.path.join(audioDirectory, f"{videoId}.mp3")
        if os.path.exists(audioFilePath):
            continue
        ___downloadAudioFile(videoId, audioDirectory)
        print(f"Audio output: {audioFilePath}")


def generateTranscript(metadataFilePath):
    with open(metadataFilePath, "r", encoding="utf-8") as metadataFile:
        metadata = list(csv.reader(metadataFile))[1:]

    transcriptionDirectory = os.path.join(
        "data", __getDirectoryPrefix(metadataFilePath) + "_" + "transcription"
    )
    audioDirectory = os.path.join(
        "data", __getDirectoryPrefix(metadataFilePath) + "_" + "audio"
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    transcriber = pipeline(
        "automatic-speech-recognition", model=whisperModel, device=device
    )
    transcriber.model.generation_config = GenerationConfig.from_pretrained(
        whisperPretrainedModel
    )

    print(f"Use: {device}")

    for channel, title, processedTitle, prompts, duration, videoId in metadata:

        audioFilePath = os.path.join(audioDirectory, f"{videoId}.mp3")
        transcriptionFilePath = os.path.join(transcriptionDirectory, f"{videoId}.srt")

        if os.path.exists(transcriptionFilePath):
            continue

        transcription = transcriber(audioFilePath, return_timestamps=True)

        with open(
            transcriptionFilePath, "w", encoding="utf-8", newline=""
        ) as transcriptionFile:

            for idx, chunk in enumerate(transcription["chunks"]):
                start, end = chunk["timestamp"]
                text = chunk["text"]
                transcriptionFile.write(f"{idx + 1}\n{start} --> {end}\n{text}\n\n")

        print(f"Transcription output: {transcriptionFilePath}")
