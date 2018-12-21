import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get('http://192.168.1.111')
driver.implicitly_wait(10)
driver.maximize_window()
driver.find_element_by_id('userid').send_keys('admin')
driver.find_element_by_id('password').send_keys('admin')
driver.find_element_by_id('btn-login').click()
driver.implicitly_wait(5)
alert =driver.switch_to_alert()
alert.accept()
time.sleep(6)
print driver.find_element_by_id('bios_ver').text
driver.find_element_by_xpath('//*[@id="h5kvm"]/span').click()
windows = driver.window_handles
driver.switch_to_window(windows[-1])
time.sleep(5)
driver.close()
#driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[1]/div/section/ul/li[3]/a/span').click()


