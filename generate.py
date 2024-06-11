import os
import shutil
import argparse
from dotenv import load_dotenv
from utils.common import ensureDirectoryExists, TITLE_TYPE_DESCRIPTIONS
from generators.transcript_generator import (
    generateTranscript,
    getTranscriber,
)
from generators.outline_generator import generateOutline
from generators.title_generator import generateTitle


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="generate.py",
        description="Generate clickable title",
        epilog="repo: https://github.com/lnfu/title-generator",
    )
    parser.add_argument(
        "input-format",
        choices=["transcript", "audio"],
        type=str,
        help="The format of input file",
    )
    parser.add_argument("file", type=str, help="The input file")
    parser.add_argument(
        "-n", "--number", type=int, default=5, help="The number of titles to generate"
    )
    parser.add_argument(
        "-t",
        "--types",
        choices=list(TITLE_TYPE_DESCRIPTIONS.keys()),
        type=int,
        default=5,
        help="The title types you want",
    )
    # TODO type 加上選項
    parser.add_argument(
        "-o",
        "--output-directory",
        help="The directory to place audio/transcript/outline/title files into",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    load_dotenv(dotenv_path=".env")

    outputDirectory = args.output_directory if args.output_directory else "data"
    ensureDirectoryExists(outputDirectory)

    audioDirectory = os.path.join(outputDirectory, "audio")
    transcriptDirectory = os.path.join(outputDirectory, "transcript")
    outlineDirectory = os.path.join(outputDirectory, "outline")
    titleDirectory = os.path.join(outputDirectory, "title")
    ensureDirectoryExists(audioDirectory)
    ensureDirectoryExists(transcriptDirectory)
    ensureDirectoryExists(outlineDirectory)
    ensureDirectoryExists(titleDirectory)

    videoId = os.path.join(outputDirectory, os.path.splitext(args.file)[0])
    extension = os.path.join(outputDirectory, os.path.splitext(args.file)[-1])

    # 把檔案移到工作區
    if args.input_format == "audio":
        if extension != "mp3":
            print(f"檔案格式錯誤")
            exit()
        shutil.copy(args.file, audioDirectory)
    elif args.input_format == "transcript":
        if extension != "srt":
            print(f"檔案格式錯誤")
            exit()
        shutil.copy(args.file, transcriptDirectory)

    # 產生逐字稿
    if args.input_format == "audio":
        transcriber = getTranscriber()
        generateTranscript(
            transcriber,
            audioDirectory,
            videoId,
            transcriptDirectory,
        )

    # 產生大綱
    generateOutline(
        transcriptDirectory,
        videoId,
        outlineDirectory,
    )

    # 產生標題
    titles = generateTitle(
        args.number,
        list(filter(None, args.types.split(","))),
        os.getenv("FINE_TUNED_MODEL_NAME"),
        outlineDirectory,
        videoId,
        titleDirectory,
    )
    for i, title in enumerate(titles):
        print(f"{i+1}\t{title}\n")
