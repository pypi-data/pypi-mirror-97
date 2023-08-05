#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# defaults.
import os,sys,json,pathlib,platform
def __get_argument__(argument, required=True, index=1, default=None):

	# check presence.
	if argument not in sys.argv:
		if required:
			raise ValueError(f"Define parameter [{argument}].")
		else: return empty

	# retrieve.
	y = 0
	for x in sys.argv:
		try:
			if x == argument: return sys.argv[y+index]
		except IndexError:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty
		y += 1

	# should not happen.
	return empty
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")
def __check_alias__(
	# the source name.
	alias=None, 
	# the source path.
	executable=None,
):
	present = "--create-alias" in sys.argv and __get_argument__("--create-alias") == alias
	base = f"/usr/local/bin"
	if not os.path.exists(str(base)):
		base = f"/usr/bin/"
	path = f"{base}/{alias}"
	overwrite = "--overwrite" in sys.argv
	if (("--force" in sys.argv or "--forced" in sys.argv or overwrite) and present) or (present or not os.path.exists(str(path))):
		file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nif os.path.exists("/usr/bin/python3"): os.system("/usr/bin/python3 "+package+" "+s)\nelse:  os.system("python3 "+package+" "+s)"""
		sudo = Boolean("--sudo" in sys.argv).string(true="sudo ",false="")
		os.system(f"{sudo}touch {path}")
		os.system(f"{sudo}chmod +x {path}")
		os.system(f"{sudo}chown {USER}:{GROUP} {path}")
		try:
			File(path=f"{path}", data=file).save()
		except:
			print(f"Unable to create alias $ {alias}.")
			return None
		os.system(f"{sudo}chmod +x {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")
	if present:
		sys.exit(0)

# source.
from fil3s import *
ALIAS = "syst3m"
SOURCE_NAME = "syst3m"
SOURCE_PATH = gfp.base(path=__file__, back=3)
OS = __get_operating_system__()

# imports.
try: 

	# pip imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, time, random, threading, urllib, flask, logging, multiprocessing

	# inc imports.
	import cl1
	from fil3s import *
	from r3sponse import r3sponse

# download.
except ImportError as e:
	import os
	if os.path.exists("/usr/bin/pip3"): 
		os.system(f"/usr/bin/pip3 install -r {FilePath(__file__).base(back=3)}/requirements/requirements.pip --user {os.environ.get('USER')}")
	else:
		os.system(f"pip3 install -r {FilePath(__file__).base(back=3)}/requirements/requirements.pip")

	# pip imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, time, random, threading, urllib, flask, logging, multiprocessing

	# inc imports.
	import cl1
	from fil3s import *
	from r3sponse import r3sponse

# imports.
from r3sponse import ResponseObject

# universal variables.
USER = os.environ.get("USER")
OWNER = os.environ.get("USER")
GROUP = "root"
HOME = os.environ.get('HOME')
HOME_BASE = gfp.base(path=HOME)
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["macos"]: 
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

# check alias.
__check_alias__(SOURCE_NAME,f"{SOURCE_PATH}")