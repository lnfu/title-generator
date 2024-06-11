import os
import csv
import json
import argparse
from dotenv import load_dotenv
from generators.transcript_generator import (
    downloadAudio,
    generateTranscript,
    getTranscriber,
)
from generators.outline_generator import generateOutline
from utils.common import ensureDirectoryExists, TITLE_TYPE_DESCRIPTIONS

systemContent = "你是一位在 YouTube 平台上的影音創作者，你擅長撰寫吸引人的影片標題。"


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="preprocess.py",
        description="Prepare traning dataset",
        epilog="repo: https://github.com/lnfu/title-generator",
    )
    parser.add_argument("metadata_file", help="The file containing metadata")
    parser.add_argument(
        "-o",
        "--output-directory",
        help="The directory to place audio/transcript/outline/dataset files into",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    load_dotenv(dotenv_path=".env")
    metadataFilePath = args.metadata_file

    base = os.path.splitext(os.path.basename(metadataFilePath))[0]
    outputDirectory = args.output_directory if args.output_directory else "data"
    prefix = os.path.join(outputDirectory, base)
    ensureDirectoryExists(outputDirectory)
    ensureDirectoryExists(prefix)

    with open(metadataFilePath, "r", encoding="utf-8") as metadataFile:
        metadata = list(csv.reader(metadataFile))[1:]

    # 產生逐字稿
    transcriber = getTranscriber()
    audioDirectory = os.path.join(prefix, "audio")
    transcriptDirectory = os.path.join(prefix, "transcript")
    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        audioFilePath = os.path.join(audioDirectory, f"{videoId}.mp3")
        transcriptFilePath = os.path.join(transcriptDirectory, f"{videoId}.srt")
        # 檢查逐字稿是否已經存在
        if not os.path.exists(transcriptFilePath):
            print(f"{transcriptFilePath} 不存在，正在產生逐字稿")
            # 檢查音檔是否已經存在
            if not os.path.exists(audioFilePath):
                print(f"{audioFilePath} 不存在，正在下載音檔")
                downloadAudio(videoId, audioDirectory)
            # 產生逐字稿
            generateTranscript(
                transcriber,
                audioDirectory,
                videoId,
                transcriptDirectory,
            )

    # 根據逐字稿產生大綱
    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        generateOutline(
            os.path.join(prefix, "transcript"),
            videoId,
            os.path.join(prefix, "outline"),
        )

    # 利用大綱和原標題產生 fine tuning dataset
    datasetFilePath = os.path.join(prefix, "dataset.jsonl")
    for channel, title, processedTitle, prompts, duration, videoId in metadata:
        outlineFilePath = os.path.join(
            os.path.join(prefix, "outline"), videoId + ".txt"
        )
        with open(
            outlineFilePath,
            "r",
            encoding="utf-8",
        ) as outlineFile:
            outline = outlineFile.read()

        promptStr = "標題內容需要包含"
        prompts = list(filter(None, prompts.split(" ")))
        for prompt in prompts:
            promptStr += TITLE_TYPE_DESCRIPTIONS[prompt] + "、"
        promptStr = promptStr[:-1] + "。"

        data = {
            "messages": [
                {
                    "role": "system",
                    "content": systemContent,
                },
                {
                    "role": "user",
                    "content": f"""#zh-tw 請根據以下影片摘要想一個吸睛的 YouTube 影片標題。{promptStr}
                    摘要：{outline}""",
                },
                {"role": "assistant", "content": f"{processedTitle}"},
            ]
        }

        with open(datasetFilePath, "a", encoding="utf-8") as datasetFile:
            json.dump(
                data,
                datasetFile,
                ensure_ascii=False,
                indent=None,
                separators=(",", ":"),
            )
            datasetFile.write("\n")

        print(videoId)
    print(f"Preprocessing complete. Dataset is at {datasetFilePath}")
