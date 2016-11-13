#!/usr/bin/env python

#from gooxi_test import *
import os,sys
import time
import pickle
import pexpect

"""
#class G1DCW(tests):
#    def __init__(self):
#        tests.__init__(self)
#        self.get_expect_basic_config()
#       self.is_new_planar_test()
"""
class TestError(Exception):
    pass

class MLBTEST():
    def __init__(self):    
        self.memories = 0
        self.cpu_num = 0
        self.pci_devices = 0
        self.usb_port = 0
        self.sata_port = 0
        self.ncsi_nic = 0

        self.mac_num = 0
        self.planar_code = ""
        self.net_macs = {}
        self.bmc_mac = ''
        self.eth0_mac = ''
        self.eth1_mac = ''
        self.eth2_mac = ''
        self.eth3_mac = ''
        self.eth4_mac = ''
        self.eth5_mac = ''


    def run(self):

        self.init_test()
        self.get_expect_basic_config()
        self.is_new_planar_test()
        self.start_test("Basic Config Check Test")
        self.check_net_macs(self.mac_num+1)

        # basic config check
#        self.check_memories()
        self.check_cpu()
        self.check_pci_device()
        self.check_pci_device_speed()
#        self.check_usb_device()
#        self.check_sata_device()
#
#        # flash process
        self.start_test("Flash Test")       
        self.flash_bmc_mac()
#       skip flash BMC eeprom
        self.flash_os_mac_eeprom()
        self.flash_os_mac()
        self.flash_fe()
        self.flash_pxe()
#
# final verification test
        self.start_test("Final Verification Test")
#        self.check_memories()
        self.check_pci_device()
        self.check_pci_device_speed()
        self.check_fvt_bmc_mac()
        self.check_fvt_pxe()
        self.check_fvt_net_macs()
        self.test_uut_done()

    def run_command( self, cmd, sleep_time=0 ):
        p = os.popen( cmd )
        if sleep_time != 0:
            time.sleep(sleep_time)
        return p.readlines()

    def init_test(self):
        print "1: Start New Test"
        print "2: Go On Original Test"
        input_num = raw_input("Please input 1 or 2 to go on test\n")
        if input_num not in ['1','2']:
            raise TestError, self.print_test_fail("Only accept 1 or 2")
        else:
            if '1' == input_num:
                cmd = "rm *.done > /dev/null 2>&1"
                self.run_command(cmd)
                cmd = "rm *.ini > /dev/null 2>&1"
                self.run_command(cmd)

    def get_expect_basic_config(self):
        self.mac_num = 6
        self.cpu_num = 1
        self.memories = 16
        self.usb_port = 5
        self.pci_devices = 1
        self.sata_port = 2
