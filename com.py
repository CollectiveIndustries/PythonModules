#!/usr/bin/python

## Hopefully we can avoid disaster if we dont import this in a main program
import os, shutil, subprocess
from sys import platform

# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
# Located at http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

## OS Specific Stuff
class _OS_(object):
    """Defines an OS environment to work with"""
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

    def ProgExists(self,package):
        def ProgExists(self,package):
        """Checks to see if a program is installed or not"""
        status = subprocess.getstatusoutput("dpkg-query -W -f='${Status}' " + package)
        if not status[0]:
            return '{}Installed{}'.format(color.OKGREEN,color.END) # package is installed
        else:
            return '{}Not Installed{}'.format(color.FAIL,color.END)

    def Clear(self):
        if(self._type_ == "win32"):
            os.system("cls")
        else: # well its not Windows we can just "clear"
            os.system("clear")

    def Shutdown(self):
        if(self._type_ == 'win32'):
            os.system('shutdown', '/s')
        elif(self._type_ == 'debian'):
            os.system('sudo shutdown -h')

    def Reboot(self):
        if(self._type_ == 'win32'):
            os.system('shutdown', '/r')
        elif(self._type_ == 'debian'):
            os.system('sudo reboot')

    def FormatName(self):
        formatstring = "{}{}{}"
        if(self._type_ == "win32"):
            return formatstring.format(color.FAIL,self._type_,color.END)
        elif(self._type_ == "debian"):
            return formatstring.format(color.OKGREEN,self._type_,color.END)
        else:
            return formatstring.format(color.WARNING,self._type_,color.END)

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