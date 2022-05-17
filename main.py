import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject
import os, sys
import time,requests

from bs4 import BeautifulSoup

delayTime = 2
audioToTextDelay = 10
filename = '1.mp3'
#byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
byPassUrl = 'https://contributor-accounts.shutterstock.com/login'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
option = webdriver.FirefoxOptions()
option.add_argument('--disable-notifications')
option.add_argument("--mute-audio")
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

def audioToText(mp3Path):
    print("1")
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    print("2")
    driver.get(googleIBMLink)
    delayTime = 10
    # Upload file
    time.sleep(1)
    print("3")
    # Upload file
    time.sleep(1)
    root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(os.getcwd() + '/1.mp3')
    # Audio to text is processing
    time.sleep(delayTime)
    #btn.send_keys(path)
    print("4")
    # Audio to text is processing
    time.sleep(audioToTextDelay)
    print("5")
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
    print("5.1")
    result = " ".join( [ each.text for each in text ] )
    print("6")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("7")
    return result


def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def set_proxy(driver, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):

    driver.execute("SET_CONTEXT", {"context": "chrome"})

    try:
        driver.execute_script("""
          Services.prefs.setIntPref('network.proxy.type', 1);
          Services.prefs.setCharPref("network.proxy.http", arguments[0]);
          Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
          Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
          Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
          Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
          Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
          """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)
    finally:
        driver.execute("SET_CONTEXT", {"context": "content"})

driver = webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install(), options=option)

def work(byPassUrl):
    driver.get(byPassUrl)
    time.sleep(1)
    googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
    time.sleep(2)
    outeriframe = googleClass.find_element_by_tag_name('iframe')
    time.sleep(1)
    outeriframe.click()
    time.sleep(2)
    allIframesLen = driver.find_elements_by_tag_name('iframe')
    time.sleep(1)
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(allIframesLen)):
        driver.switch_to.default_content()
        iframe = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass
    if audioBtnFound:
        try:
            while True:
                href = driver.find_element_by_id('audio-source').get_attribute('src')
                response = requests.get(href, stream=True)
                saveFile(response,filename)
                response = audioToText(os.getcwd() + '/' + filename)
                print(response)
                driver.switch_to.default_content()
                iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)
                inputbtn = driver.find_element_by_id('audio-response')
                inputbtn.send_keys(response)
                inputbtn.send_keys(Keys.ENTER)
                time.sleep(2)
                errorMsg = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
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


if __name__ == '__main__':
    proxies = ["mysuperproxy.com:5000", "mysuperproxy.com:5001", "mysuperproxy.com:5100", "mysuperproxy.com:5010",
     "mysuperproxy.com:5050", "mysuperproxy.com:8080", "mysuperproxy.com:8001",
     "mysuperproxy.com:8000", "mysuperproxy.com:8050"]
    while work(byPassUrl) == 0:
        time.sleep(1)
        cur_proxy = proxies[random.randint(0, len(proxies) - 1)]
        set_proxy(driver, http_addr=cur_proxy.split(':')[0], http_port=int(cur_proxy.split(':')[1]))