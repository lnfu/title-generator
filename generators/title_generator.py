import os
from openai import OpenAI
from utils.common import ensureDirectoryExists, TITLE_TYPE_DESCRIPTIONS


# TODO 看要不要把 outputDirectory 都統一改成 specific 名稱
# TODO 檢查 with open 是不是都是 UTF-8 encode
# TODO MODEL_NAME = os.getenv('FINE_TUNED_MODEL_NAME')
def generateTitle(
    titleCount, titleTypes, modelName, outlineDirectory, videoId, outputDirectory
):
    ensureDirectoryExists(outlineDirectory)
    ensureDirectoryExists(outputDirectory)

    # ChatGPT Client
    client = OpenAI(api_key=os.getenv("API_KEY"))

    # 標題類型
    prmopt = "標題內容需要包含"
    for titleType in titleTypes:
        prmopt += TITLE_TYPE_DESCRIPTIONS[titleType] + "、"
    prmopt = prmopt[:-1] + "。"

    outlineFilePath = os.path.join(outlineDirectory, f"{videoId}.txt")
    titleFilePath = os.path.join(outputDirectory, f"{videoId}.txt")

    # 大綱
    with open(outlineFilePath, "r", encoding="utf-8") as outlineFile:
        outline = outlineFile.read()

    # 產生標題
    titles = []
    for i in range(titleCount):
        completion = client.chat.completions.create(
            model=modelName,
            messages=[
                {
                    "role": "system",
                    "content": "你是一位在 YouTube 平台上的影音創作者，你擅長撰寫吸引人的影片標題。",
                },
                {
                    "role": "user",
                    "content": f"#zh-tw 請根據以下影片摘要想一個吸睛的 YouTube 影片標題。{prmopt}\n摘要：{outline}",
                },
            ],
        )

        response = completion.choices[0].message.content
        if response[-1] == "\n":
            response = response[:-1]
        titles.append(response)

    with open(titleFilePath, "w", encoding="utf-8") as titleFile:
        titleFile.write("\n".join(titles))

    return titles