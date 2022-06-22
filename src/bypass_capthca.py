import time
import sys
sys.path.insert(1, './config')
import params
from selenium.webdriver.common.by import By
from audio_to_text import audioToText
import requests
from selenium.webdriver.common.keys import Keys


def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


def getIFrames(driver):

    driver.get(params.byPassUrl)
    time.sleep(1)
    googleClass = driver.find_elements(by=By.CLASS_NAME, value='g-recaptcha')[0]
    time.sleep(2)
    outeriframe = googleClass.find_element(by=By.TAG_NAME, value='iframe')
    time.sleep(1)
    outeriframe.click()
    time.sleep(2)
    allIframes = driver.find_elements(by=By.TAG_NAME, value='iframe')
    time.sleep(1)

    return allIframes

def findBtn(driver, allIframes):

    for index in range(len(allIframes)):
        driver.switch_to.default_content()
        iframe = allIframes[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(params.delayTime)
        try:
            audioBtn = driver.find_element(by=By.ID, value='recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
            audioBtn.click()
            audioBtnIndex = index
            break
        except Exception as e:
            pass
    else:
        return False, -1
    return True, audioBtnIndex


def captchaByPass(driver, audioBtnIndex):
    href = driver.find_element(by=By.ID, value='audio-source').get_attribute('src')
    response = requests.get(href, stream=True)
    saveFile(response, params.mp3filename)
    response = audioToText(driver)
    print(response)
    driver.switch_to.default_content()
    iframe = driver.find_elements(by=By.TAG_NAME, value='iframe')[audioBtnIndex]
    driver.switch_to.frame(iframe)
    inputbtn = driver.find_element(by=By.ID, value='audio-response')
    inputbtn.send_keys(response)
    inputbtn.send_keys(Keys.ENTER)
    time.sleep(2)
    errorMsg = driver.find_elements(by=By.CLASS_NAME, value='rc-audiochallenge-error-message')[0]
    if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
        print("Success")
        return 1
    return 0


def work(driver, byPassUrl):

    try:
        allIframes = getIFrames(driver)
    except:
        print('error of loading page and find frames')
        return 0

    audioBtnFound, audioBtnIndex = findBtn(driver, allIframes)

    if not audioBtnFound:
        print('Button not found. This should not happen.')
        return 0

    try:
        while not captchaByPass(driver, audioBtnIndex):
            pass
    except Exception as e:
        print(e)
        print('Caught. Need to change proxy now')
        return 0
    return 1

