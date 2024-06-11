import os
import csv
import argparse
from dotenv import load_dotenv
from generators.transcript_generator import (
    downloadAudio,
    generateTranscript,
    getTranscriber,
)
from generators.outline_generator import generateOutline
from generators.title_generator import generateTitle
from utils.common import ensureDirectoryExists


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="test.py",
        description="Test fine-tuned model",
        epilog="repo: https://github.com/lnfu/title-generator",
    )
    parser.add_argument("metadata_file", help="The file containing metadata")
    parser.add_argument(
        "-o",
        "--output-directory",
        help="The directory to place audio/transcript/outline/title files into",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    load_dotenv(dotenv_path=".env")
    metadataFilePath = args.metadata_file

    base = os.path.splitext(os.path.basename(metadataFilePath))[0]
    outputDirectory = args.output_directory if args.output_directory else "data"
    prefix = os.path.join(outputDirectory, os.path.basename(metadataFilePath)[0])
    ensureDirectoryExists(outputDirectory)
    ensureDirectoryExists(prefix)

    with open(metadataFilePath, "r", encoding="utf-8") as metadataFile:
        metadata = list(csv.reader(metadataFile))[1:]

    # 產生逐字稿
    transcriber = getTranscriber()
    audioDirectory = os.path.join(prefix, "audio")
    transcriptionDirectory = os.path.join(prefix, "transcript")
    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        audioFilePath = os.path.join(audioDirectory, f"{videoId}.mp3")
        transcriptionFilePath = os.path.join(transcriptionDirectory, f"{videoId}.srt")
        # 檢查逐字稿是否已經存在
        if not os.path.exists(transcriptionFilePath):
            print(f"{transcriptionFilePath} 不存在，正在產生逐字稿")
            # 檢查音檔是否已經存在
            if not os.path.exists(audioFilePath):
                print(f"{audioFilePath} 不存在，正在下載音檔")
                downloadAudio(videoId, audioDirectory)
            # 產生逐字稿
            generateTranscript(
                transcriber,
                audioDirectory,
                videoId,
                transcriptionDirectory,
            )

    # 根據逐字稿產生大綱
    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        generateOutline(
            os.path.join(prefix, "transcript"),
            videoId,
            os.path.join(prefix, "outline"),
        )

    # 產生標題
    with open(os.path.join(prefix, "result.csv"), "w", newline="", encoding="utf-8") as resultFile:
        writer = csv.writer(resultFile)

        for channel, title, processedTitle, titleTypes, duration, videoId in metadata:
            titleTypes = list(filter(None, titleTypes.split(" ")))
            oriGPTTitle = generateTitle(
                1,
                titleTypes,
                "gpt-3.5-turbo",
                os.path.join(prefix, "outline"),
                videoId,
                os.path.join(prefix, "title_oriGPT"),
            )[0]
            ftGPTTitle = generateTitle(
                1,
                titleTypes,
                os.getenv("FINE_TUNED_MODEL_NAME"),
                os.path.join(prefix, "outline"),
                videoId,
                os.path.join(prefix, "title_ftGPT"),
            )[0]
            writer.writerow([processedTitle, oriGPTTitle, ftGPTTitle])
