def generateOutline():
    import os
    from random import randint
    from openai import OpenAI
    from dotenv import load_dotenv


    load_dotenv(dotenv_path='.env')

    API_KEY = os.getenv('API_KEY')
    MODEL_NAME = 'gpt-3.5-turbo'

    client = OpenAI(api_key=API_KEY)

    PROMPT_LIMIT = 3500


    transcriptionFile = 'data/transcription.srt'
    outlineFile = 'data/outline.txt'

    prompt = '以下是一部影片的逐字稿，請幫我整理成一段詳細的大綱：'

    with open(transcriptionFile, 'r', encoding='utf-8') as file:
        parts = file.read()

    lines = []
    for part in parts.split('\n\n'):
        lines += part.split('\n')[2:]

    lenSum = sum(len(line) for line in lines)
    extractRatio = (lenSum // PROMPT_LIMIT) + 1
    extractedLines = [line for line in lines if randint(1, extractRatio) == 1]

    extractedLines = [prompt] + extractedLines + ['#zh-tw']

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role":"system","content":"你擅長整理很長的文字並產生大綱。"},
            {"role":"user", "content": '\n'.join(extractedLines)}
        ]
    )

    response = completion.choices[0].message.content
    if response[-1] == '\n':
        response = response[:-1]

    outline = response
    # print(response)

    with open(outlineFile, 'w', encoding='utf-8') as file:
        file.write(outline)
