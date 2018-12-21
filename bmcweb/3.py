#encoding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get('http://192.168.1.111')
driver.maximize_window()
driver.implicitly_wait(10)
driver.find_element_by_id('userid').send_keys('admin')
driver.find_element_by_id('password').send_keys('admin')
driver.find_element_by_id('btn-login').click()
driver.implicitly_wait(5)
alert =driver.switch_to_alert()
alert.accept()
time.sleep(10)
ver = driver.find_element_by_id('bios_ver').text
print "The  BIOS version is %s" %ver
driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[1]/div/section/ul/li[12]/a/span').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[2]/div/section[2]/div/div/div[8]/a/span').click()
driver.find_element_by_id('filefirmware_image').send_keys("C:\\Users\\walle\\Desktop\\G2DCN-B13NM.hpm")
time.sleep(5)
driver.find_element_by_id('start').click()
time.sleep(5)
driver.find_element_by_id('proceed').click()
alert =driver.switch_to_alert()
alert.accept()
WebDriverWait(driver,200).until(EC.alert_is_present())
alert =driver.switch_to_alert()
alert.accept()
