import os
from openai import OpenAI
from dotenv import load_dotenv


def generateTitle(titleCount, outlineDirectory, videoId, outputDirectory):

    # ChatGPT Client
    API_KEY = os.getenv("API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"

    client = OpenAI(api_key=API_KEY)

    outlineFile = "data/outline.txt"
    promptFile = "data/prompt.txt"
    titleFile = "data/title.txt"

    promptTypes = {
        "驚嘆": "驚嘆語句",
        "疑問": "疑問語句",
        "項目數": "影片中主要內容列表的項目數量",
        "數據": "影片提到的重要數據",
        "轉折": "轉折句",
    }

    prompts = ""
    if os.path.exists(promptFile):
        with open(promptFile, "r", encoding="utf-8") as file:
            prompts = file.read()
    with open(outlineFile, "r", encoding="utf-8") as file:
        outline = file.read()

    prompt_str = "標題內容需要包含"
    prompts = list(filter(None, prompts.split(" ")))
    for prompt in prompts:
        prompt_str += promptTypes[prompt] + "、"
    prompt_str = prompt_str[:-1] + "。"

    titles = []
    for i in range(titleCount):
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "你是一位在 YouTube 平台上的影音創作者，你擅長撰寫吸引人的影片標題。",
                },
                {
                    "role": "user",
                    "content": f"#zh-tw 請根據以下影片摘要想一個吸睛的 YouTube 影片標題。{prompt_str}\n摘要：{outline}",
                },
            ],
        )

        response = completion.choices[0].message.content
        if response[-1] == "\n":
            response = response[:-1]
        titles.append(response)
        # print(response)

    with open(titleFile, "w", encoding="utf-8") as file:
        file.write("\n".join(titles))
