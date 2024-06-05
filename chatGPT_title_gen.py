import time, os
import clipboard
import undetected_chromedriver as uc
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PROMPT_LIMIT = 3500

outline_folder = 'ok/'
title_folder = 'chatGPT_generated_title/'

files = os.listdir(outline_folder)

transcriptions = []
prompt = '以下是一部影片的大綱，請幫我想一個吸睛的標題：'

for f in files:
    if f in os.listdir(title_folder):
        continue
    print(f[:-4])
    
    outline = ''
    with open(os.path.join(outline_folder, f), 'r', encoding='utf-8') as file:
        outline = file.read()
    
    outline = '\n' * 30 + prompt + '\n' + outline + 'zh-tw'

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

    clipboard.copy(outline)
    text_area.send_keys(Keys.CONTROL, 'v')


    text_area.send_keys(Keys.RETURN)

    time.sleep(1)
    button_xpath1 = '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/span/button'
    button_xpath2 = '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/span'
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

    with open(os.path.join(title_folder, f), 'w', encoding='utf-8') as file:
        file.write(response)

    driver.close()
