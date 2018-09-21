#!/usr/bin/python

## Hopefully we can avoid disaster if we dont import this in a main program
import os, shutil
from sys import platform

## OS Specific Stuff
class _OS_(object):
    def __init__(self):
        _SystemOS_ = platform.strip()
        if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
        # linux
            with open('/etc/os-release') as file:
                oper = file.readlines()
                oper = oper[5].split('=')
                self._type_ = oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
        elif(_SystemOS_ == 'win32'):
            self._type_ = _SystemOS_
        
    def Clear(self):
        if(self._type_ == "win32"):
            os.system("cls")
        else: # well its not Windows we can just "clear"
            os.system("clear")

    def Shutdown(self):
        if(_OS_._type_ == 'win32'):
            os.system('shutdown', '/s')
        elif(_OS_._type_ == 'debian'):
            os.system('sudo shutdown -h')

    def Reboot(self):
        if(_OS_._type_ == 'win32'):
            os.system('shutdown', '/r')
        elif(_OS_._type_ == 'debian'):
            os.system('sudo reboot')

     # TODO Make sure that these directories exist before moving files around
#    def mv(dir_src,dir_dst):
#        for file in os.listdir(dir_src):
#            print("{}Installing: {}{}".format(color.HEADER,file,color.END))
#            src_file = os.path.join(dir_src, file)
#            dst_file = os.path.join(dir_dst, file)
#            shutil.copyfile(src_file, dst_file)

            ## END OF _OS_ CLASS

# Text output color definitions
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def shellQoute(str):
	return "'" + str.replace("'", "'\\''") + "'"