#        self.planar_code = 'G1DCW'
        self.sata_expect_set = (['sata5','sata6'])

    def is_new_planar_test(self):
        # clear all config file and get ready macs
        if not os.path.exists("net_macs.ini"):
            self.get_macs()
            f = file("net_macs.ini","wb")
            pickle.dump(self.net_macs, f)
            f.close()
            cmd = "sync"  
            self.run_command( cmd )
        else:
            self.get_macs()

    def get_macs(self):

        if os.path.exists("net_macs.ini"):
            self.net_macs_file = open("net_macs.ini", 'rb')
            self.net_macs = pickle.load(self.net_macs_file)
            self.bmc_mac = self.net_macs['bmc_mac'].lower()
            self.eth0_mac = self.net_macs['eth0_mac'].lower()
            self.eth1_mac = self.net_macs['eth1_mac'].lower()
            if self.mac_num == 4:
                self.eth2_mac = self.net_macs['eth2_mac'].lower()
                self.eth3_mac = self.net_macs['eth3_mac'].lower()
            if self.mac_num == 6:
                self.eth2_mac = self.net_macs['eth2_mac'].lower()
                self.eth3_mac = self.net_macs['eth3_mac'].lower()
                self.eth4_mac = self.net_macs['eth4_mac'].lower()
                self.eth5_mac = self.net_macs['eth5_mac'].lower()
            if self.mac_num == 8:
                self.eth2_mac = self.net_macs['eth2_mac'].lower()
                self.eth3_mac = self.net_macs['eth3_mac'].lower()
                self.eth4_mac = self.net_macs['eth4_mac'].lower()
                self.eth5_mac = self.net_macs['eth5_mac'].lower()
                self.eth6_mac = self.net_macs['eth6_mac'].lower()
                self.eth7_mac = self.net_macs['eth7_mac'].lower()
        else:
            self.bmc_mac = raw_input("Please scan BMC MAC ")
            self.net_macs['bmc_mac'] = self.bmc_mac.lower()
            if self.mac_num == 8:
                self.eth0_mac = raw_input("Please scan eth0 MAC ")
                self.net_macs['eth0_mac'] = self.eth0_mac.lower()
                self.eth1_mac = raw_input("Please scan eth1 MAC ")
                self.net_macs['eth1_mac'] = self.eth1_mac.lower()
                self.eth2_mac = raw_input("Please scan eth2 MAC ")
                self.net_macs['eth2_mac'] = self.eth2_mac.lower()
                self.eth3_mac = raw_input("Please scan eth3 MAC ")
                self.net_macs['eth3_mac'] = self.eth3_mac.lower()
                self.eth4_mac = raw_input("Please scan eth4 MAC ")
                self.net_macs['eth4_mac'] = self.eth4_mac.lower()
                self.eth5_mac = raw_input("Please scan eth5 MAC ")
                self.net_macs['eth5_mac'] = self.eth5_mac.lower()
                self.eth6_mac = raw_input("Please scan eth6 MAC ")
                self.net_macs['eth6_mac'] = self.eth6_mac.lower()
                self.eth7_mac = raw_input("Please scan eth7 MAC ")
                self.net_macs['eth7_mac'] = self.eth7_mac.lower()
            if self.mac_num == 6:
                self.eth0_mac = raw_input("Please scan eth0 MAC ")
                self.net_macs['eth0_mac'] = self.eth0_mac.lower()
                self.eth1_mac = raw_input("Please scan eth1 MAC ")
                self.net_macs['eth1_mac'] = self.eth1_mac.lower()
                self.eth2_mac = raw_input("Please scan eth2 MAC ")
                self.net_macs['eth2_mac'] = self.eth2_mac.lower()
                self.eth3_mac = raw_input("Please scan eth3 MAC ")
                self.net_macs['eth3_mac'] = self.eth3_mac.lower()
                self.eth4_mac = raw_input("Please scan eth4 MAC ")
                self.net_macs['eth4_mac'] = self.eth4_mac.lower()
                self.eth5_mac = raw_input("Please scan eth5 MAC ")
                self.net_macs['eth5_mac'] = self.eth5_mac.lower()
            if self.mac_num == 4:
                self.eth0_mac = raw_input("Please scan eth0 MAC ")
                self.net_macs['eth0_mac'] = self.eth0_mac.lower()
                self.eth1_mac = raw_input("Please scan eth1 MAC ")
                self.net_macs['eth1_mac'] = self.eth1_mac.lower()
                self.eth2_mac = raw_input("Please scan eth2 MAC ")
                self.net_macs['eth2_mac'] = self.eth2_mac.lower()
                self.eth3_mac = raw_input("Please scan eth3 MAC ")
                self.net_macs['eth3_mac'] = self.eth3_mac.lower()
            if self.mac_num == 2:
                self.eth0_mac = raw_input("Please scan eth0 MAC ")
                self.net_macs['eth0_mac'] = self.eth0_mac.lower()
                self.eth1_mac = raw_input("Please scan eth1 MAC ")
                self.net_macs['eth1_mac'] = self.eth1_mac.lower()

