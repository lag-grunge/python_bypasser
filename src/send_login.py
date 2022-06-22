from selenium.webdriver.common.by import By

def sendLogin(driver, user, passwd):
    driver.switch_to.default_content()
    username = driver.find_element(by=By.ID, value="login-username")
    password = driver.find_element(by=By.ID, value="login-password")
    username.send_keys(user)
    password.send_keys(passwd)
    log = driver.find_element(by=By.ID, value="login")
    log.click()

