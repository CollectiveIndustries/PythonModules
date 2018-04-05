#!/usr/bin/python

## Hopefully we can avoid disaster if we dont import this in a main program
try:
  config
except NameError:
  import config

import MySQLdb
import subprocess
import os, shutil
from getpass import getpass

## MySQL init function added an error handler + a config data setting dump should be able to use this for all python database connections
def MySQL_init():
	output = subprocess.check_output(['ps', '-A'])
	if 'mysqld' in output:
    		print("MariaDB/MySQL is up an running!")
	else:
		print("MariaDB/MySQL is NOT running...fixing!")
		subprocess.call(['service','mysql','start'])

	while True:

    ## Set up the Connection using config.d/NAME.conf returns a standard DB Object
		try:
			db = MySQLdb.connect(host=config.settings.MYSQL_HOST_,user=config.settings.MYSQL_USR_,passwd=config.settings.MYSQL_PASS_,db=config.settings.MYSQL_DB_)
			# Values must be correct, if values were wrong a MySQLdb.Error would have been thrown
			# lets write out the new configuration values.
#			config.ConfigAddSection("DB")
			config.ConfigSetValue("DB","host",config.settings.MYSQL_HOST_)
			config.ConfigSetValue("DB","user",config.settings.MYSQL_USR_)
			config.ConfigSetValue("DB","password",config.settings.MYSQL_PASS_)
			config.ConfigSetValue("DB","database",config.settings.MYSQL_DB_)
#			config.ConfigSetValue("DB","port",config.settings.MYSQL_PORT_) # this setting looks to be unused at the moment however at some time in the future it should be configurable.
			config.ConfigWrite() # Write file with proper values now that weve updated everything.

			return db # Return the DB connection Object

		except MySQLdb.Error:
			print "There was a problem in connecting to the database."
			print "Config DUMP:"
			print "HOST: %s\nUSER: %s\nPASS: %s\nDATABASE: %s" %(config.settings.MYSQL_HOST_,config.settings.MYSQL_USR_,config.settings.MYSQL_PASS_,config.settings.MYSQL_DB_)
			print "Please Enter the correct login credentials below.\nRequired items are marked in "+color.FAIL+"RED"+color.END+" Any default values will be marked with []\n Once correct values are configured the installer will update the configuration file: "+config.ConfigFile

			## > fix values here < ##

			config.settings.MYSQL_HOST_ = None
			config.settings.MYSQL_USR_ = None
			config.settings.MYSQL_PASS_ = None
			config.settings.MYSQL_DB_ = None

			# After restting variables to None we need to prompt the user for each one and try again.

			while ((config.settings.MYSQL_HOST_ is None) or (config.settings.MYSQL_HOST_=='')):
				config.settings.MYSQL_HOST_ = raw_input(color.FAIL+"Mysql Server Host (example.com) []: "+color.END)
			while ((config.settings.MYSQL_DB_ is None) or (config.settings.MYSQL_DB_ == '')):
				config.settings.MYSQL_DB_ = raw_input(color.FAIL+"Name of Database []: "+color.END)
			while ((config.settings.MYSQL_USR_ is None) or (config.settings.MYSQL_USR_ == '')):
				config.settings.MYSQL_USR_ = raw_input(color.FAIL+"Username []: "+color.END)
			while ((config.settings.MYSQL_PASS_ is None) or (config.settings.MYSQL_PASS_ == '')):
				config.settings.MYSQL_PASS_ = getpass(color.FAIL+"Password []: "+color.END)
			pass
		except MySQLdb.Warning: # Silently ignore Warnings
			break