#######################################################################################
############## check config test, flash test and flash verification test ##############
#######################################################################################
    def start_test(self, test_items):

        print "===" + test_items + "==="

    def check_net_macs(self, no):

        if len(set(self.net_macs.values())) != no:
            cmd = "rm net_macs.ini"
            os.popen( cmd )
            raise TestError, self.print_test_fail("Check MACS failure, has duplicated MAC address,"
                                                  " please input MACs again")

        for mac in self.net_macs.values():
            if len(mac) != 12:
                cmd = "rm net_macs.ini"
                os.popen( cmd )
                raise TestError, self.print_test_fail("Check MAC failure, the MAC length is incorrect, "
                                                       "please correct it")

    def check_memories(self):
        cmd = "dmidecode | grep -A 15 'DMI type 17' | grep 'Speed' | awk -F: '{print $2}'|grep MHz"
        lines = self.run_command(cmd)
        if len(lines) != self.memories:
            self.print_test_fail("Config check test memory failed.")
        for line in lines:
            if line.strip() == 'Unknown' or line.strip() == '65535 MHz':
                self.print_test_fail( "Config check test memory" + str(lines))
        self.print_test_pass( "Config check test memory")

    def check_cpu(self):

        if self.cpu_num <=1:
            self.print_test_pass("Config check test CPU")
            return

        cmd = "dmidecode | grep -A 5 'DMI type 4' | grep 'Intel' | wc -l"
        installed_cpu = int(self.run_command( cmd )[0].strip())
        if self.cpu_num == installed_cpu:
            self.print_test_pass("Config check test CPU")
        else:
            msg = str(installed_cpu) + " CPU found"
            self.print_test_fail("Config check test CPU", msg)

    def check_pci_device(self):

        cmd = "lspci -n -d 1000:0072 | wc -l"
        if int(self.run_command( cmd )[0].strip()) == self.pci_devices:
            self.print_test_pass("Config check test PCI")
        else:
            msg = "PCI device missing"
            raise self.print_test_fail("Check PCI Device failed", msg)


    def check_pci_device_speed(self):

        #
        cmd = "lspci -n -d 1000:0072 -vv | grep Width | grep x8 | wc -l "
        if int(self.run_command( cmd )[0].strip()) != self.pci_devices * 2:
            raise self.print_test_fail("Check PCI Speed failure")
        else:
            self.print_test_pass("Check PCI Speed Pass")

    def check_usb_device(self):

        if self.usb_port <= 2:
            self.print_test_pass("Skip config check USB")
            return
        if os.path.exists("usb_check.done"):
            self.print_test_pass("Check USB device Pass")
            return

        print "We have " + str(self.usb_port - 1) + " ports need to check, please insert USB device one by one"

        cmd = 'lsusb'
        usb_lines = self.run_command(cmd)
        usb_lines = set(usb_lines)
        for port in range(self.usb_port-1):
            while True:
                print "please insert a new device to USB port" + str(port+2)
                time.sleep(1)
                raw_input("Waiting for USB device connected..Please press any key to continue once done\n")

                new_usb_lines = self.run_command(cmd)
                new_usb_lines = set(new_usb_lines)
                usb_device = new_usb_lines - usb_lines
                print usb_device
                if len(usb_device) == 1:
                    print "check USB port pass for port" + str(port+2)
                    flag = usb_device
                    while len(flag) != 0:
                        raw_input("Waiting for USB device disconnected..Please press any key to continue once done")
                        time.sleep(1)
                        newest_usb_lines = self.run_command(cmd)
                        newest_usb_lines = set(newest_usb_lines)
                        flag = newest_usb_lines - usb_lines
                    break
                else:
                    print "\033[1;31;40mFailed: no found USB device...Please re-insert USB disk to USB port\033[0m"
                    continue
        self.run_command("touch usb_check.done")

    def check_sata_device(self):
        if os.path.exists("check_sata_device.done"):
            self.print_test_pass("Check SATA Device Pass")
            return

        while len(self.sata_expect_set) != 0:
            print "Please insert " + str(len(self.sata_expect_set)) + " SATA HDDs"
            time.sleep(3)
            cmd = "ls -l /sys/block/ | grep 'ata' | awk '{print $11}'"
            for line in self.run_command(cmd):
                line = 's' + line.strip().split('/')[4]
                print line + " have been checked"
                try:
                    self.sata_expect_set.remove(line)
                except:
                    pass
            print self.sata_expect_set
        self.run_command("touch check_sata_device.done")
        self.print_test_pass("Check SATA Device")

