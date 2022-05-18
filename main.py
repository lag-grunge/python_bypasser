import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os, sys
import time,requests

#from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject

delayTime = 2
audioToTextDelay = 10
mp3filename = '1.mp3'
byPassUrl = 'https://contributor-accounts.shutterstock.com/login'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

def audioToText(driver):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(googleIBMLink)
    delayTime = 10
    # Upload file
    time.sleep(1)
    # Upload file
    time.sleep(1)
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(os.getcwd() + '/' + mp3filename)
    # Audio to text is processing
    time.sleep(delayTime)
    # Audio to text is processing
    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements(by=By.TAG_NAME, value='span')
    result = " ".join( [ each.text for each in text ] )
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def work(driver, byPassUrl):
    driver.get(byPassUrl)
    time.sleep(1)
    googleClass = driver.find_elements(by=By.CLASS_NAME, value='g-recaptcha')[0]
    time.sleep(2)
    outeriframe = googleClass.find_element(by=By.TAG_NAME, value='iframe')
    time.sleep(1)
    outeriframe.click()
    time.sleep(2)
    allIframes = driver.find_elements(by=By.TAG_NAME, value='iframe')
    time.sleep(1)
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(allIframes)):
        driver.switch_to.default_content()
        iframe = allIframes[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(by=By.ID, value='recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass
    if audioBtnFound:
        try:
            while True:
                href = driver.find_element(by=By.ID, value='audio-source').get_attribute('src')
                response = requests.get(href, stream=True)
                saveFile(response, mp3filename)
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
        except Exception as e:
            print(e)
            print('Caught. Need to change proxy now')
            return 0
    else:
        print('Button not found. This should not happen.')
        return 0

def sendLogin(driver, user, passwrd):
    driver.switch_to.default_content()
    username = driver.find_element(by=By.ID, value="login-username")
    password = driver.find_element(by=By.ID, value="login-password")
    username.send_keys(user)
    password.send_keys(passwrd)
    log = driver.find_element(by=By.ID, value="login")
    log.click()


if __name__ == '__main__':
    assert len(sys.argv) == 3
    with webdriver.Firefox(service=Service(GeckoDriverManager(cache_valid_range=1).install()), options=Options()) as driver:
        while work(driver, byPassUrl) == 0:
            time.sleep(1)
            # cur_proxy = proxies[random.randint(0, len(proxies) - 1)]
            # set_proxy(driver, http_addr=cur_proxy.split(':')[0], http_port=int(cur_proxy.split(':')[1]))
        sendLogin(driver, sys.argv[1], sys.argv[2])
        os.system("read -p 'Press any key' case")
        os.system("rm -f " + mp3filename)
