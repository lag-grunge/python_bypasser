import random
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os
import sys
sys.path.insert(1, './config')
import params
import time
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='embody.me@inbox.ru')
    parser.add_argument('--passwd', default='T66PM3NzR7mPmBhd9BugxyTk')
    args = parser.parse_args()
    with webdriver.Firefox(service=Service(GeckoDriverManager(cache_valid_range=1).install()), options=Options()) as driver:
        while work(driver, params.byPassUrl) == 0:
            time.sleep(1)
            # cur_proxy = proxies[random.randint(0, len(proxies) - 1)]
            # set_proxy(driver, http_addr=cur_proxy.split(':')[0], http_port=int(cur_proxy.split(':')[1]))
        sendLogin(driver, args.user, args.passwd)
        os.system("read -p 'Press any key' case")
        os.system("rm -f " + params.mp3filename)