##### Flash Process

    def flash_bmc_mac(self):

        if os.path.exists("flash_bmc_mac.done"):
            self.print_test_pass("Flash BMC MAC")
            return

        cmd = "ipmitool raw 0x06 0x52 0x07 0xa8 0x00 0x00 0x00" + " 0x"+self.net_macs['bmc_mac'][0:2] + " 0x"+self.net_macs['bmc_mac'][2:4] + \
              " 0x"+self.net_macs['bmc_mac'][4:6] + " 0x"+self.net_macs['bmc_mac'][6:8] + " 0x"+self.net_macs['bmc_mac'][8:10] + " 0x"+self.net_macs['bmc_mac'][10:12]
        print cmd
        self.run_command(cmd, sleep_time=1)
        os.popen('ipmitool raw 06 02')
        cmd = "touch flash_bmc_mac.done"
        self.run_command(cmd)
    def flash_sbmc_mac( self ):

        if os.path.exists("flash_bmc_mac.done"):
            self.print_test_pass("Flash BMC MAC")
            return

        cmds = []
        cmds.append("ipmitool raw 0x0c 0x02 0x01 0xc2 0x00 0x00")
        cmds.append("ipmitool raw 0x0c 0x01 0x01 0xc2 0x00")
        for cmd in cmds:
            print cmd
            self.run_command(cmd)

        cmd = "ipmitool raw 0x0c 0x01 0x01 0x05" + " 0x"+self.bmc_mac[0:2] + " 0x"+self.bmc_mac[2:4] + \
              " 0x"+self.bmc_mac[4:6] + " 0x"+self.bmc_mac[6:8] + " 0x"+self.bmc_mac[8:10] + " 0x"+self.bmc_mac[10:12]
        print cmd
        self.run_command(cmd, sleep_time=1)
        cmd = "touch flash_bmc_mac.done"
        self.run_command(cmd)

    def flash_bmc_eeprom(self):
		
		if os.path.exists("flash_bmc_eeprom.done"):
			self.print_test_pass("Flash BMC EEPROM")
			return
		
		cmd = "ipmitool raw 0x06 0x52 0x0b 0xae 0x00 0x00 0x53 0x59 0x31 0x30 0x31 0x44 0x30 0x34 0x52"
		print cmd
		self.run_command(cmd, sleep_time=1)
		cmd = "touch flash_bmc_eeprom.done"
		self.run_command(cmd)
    def flash_os_mac( self ):


        if os.path.exists("flash_os_mac.done"):
            self.print_test_pass("Flash OS MAC")
            return

        for i in range(self.mac_num):

#             mac = self.net_macs['eth'+str(i)+'_mac']
            if i == 0:
                mac = self.net_macs['eth0_mac']
            if i == 1:
                mac = self.net_macs['eth1_mac']
            if i == 2:
                mac = self.net_macs['eth2_mac']
            if i == 3:
                mac = self.net_macs['eth3_mac']
            if i == 4:
                mac = self.net_macs['eth4_mac']
            if i == 5:
                mac = self.net_macs['eth5_mac']
            if i == 6:
                mac = self.net_macs['eth6_mac']
            if i == 7:
                mac = self.net_macs['eth7_mac']

            cmd = "./eeupdate64e /NIC=" + str(i+1) + " /MAC=" + mac
            print cmd
            self.run_command(cmd, sleep_time=10)
        self.reboot_system("flash_os_mac.done")

    def flash_os_mac_eeprom(self):

        if os.path.exists("flash_os_mac_eeprom.done"):
            self.print_test_pass("Flash OS MAC EEPROM")
            return
        # to make sure flash file I350.hex and I210 is correct.
        cmd = "./eeupdate64e | grep 8086 | awk {'print $1,$6,$7'}"
        print cmd
        lines = self.run_command( cmd )
        if self.mac_num != len(lines):
            self.print_test_fail( "Test Flash OS MAC EEPROM FAILED")
        for line in lines:
    	    print line
            cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " /D "
            if line.find("i350") != -1 or line.find("I350") != -1:
#                cmd = cmd + "I350.hex"
                cmd = cmd + "I350.txt"
                print cmd
                self.run_command(cmd, sleep_time=5)
                cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " -cb 0x03 0x0800"
                self.run_command(cmd, sleep_time=3)
                cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " -ww 0x33 0x4013"
                self.run_command(cmd, sleep_time=3)
                cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " -sb 0x28 0x000D"
                self.run_command(cmd, sleep_time=3)
            elif line.find("I210") != -1:
                cmd = cmd + "I210.bin"
                print cmd
                self.run_command(cmd, sleep_time=5)
            elif line.find("82599") != -1:
                cmd = cmd + "82599.txt"
                print cmd
                self.run_command(cmd, sleep_time=5)
                cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " -cb 0x10 0x800"
                self.run_command(cmd, sleep_time=3)
                cmd = "./eeupdate64e /nic=" + line.strip().split()[0] + " -sb 0x194 0x2600"
                self.run_command(cmd, sleep_time=3)
            elif line.find("82599EB") != -1:
                cmd = cmd + "82599EB.txt"
                self.run_command(cmd, sleep_time=5)
