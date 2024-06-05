import time, os, csv, collections
import clipboard
import undetected_chromedriver as uc
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PROMPT_LIMIT = 3500


transcription_folder = 'testing_rate_transcription/'
outline_folder = 'outline/'
outline_folder2 = 'outline2/'
files = os.listdir(transcription_folder)

transcriptions = []
prompt = '以下是一部影片的逐字稿，請幫我整理成一段詳細的大綱：'

def get_parts(message: str) -> list[str]:
    cur = 0
    ret = [[prompt]]
    for line in message.split('\n'):
        cur += len(line)
        if cur > PROMPT_LIMIT:
            ret.append([prompt])
            cur = 0
        ret[-1].append(line)
    return ret

for f in files:
    if f[:-4] + '.txt' in os.listdir(outline_folder):
        continue
    print('video id: ' + f[:-4])
    with open(os.path.join(transcription_folder, f), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        transcriptions.append([])
        for row in reader:
            transcriptions[-1].append(row[-1])

    message = '\n'.join(transcriptions[-1])
    # print(message)

    driver = None
    while True:
        driver = uc.Chrome()
        driver.maximize_window()
        driver.get("https://chatgpt.com")

        time.sleep(2)
        if driver.current_url == "https://chatgpt.com/":
            break
        driver.close()

    while True:
        text_areas = driver.find_elements(By.ID, 'prompt-textarea')
        if len(text_areas) > 0:
            break
        time.sleep(0.1)
    text_area = text_areas[0]

    lines = message.split('\n')
    lenSum = sum(len(line) for line in lines)
    extractRatio = (lenSum // PROMPT_LIMIT) + 1
    extractedLines = [line for line in lines if randint(1, extractRatio) == 1]
    assebleLines = '\n'.join(extractedLines)

    extractedLines = [prompt] + extractedLines + ['zh-tw']
    parts = [extractedLines.copy()]

    outlines = []

    for i, part in enumerate(parts):
        clipboard.copy('\n'.join(part))
        text_area.send_keys(Keys.CONTROL, 'v')

        # for line in part:
        #     text_area.send_keys(line)
        #     text_area.send_keys(Keys.SHIFT, Keys.ENTER)

        text_area.send_keys(Keys.RETURN)

        time.sleep(1)
        button_xpath1 = f'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[{i * 2 + 3}]/div/div/div[2]/div[2]/div[2]/div/span/button'
        button_xpath2 = f'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[{i * 2 + 3}]/div/div/div[2]/div[2]/div[2]/div/span'
        arrow_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/button'
        
        while True:
            arrow = driver.find_elements(By.XPATH, arrow_xpath)
            # print(len(copy))
            if len(arrow) > 0:
                time.sleep(1)
                break
            time.sleep(0.1)
        arrow[0].click()

        button_xpath = button_xpath1

        while True:
            copy = driver.find_elements(By.XPATH, button_xpath)
            # print(len(copy))
            if len(copy) > 0:
                time.sleep(1)
                break
            time.sleep(0.1)
        # input()
        driver.find_element(By.XPATH, button_xpath).click()
        # time.sleep(1)
        response = clipboard.paste()
        print(response)
        outlines.append(response)
   
    print(outlines)

    with open(os.path.join(outline_folder, f)[:-4] + '.txt', 'w', encoding='utf-8') as file:
        file.write('\n----------\n'.join(outlines))

    # with open(os.path.join(outline_folder2, f)[:-4] + '.txt', 'w', encoding='utf-8') as file:
    #     file.write('\n----------\n'.join(outlines))
    
    driver.close()
