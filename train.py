import os
import csv
import argparse
from transcript.speech2text import downloadAudio, generateTranscript, getTranscriber


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="train.py",
        description="Model training & validation",
        epilog="repo: https://github.com/lnfu/title-generator",
    )
    parser.add_argument("metadata_file", help="The file containing metadata")
    parser.add_argument(
        "-o",
        "--output-directory",
        help="The directory to place audio/transcript/outline/title files into",
    )
    parser.add_argument(
        "-v",
        "--validate",
        action="store_true",
        help="Perform validation instead of training",
    )
    parser.add_argument(
        "-t",
        "--generate-transcript",
        action="store_true",
        help="Generate transcripts from audio if not already available",
    )
    parser.add_argument(
        "-d",
        "--download-audio",
        action="store_true",
        help="Download audio if not already available",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    metadataFilePath = args.metadata_file

    if args.output_directory:
       prefix = os.path.join(args.output_directory, os.path.splitext(metadataFilePath)[0])
    else:
       prefix = os.path.join('data', os.path.splitext(metadataFilePath)[0])

    with open(metadataFilePath, "r", encoding="utf-8") as metadataFile:
        metadata = list(csv.reader(metadataFile))[1:]

    if args.download_audio:
        for channel, title, processedTitle, prompts, duration, videoId in metadata:
            downloadAudio(videoId, os.path.join(prefix, "audio"))

    if args.generate_transcript:
        transcriber = getTranscriber()
        for channel, title, processedTitle, prompts, duration, videoId in metadata:
            generateTranscript(
                transcriber,
                os.path.join(prefix, "audio"),
                videoId,
                os.path.join(prefix, "transcript"),
            )
