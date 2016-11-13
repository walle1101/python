# coding = utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os, time, sys, re,traceback,threading
fp = webdriver.FirefoxProfile(r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\5epvr8je.default')
class Web:
    def __init__(self):
        self.ip = 55
        self.driver = webdriver.Firefox(fp)
        self.base_url = 'http://192.168.1.'

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

    def login(self,username = 'admin',passwod= 'admin'):
        driver = self.driver
        try:
            driver.get(self.base_url+str(self.ip))
            driver.implicitly_wait(10)
            driver.switch_to_frame('MAINFRAME')
            driver.implicitly_wait(2)
            driver.find_element_by_id('login_username').send_keys(username)
            driver.implicitly_wait(2)
            driver.find_element_by_id('login_password').send_keys(passwod)
            time.sleep(1)
            driver.find_element_by_id('LOGIN_VALUE_1').click()
            driver.implicitly_wait(10)
            driver.find_element_by_link_text('Dashboard')
            self.PASS("login")
        except:
            self.FAIL('login')
            traceback.print_exc()

    def kvm(self,username = 'admin',passwod= 'admin'):
        driver = self.driver
        try:
            self.login(username,passwod)
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            driver.implicitly_wait(10)
            driver.find_element_by_id("_btnJava").click()
            print ('PLS wait the popup')
        except:
            self.FAIL('kvm')
            traceback.print_exc()

    def biosupdate(self,username = 'admin',passwod= 'admin'):
        driver = self.driver
        try:
            self.login(username,passwod)
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            time.sleep(5)
            ver = driver.find_element_by_id('_biosRev').text
            print "The  BIOS version is %s" %ver
            driver.implicitly_wait(10)
            driver.switch_to.default_content()
            driver.implicitly_wait(10)
            driver.switch_to_frame('MAINFRAME')
            driver.implicitly_wait(10)
            driver.find_element_by_link_text('Firmware Update').click()
            driver.implicitly_wait(10)
            driver.find_element_by_link_text('BIOS Update').click()
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            driver.find_element_by_id('_btnFWUpdate').click()
            self.alertwait(10)
            driver.implicitly_wait(10)
            driver.find_element_by_id("brwsUpld").send_keys("C:\\Users\\Administrator\\Desktop\\G1DCW120NM.bin")
            driver.find_element_by_css_selector("input[type=\"button\"]").click()
            self.alertwait(100)
            time.sleep(2)
            # driver.quit()
            self.login()
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            time.sleep(5)
            ver = driver.find_element_by_id('_biosRev').text
            print "The new BIOS version is %s" %ver
            self.PASS("biosupdate")
        except :
            self.FAIL('biosupdate')
            traceback.print_exc()


    def bmcupdate(self,username = 'admin',passwod= 'admin'):
        driver = self.driver
        try:
            self.login(username,passwod)
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            time.sleep(5)
            ver = driver.find_element_by_id('_fwRev').text
            print "The  BMC version is %s" %ver
            driver.implicitly_wait(10)
            driver.switch_to.default_content()
            driver.implicitly_wait(10)
            driver.switch_to_frame('MAINFRAME')
            driver.implicitly_wait(10)
            driver.find_element_by_link_text('Firmware Update').click()
            driver.implicitly_wait(10)
            driver.find_element_by_link_text('BMC Firmware Update').click()
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            driver.find_element_by_id('_btnFWUpdate').click()
            self.alertwait(10)
            element=WebDriverWait(driver,120).until(lambda x: x.find_element_by_id("brwsUpld"))
            driver.find_element_by_id("brwsUpld").send_keys("C:\\Users\\Administrator\\Desktop\\G1DCW105a.bin")
            driver.find_element_by_css_selector("input[type=\"button\"]").click()
            element=WebDriverWait(driver,100).until(lambda x: x.find_element_by_id("__proceed"))
            driver.find_element_by_id("__proceed").click()
            self.alertwait(10)
            WebDriverWait(driver,200).until(lambda x: x.find_element_by_id('descFrame'))
            time.sleep(5)
            # driver.quit()
            print 'Resting BMC...',
            time.sleep(120)
            self.login()
            driver.implicitly_wait(10)
            driver.switch_to_frame('pageFrame')
            time.sleep(5)
            ver = driver.find_element_by_id('_fwRev').text
            print "The new BMC version is %s" %ver
            self.PASS("bmcupdate")
        except:
            self.FAIL('bmcupdate')
            traceback.print_exc()

class Mulact:
    def mul(self,ips,f):
        nloops =range(len(ips))
        threads = []
        for i in nloops:
            b = Web() #very import,if not only one window open
            b.ip = ips[i]
            if f == 'login':
                t = threading.Thread(target=b.login)
                threads.append(t)
                continue
            elif f == 'bios':
                t = threading.Thread(target=b.biosupdate)
                threads.append(t)
                continue
            elif f == 'bmc':
                t = threading.Thread(target=b.bmcupdate)
                threads.append(t)
                continue
            elif f == 'kvm':
                t = threading.Thread(target=b.kvm)
                threads.append(t)
                continue
            else:
                print 'Wrong func'

        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()
