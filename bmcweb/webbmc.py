#encoding: utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os, time, sys, re,traceback,threading
class Web:
    def __init__(self):
        self.ip = 1.111
        self.driver = webdriver.Chrome()
        self.base_url = 'http://192.168.'

    def PASS(self,testname):
        print "*"*100
        print '\033[42m'+"IP: %s,%s is PASS" %(self.base_url+str(self.ip),testname)+'\033[0m'
        print "*"*100

    def FAIL(self,testname):
        self.driver.get_screenshot_as_file(r'D:\py\screenshot\%s.png' %testname)
        print "*"*100
        print '\033[41m'+"IP: %s,%s is Failed,please see screenshot at D:\py\screenshot\%s.png"\
                         %(self.base_url+str(self.ip),testname,self.base_url+str(self.ip)+testname)+'\033[0m'
        print "*"*100


    def alertwait(self, wt):
        for i in range(0,wt*2):
            time.sleep(0.5)
            try:
                alert = self.driver.switch_to_alert()
                alert.accept()
                break
            except:
                continue

    def login(self, username='admin', passwod='admin'):
        driver = self.driver
        try:
            driver.get(self.base_url + str(self.ip))
            driver.maximize_window()
            driver.implicitly_wait(10)
            driver.find_element_by_id('userid').send_keys('admin')
            driver.find_element_by_id('password').send_keys('admin')
            driver.find_element_by_id('btn-login').click()
            driver.implicitly_wait(5)
            alert = driver.switch_to_alert()
            alert.accept()
            time.sleep(8)
        except:
            self.FAIL('login')
            traceback.print_exc()

    def kvm(self, username='admin', passwod='admin'):
        driver = self.driver
        try:
            self.login(username, passwod)
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="h5kvm"]/span').click()
            windows = driver.window_handles
            driver.switch_to_window(windows[-1])
        except:
            self.FAIL('kvm')
            traceback.print_exc()

    def bmcupdate(self, username='admin', passwod='admin'):
        driver = self.driver
        try:
            self.login(username, passwod)
            driver.implicitly_wait(10)
            ver =  driver.find_element_by_id('fw_ver').text
            print "The  BMC version is %s" % ver
            driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[1]/div/section/ul/li[12]/a/span').click()
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[2]/div/section[2]/div/div/div[7]/a/span').click()
            driver.find_element_by_id('filefirmware_image').send_keys("C:\\Users\\walle\\Desktop\\G2DCN172a.ima")
            time.sleep(5)
            driver.find_element_by_id('start').click()
            alert = driver.switch_to_alert()
            alert.accept()
            # WebDriverWait(driver,60).until(EC.text_to_be_present_in_element((By.LINK_TEXT)))
            WebDriverWait(driver, 200).until(lambda x: x.find_element_by_link_text(u'更新所选的部分'))
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="start"]').click()
            WebDriverWait(driver, 60).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert.accept()
            print 'Resting BMC...',
            time.sleep(120)
            self.login()
            ver = driver.find_element_by_id('fw_ver').text
            print "The new BMC version is %s" % ver
            self.PASS("bmcupdate")
        except:
            self.FAIL('bmcupdate')
            traceback.print_exc()

    def biosupdate(self, username='admin', passwod='admin'):
        driver = self.driver
        try:
            self.login(username, passwod)
            driver.implicitly_wait(10)
            ver = driver.find_element_by_id('bios_ver').text
            print "The  BIOS version is %s" % ver
            driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[1]/div/section/ul/li[12]/a/span').click()
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="main"]/div/div/aside[2]/div/section[2]/div/div/div[8]/a/span').click()
            driver.find_element_by_id('filefirmware_image').send_keys("C:\\Users\\walle\\Desktop\\G2DCN-B13NM.hpm")
            time.sleep(5)
            driver.find_element_by_id('start').click()
            time.sleep(5)
            driver.find_element_by_id('proceed').click()
            alert = driver.switch_to_alert()
            alert.accept()
            WebDriverWait(driver, 300).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert.accept()
            time.sleep(15)
            self.login()
            driver.implicitly_wait(10)
            ver = driver.find_element_by_id('bios_ver').text
            print "The  New BIOS version is %s" % ver
            self.PASS("biosupdate")
        except :
            self.FAIL('biosupdate')
            traceback.print_exc()