#            print cmd, "flashing OS EEPROM in process"
#            lines = self.run_command(cmd, sleep_time=5)
        self.print_test_pass("Flash OS MAC EEPROM")
        self.softpowercycle_system("flash_os_mac_eeprom.done")
    def flash_fe(self):

        if os.path.exists("flash_fe.done"):
            self.print_test_pass("Flash fe")
            return
        cmd = "./eeupdate64e | grep 8086 | awk {'print $1,$6,$7'}"
        lines = self.run_command( cmd )
        for line in lines:
            if line.find("i350") != -1 or line.find("I350") != -1 or line.find("82599") != -1:
                cmd = "./bootutil64e -nic=" + line.strip().split()[0] + " -fe"
               # print "hi"
                self.run_command(cmd,sleep_time=1)
        self.print_test_pass("Flash fe")
        self.reboot_system("flash_fe.done")

    def flash_pxe(self):

        if os.path.exists("flash_pxe.done"):
            self.print_test_pass("Flash PXE")
            return

        for eth in range(self.mac_num):
            # print eth
            self.update_pxe( eth+1 )
        self.reboot_system("flash_pxe.done")

    def update_pxe(self, eth):

        cmd = "./bootutil64e -nic=%d -up=pxe" %eth
        child = pexpect.spawn( cmd )
        child.logfile = sys.stdout
        time.sleep(1)
        p_expect_line = "Create restore image of NIC %d before proceeding? (Y)es or (N)o: " %eth
        child.expect_exact([p_expect_line])
        child.sendline ("N")
        child.expect_exact("Continue update without restore image? (Y)es or (N)o: ")
        child.sendline ("Y")
        time.sleep(20)
        child.expect_exact("Flash update successful")
        self.check_checksum( eth )

    def check_checksum( self, eth ):

        cmd = "./eeupdate64e /nic=%d /calcchksum" %eth
        print cmd
        lines = self.run_command( cmd )

    def power_cycle_system(self, flag_file):

        f = open(flag_file, 'w')
        f.write( flag_file )
        f.close()
        cmd = "sync"
        self.run_command( cmd )
        while True:
            time.sleep(1)
            print "Please press Ctrl+C, then plug the power cable and insert it back"
            time.sleep(6000)
    def reboot_system(self, flag_file):

        f = open(flag_file, 'w')
        f.write( flag_file )
        f.close()
        cmd = "sync"
        self.run_command( cmd )
        while True:
            time.sleep(1)
            cmd = "reboot"
	    self.run_command(cmd)
            time.sleep(6000)
    def softpowercycle_system(self, flag_file):

        f = open(flag_file, 'w')
        f.write( flag_file )
        f.close()
        cmd = "sync"
        self.run_command( cmd )
        while True:
            time.sleep(1)
            cmd = "ipmitool raw 0 2 2"
	    self.run_command(cmd)
            time.sleep(6000)
#    def power_cycle_system(self):

#       cmd = "sync"
#        self.run_command( cmd )
#        print "Please plug out/in power cable!"
#        time.sleep(36000)
#	self.run_command(cmd)
####### Finally verify mac address for bmc and net

    def check_fvt_bmc_mac(self):
        lines = self.run_command("./bootutil64e | sed -n '10,$'p | awk '{print $2}'")
        for i in lines:
            print i 
        if self.eth0_mac != lines[0].strip().lower() or self.eth1_mac != lines[1].strip().lower() or\
            self.eth2_mac != lines[2].strip().lower() or self.eth3_mac != lines[3].strip().lower():
            self.print_test_fail("FVT check net MAC")           
        else:
            self.print_test_pass("FVT Check net MAC")

    def check_fvt_pxe(self):
        cmd = "./bootutil64e |tail -6 | grep -w PXE"
        lines = self.run_command( cmd )
        if len(lines) != self.mac_num:
            self.print_test_fail("Check FVT PXE")
        else:
            self.print_test_pass("Check FVT PXE")
#######################################################################################
###############  test result function #################################################
#######################################################################################


    def print_test_fail(self, test_item, msg=""):
        msg = "\033[1;31;40mFailed\t%s, %s\033[0m" %(test_item, msg)
        raise TestError, msg

    def print_test_pass(self, test_item):
        # print "debug point"
        print "\033[1;32;40mPass\t%s\033[0m" %test_item

    def test_uut_done(self):

        self.print_test_pass("Test UUT DONE")

def main():
    mlb_test = MLBTEST()  
#    g1dcw_test.run()

if __name__ == '__main__':
    main()
