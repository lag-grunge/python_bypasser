import time
import sys
sys.path.insert(1, './config')
import params
from selenium.webdriver.common.by import By
import os


def audioToText(driver):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(params.googleIBMLink)
    # Upload file
    time.sleep(1)
    # Upload file
    time.sleep(1)
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(os.getcwd() + '/' + params.mp3filename)
    # Audio to text is processing
    time.sleep(params.audio_delayTime)
    # Audio to text is processing
    time.sleep(params.audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements(by=By.TAG_NAME, value='span')
    result = " ".join( [ each.text for each in text ] )
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


