import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = uc.Chrome()
browser.maximize_window()
browser.get("https:/chat.openai.com")

while True:
    text_areas = browser.find_elements(By.ID, 'prompt-textarea')
    if len(text_areas) > 0:
        break
    time.sleep(0.1)

text_area = text_areas[0]
text_area.send_keys('hi')
text_area.send_keys(Keys.RETURN)
time.sleep(1)

sensitive_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[1]/div/div/div'


while True:
    copy = browser.find_elements(By.XPATH, sensitive_xpath)
    # print(len(copy))
    if len(copy) > 0:
        break
    time.sleep(0.1)

copy = browser.find_elements(By.XPATH, sensitive_xpath)


response = browser.find_elements(By.TAG_NAME, 'p')

print(response[-2].text)