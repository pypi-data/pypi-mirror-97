#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, random
import traceback as _traceback_

# inc imports.
from fil3s import *

# functions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")
def __get_source_path__(package_name, back=1):
	executive_dir = str(pathlib.Path(__file__).absolute()).replace(os.path.basename(pathlib.Path(__file__)), '').replace("//","/")
	if executive_dir[len(executive_dir)-1] == "/": executive_dir = executive_dir[:-1]
	source, c = "/", 1
	for id in executive_dir.split("/"):
		if id == package_name:
			if c == index:
				source += id+"/"
				break
			else: c += 1
		else: source += id+"/"
	base = source[:-1].split("/")
	base = source.replace(f'/{base[len(base)-1]}/', '/')
	return source, base
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()
def __check_alias__(
	# the source name.
	alias=None, 
	# the source path.
	executable=None,
):
	present = "--create-alias" in sys.argv and cl1.get_argument("--create-alias") == alias
	base = f"/usr/local/bin"
	if not Files.exists(base):
		base = f"/usr/bin/"
	path = f"{base}/{alias}"
	if present or not Files.exists(path):
		file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nos.system("python3 "+package+" "+s)"""

		os.system(f"touch {path}")
		os.system(f"chmod +x {path}")
		os.system(f"chown {USER}:{GROUP} {path}")
		try:
			File(path=f"{path}", data=file).save()
		except:
			print(f"Unable to create alias $ {alias}.")
			return None
		os.system(f"chmod +x {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")
	if present:
		quit()

# source.
ALIAS = SOURCE_NAME = "r3sponse"
SOURCE_PATH = __get_source_path__(__file__, back=3)
BASE = __get_source_path__(SOURCE_PATH)
OS = __get_operating_system__()
#__check_alias__(alias=ALIAS, executable=f"{SOURCE_PATH}/")

# options.
ERROR_TRACEBACK = os.environ.get("R3SPONSE_ERROR_TRACEBACK")
if str(ERROR_TRACEBACK) in ["True", "true", True]: ERROR_TRACEBACK = True
else: ERROR_TRACEBACK = False

# universal variables.
USER = OWNER = os.environ.get("USER")
GROUP = "root"
HOME = os.environ.get('HOME')
HOME_BASE = gfp.base(path=HOME)
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["macos"]: 	
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

