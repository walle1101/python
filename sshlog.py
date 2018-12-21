#!/usr/bin/env python
# encoding: utf-8

from fabric.api import *
from fabric.context_managers import *
env.hosts = ['root@192.168.1.12:22']
env.password = '1'

def setting_ci():
	local('echo "have in 12"')
def update_setting_remote():
	with cd('/root/'):
		run('ls')
def update():
	setting_ci()
	update_setting_remote()
setting_ci()
update_setting_remote()
