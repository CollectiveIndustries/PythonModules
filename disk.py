#!/usr/bin/python

import json
import ctypes
import os
from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
import com


class prog:
	umount = ['umount']
	lsblk = ['lsblk', '--json', '--noheadings', '-o', 'name,size,model,serial,fstype,label']
	rsync = ['rsync', '--recursive', '--compress-level=9', '--human-readable', '--progress', '--no-perms', '--no-owner', '--no-group', '--no-times', '--ignore-existing', '--exclude-from=/etc/rsync_exclude.conf']
	cp = ['cp', '/media/cw/Drew/Live_USB/scripts/rsync_exclude.conf', '/etc/rsync_exclude.conf']
	ntfs = ['lowntfs-3g', '-o', 'windows_names,ignore_case']
	cifs = ['mount.cifs', '-o', 'username=root,password=cw8400', '//nas/data', '/media/data']

# class container for Ignore lists
# TODO set up regex for these to avoid adding loop0 loop1...loopX

class ignore:
	filesystems = ['iso9660', 'squashfs', 'crypto_LUKS', None, 'swap']
	devices = ['sr0', 'sr1', 'loop0']
	sn = ['C860008AE288B0B109030049']

# Print block file systems
def listFileSystems():
	lsblk = Popen(prog.lsblk, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()
#	print(out)

	try:
		decoded = json.loads(out.decode("utf-8"))


	# Access data
		for x in decoded['blockdevices']:
			if x['name'] not in ignore.devices and x['serial'] not in ignore.sn: # Display valid disks with a SN
				print(com.color.HEADER+"Drive:  "+com.color.OKGREEN+"/dev/"+x['name']+com.color.END)
				print(com.color.HEADER+"Size:   "+com.color.WARNING+x['size']+com.color.END)
				if x['model'] is not None:
					print(com.color.HEADER+"Model:  "+com.color.END+x['model'])
				if x['serial'] is not None:
					print(com.color.HEADER+"Serial: "+com.color.END+x['serial'])
					print("")
				for c in x['children']:
					if c['fstype'] not in ignore.filesystems:
						print('\t'+com.color.UNDERLINE+'Partition:'+com.color.END)
						print("\t"+com.color.HEADER+"Name:  "+com.color.OKGREEN+"/dev/"+c['name']+com.color.END)
						if c['label'] is not None:
							print("\t"+com.color.HEADER+"Label: "+com.color.END+c['label'])

						if c['fstype'] is not None:
							print("\t"+com.color.HEADER+"Type:  "+com.color.END+c['fstype'])
						else:
							print("\t"+com.color.HEADER+"Type:  "+com.color.FAIL+"UNKNOWN"+com.color.END)

						if c['size'] is not None:
							print("\t"+com.color.HEADER+"Size:  "+com.color.WARNING+c['size']+com.color.END)
						else:
							print("\t"+com.color.HEADER+"Size:  "+com.color.FAIL+"UNKNOWN"+com.color.END)

						print("")
			print("") # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
		print(color.FAIL+"There was a problem parsing the JavaScript Object Notation (JSON)"+com.color.END)
		print(ValueError.msg)
		exit(1)

_libc = ctypes.cdll.LoadLibrary("libc.so.6")

# Simple wrapper around mount(2) and umount(2).
# Not thoroughly tested, and not very talkative.

class FLAGS:
    def __new__(self):
        raise NotImplementedError("This class is non-instantiable.")

    def flag_bits(count):
        flag = 1
        for i in range(count):
            yield flag
            flag <<= 1

    (
        MS_RDONLY,      #  0
        MS_NOSUID,      #  1
        MS_NODEV,       #  2
        MS_NOEXEC,      #  3
        MS_SYNCHRONOUS, #  4
        MS_REMOUNT,     #  5
        MS_MANDLOCK,    #  6
        MS_DIRSYNC,     #  7
        _, _,           # SKIP 8, 9
        MS_NOATIME,     # 10
        MS_NODIRATIME,  # 11
        MS_BIND,        # 12
        MS_MOVE,        # 13
        MS_REC,         # 14
        MS_SILENT,      # 15
        MS_POSIXACL,    # 16
        MS_UNBINDABLE,  # 17
        MS_PRIVATE,     # 18
        MS_SLAVE,       # 19
        MS_SHARED,      # 20
        MS_RELATIME,    # 21
        MS_KERNMOUNT,   # 22
        MS_I_VERSION,   # 23
        MS_STRICTATIME, # 24
        _, _, _, _, _,  # SKIP 25-29
        MS_ACTIVE,      # 30
        MS_NOUSER,      # 31
    ) = flag_bits(32)

    del flag_bits, _

    MS_MGC_VAL = 0xc0ed0000
    MS_MGC_MSK = 0xffff0000

def mount(source, target, fstype, flags=0, data=None):
    flags = (flags & FLAGS.MS_MGC_MSK) | FLAGS.MS_MGC_VAL

    result = _libc.mount(ctypes.c_char_p(source), ctypes.c_char_p(target), ctypes.c_char_p(fstype), flags, ctypes.c_char_p(data) if data is not None else 0)

    if result != 0:
        raise OSError(ctypes.get_errno())

def umount(target):
    result = _libc.umount(ctypes.c_char_p(target))

    if result != 0:
	raise OSError(ctypes.get_errno())
