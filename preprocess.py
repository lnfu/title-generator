import os
import csv
import json
import argparse
from dotenv import load_dotenv
from transcript.speech2text import downloadAudio, generateTranscript, getTranscriber
from outline.outline_gen import generateOutline
from utils.utils import ensureDirectoryExists

promptTypes = {
    "驚嘆": "驚嘆語句",
    "疑問": "疑問語句",
    "項目數": "影片中主要內容列表的項目數量",
    "數據": "影片提到的重要數據",
    "轉折": "轉折句",
}

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
        help="The directory to place audio/transcript/outline/title files into",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    load_dotenv(dotenv_path='.env')
    metadataFilePath = args.metadata_file

    if args.output_directory:
        prefix = os.path.join(
            args.output_directory, os.path.splitext(metadataFilePath)[0]
        )
    else:
        ensureDirectoryExists('data')
        prefix = os.path.join("data", os.path.splitext(metadataFilePath)[0])

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

    # 利用大綱產生 fine tuning dataset
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
            promptStr += promptTypes[prompt] + "、"
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
