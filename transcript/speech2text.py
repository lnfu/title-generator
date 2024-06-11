import os
import torch
from pytube import YouTube
from transformers import pipeline, GenerationConfig
from utils.utils import ensureDirectoryExists

whisperPretrainedModel = "openai/whisper-small"
whisperModel = "Jingmiao/whisper-small-zh_tw"


def downloadAudio(videoId, outputDirectory):
    # 檢查目錄
    ensureDirectoryExists(outputDirectory)

    # 取得 YouTube 影片音訊 (mp3)
    url = f"https://youtube.com/watch?v={videoId}"
    audio = YouTube(url).streams.get_audio_only()
    audioFilePath = audio.download(
        output_path=outputDirectory, filename=f"{videoId}.mp3"
    )
    print(f"Audio: {audioFilePath}", flush=True)
    return audioFilePath


def getTranscriber():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    transcriber = pipeline(
        "automatic-speech-recognition", model=whisperModel, device=device
    )
    transcriber.model.generation_config = GenerationConfig.from_pretrained(
        whisperPretrainedModel
    )
    print(f"Use: {device}", flush=True)
    return transcriber


def generateTranscript(transcriber, audioDirectory, videoId, outputDirectory):
    # 檢查目錄
    ensureDirectoryExists(audioDirectory)
    ensureDirectoryExists(outputDirectory)

    audioFilePath = os.path.join(audioDirectory, f"{videoId}.mp3")
    transcriptionFilePath = os.path.join(outputDirectory, f"{videoId}.srt")

    # 檢查音訊檔案是否存在
    if not os.path.exists(audioFilePath):
        print(f"{audioFilePath} not exist", flush=True)
        return

    # 將語音轉換為文字
    transcription = transcriber(audioFilePath, return_timestamps=True)

    with open(
        transcriptionFilePath, "w", encoding="utf-8", newline=""
    ) as transcriptionFile:
        for idx, chunk in enumerate(transcription["chunks"]):
            start, end = chunk["timestamp"]
            text = chunk["text"]
            transcriptionFile.write(f"{idx + 1}\n{start} --> {end}\n{text}\n\n")

    print(f"Transcription: {transcriptionFilePath}", flush=True)
    return transcriptionFilePath
