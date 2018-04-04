#!/usr/bin/python

##################################################################################################
#
# Copyright (C) Andrew Malone, Collective Industries 2016
#
# AUTHOR: Andrew Malone
#
# TITLE: config
#
# PURPOSE: Configuration file managment
#
#
##################################################################################################

import ConfigParser
import os

ConfigFile = "config.d/conf"

conf = ConfigParser.ConfigParser()
conf.read(os.path.abspath(ConfigFile))
conf.sections()

## Config Parse Helper ##

def ConfigSectionMap(section):
    dict1 = {}
    options = conf.options(section)
    for option in options:
        try:
            dict1[option] = conf.get(section, option)
            if dict1[option] == -1:
                print("Skipping: %s %s" % (section,option))
        except:
            print("Exception on %s %s!" % (section,option))
            dict1[option] = None
    return dict1

## Config section writter ##
def ConfigAddSection(section):
	conf.add_section(section)

def ConfigSetValue(section,key,value):
	conf.set(section,key,value)

def ConfigWrite():
	cfgfile = open(ConfigFile, "wb")
	conf.write(cfgfile)
	cfgfile.close()

# Set up config values

class Settings:
	# MYSQL server config
	MYSQL_HOST_ = ConfigSectionMap("DB")['host']
	MYSQL_USR_ = ConfigSectionMap("DB")['user']
	MYSQL_PASS_ = ConfigSectionMap("DB")['password']
	MYSQL_DB_ = ConfigSectionMap("DB")['database']
	MYSQL_FILE_ = ConfigSectionMap("DB")['sqlconfigfile']
	MYSQL_PORT_ = ConfigSectionMap("DB")['port']

	# Web Site config
	PHP_CONFIG_ = ConfigSectionMap("WEB")['phpconfigfile']
	PHP_REPO_ = ConfigSectionMap("WEB")['phprepo']
	WEB_ROOT_ = ConfigSectionMap("WEB")['webroot']
