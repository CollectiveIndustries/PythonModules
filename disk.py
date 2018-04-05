#!/usr/bin/python

import json
import ctypes
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

# mount binding for python
def mount(source, target, fs, options=''):
  ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
  if ret < 0:
    errno = ctypes.get_errno()
    raise RuntimeError("{}Error mounting {} ({}) on {} with options '{}': {}{}".format(com.com.color.FAIL,source, fs, target, options, os.strerror(errno),com.com.color.END))
