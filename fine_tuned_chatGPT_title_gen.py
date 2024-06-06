from openai import OpenAI
import csv, os

with open('api_key.txt', 'r') as file:
    key = file.read()

with open('model_name.txt', 'r') as file:
    model_name = file.read()

client = OpenAI(api_key=key)

promptTypes = {
    "驚嘆": "驚嘆語句",
    "疑問": "疑問語句",
    "項目數": "影片中主要內容列表的項目數量",
    "數據": "影片提到的重要數據",
    "轉折": "轉折句",
}

outline_folder = 'testing_compare_outline/'
title_folder = 'testing_compare_title/'
videoDataInputPath = 'testing_compare.csv'
title_count = 5

with open(videoDataInputPath, "r", encoding="utf-8") as videoDataFile:
    videoData = list(csv.reader(videoDataFile))[1:]

for channel, title, processedTitle, prompts, duration, videoId in videoData:
    if videoId != 'evBXDZ1dB_E':
        continue
    with open(os.path.join(outline_folder, videoId + '.txt'), 'r', encoding='utf-8') as file:
        outline = file.read()

    prompt_str = "標題內容需要包含"
    prompts = list(filter(None, prompts.split(" ")))
    for prompt in prompts:
        prompt_str += promptTypes[prompt] + "、"
    prompt_str = prompt_str[:-1] + "。"
    # print(f"#zh-tw 請根據以下的影片摘要想一個吸睛的 YouTube 影片標題。{prompt_str}\n摘要：{outline}")
    # print('---')
    # continue
    titles = []
    for i in range(title_count):
        completion = client.chat.completions.create(
            model=model_name,
            messages = [
                {"role":"system","content":"你是一位在 YouTube 平台上的影音創作者，你擅長撰寫吸引人的影片標題。"},
                {"role":"user", "content": f"#zh-tw 請根據以下影片摘要想一個吸睛的 YouTube 影片標題。{prompt_str}\n摘要：{outline}"}
            ]
        )

        response = completion.choices[0].message.content
        if response[-1] == '\n':
            response = response[:-1]
        titles.append(response)
        print(response)

    with open(os.path.join(title_folder, videoId + '.txt'), 'w', encoding='utf-8') as file:
        file.write('\n'.join(titles))