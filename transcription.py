import whisper
from pytube import YouTube
import csv

# videoDataInputPath = './testing_rate.csv'
# audioOutputDirectory = './testing_rate_audio'
# transcriptionOutputDirectory = './testing_rate_transcription'
videoDataInputPath = './testing_compare.csv'
audioOutputDirectory = './testing_compare_audio'
transcriptionOutputDirectory = './testing_compare_transcription'



# whisperModel = whisper.load_model('tiny')

with open(videoDataInputPath, 'r', encoding='utf-8') as videoDataFile:
    videoData = list(csv.reader(videoDataFile))[1:]

for channel, title, duration, videoID in videoData:
    url = f'https://youtube.com/watch?v={videoID}'
    transcriptionOutputPath = f'{transcriptionOutputDirectory}/{videoID}.csv'

    audio = YouTube(url).streams.get_audio_only()
    audioFilePath = audio.download(output_path=audioOutputDirectory, filename=f'{videoID}.mp3')
    print(f'Audio output: {audioFilePath}')

    # transcription = whisperModel.transcribe(audioFilePath, fp16=False)

    # with open(transcriptionOutputPath, 
    #           'w', encoding='utf-8', newline='') as transcriptionOutputFile:
    #     csvWriter = csv.writer(transcriptionOutputFile)

    #     for segment in transcription['segments']:
    #         csvWriter.writerow([segment['start'], segment['end'], segment['text']])

    # print(f'Transcription output: {transcriptionOutputPath}')