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

# TODO Make sure that these directories exist before moving files around
def mv(dir_src,dir_dst):
	for file in os.listdir(dir_src):
		print("{}Installing: {}{}".format(color.HEADER,filecolor.END))
		src_file = os.path.join(dir_src, file)
		dst_file = os.path.join(dir_dst, file)
		shutil.copyfile(src_file, dst_file)
