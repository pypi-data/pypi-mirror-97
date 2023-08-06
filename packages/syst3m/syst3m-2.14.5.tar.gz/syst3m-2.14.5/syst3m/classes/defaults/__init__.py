#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import utils, console
from syst3m.classes.env import env
import platform 

# vars.
vars = r3sponse.ResponseObject({
	"os": platform.system().lower(),
	"user": os.environ.get("USER"),
	"owner": os.environ.get("USER"),
	"group": "root",
	"media": f"/media/{os.environ.get('USER')}",
	"homes": gfp.base(path=os.environ.get('HOME')),
	"home": gfp.clean(os.environ.get('HOME')+"/"),
	"python3":"python3",
})
if vars.os in ["darwin"]:  
	vars.os = "macos"
	vars.group = "staff"
	vars.media = f"/Volumes/"
	vars.python3 = f"/usr/bin/python3"

# universal options.
options = r3sponse.ResponseObject({
	"interactive": not cl1.arguments_present(["--non-interactive"]) and env.get("INTERACTIVE", format=bool, default=False) == True,
	"cli": env.get_boolean("CLI", default=False),
	"json": cl1.arguments_present(["-j", "--json"]),
	"log_level": int(cl1.get_argument("--log-level", required=False, default=env.get_integer("LOG_LEVEL", default=0))),
})

# get operating system.
def operating_system(supported=["*"]):
	os = vars.os
	if os in ["macos"] and ("*" in supported or os in supported): return "macos"
	elif os in ["linux"] and ("*" in supported or os in supported): return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# create alias.
def alias(
	# the source name.
	alias=None, 
	# the source path.
	executable=None,
	# can use sudo.
	sudo=False,
	# overwrite.
	overwrite=False,
):
	l_alias = cl1.get_argument("--create-alias", required=False)
	present = "--create-alias" in sys.argv and l_alias == alias
	base = f"/usr/local/bin"
	if not Files.exists(base):
		base = f"/usr/bin/"
	path = f"{base}/{alias}"
	if ((cl1.argument_present("--force") or cl1.argument_present("--forced") or overwrite) and present) or (present or not Files.exists(path)):
		if l_alias != None: alias = l_alias
		#file = f"""package={executable}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
		sudo = Boolean("--sudo" in sys.argv).string(true="sudo ",false="")
		file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nif os.path.exists("/usr/bin/python3"): os.system("/usr/bin/python3 "+package+" "+s)\nelse:  os.system("python3 "+package+" "+s)"""
		os.system(f"{sudo}touch {path}")
		os.system(f"{sudo}chmod +x {path}")
		os.system(f"{sudo}chown {vars.user}:{vars.group} {path}")
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

# get source path.
def source_path(path, back=1):
	source = gfp.clean(path=FilePath(path).base(back=back), remove_double_slash=True)
	if len(source) > 0 and source[len(source)-1] != "/": source += "/"
	return source

# get log level.
def log_level(default=0):
	return int(cl1.get_argument("--log-level", required=False, default=env.get_integer("LOG_LEVEL", default=0)))

# get current working directory.
def pwd():
	return FilePath(utils.__execute_script__("pwd").replace("\n","")).clean()

# kill pids.
def kill(
	# option 1:
	# the process id.
	pid=None, 
	# option 2:
	# all processes that includes.
	includes=None,
	# root permission required.
	sudo=False,
	# loader.
	log_level=0,
):
	# kill includes.
	loader = None
	if includes != None:
		response = processes(includes=includes, sudo=sudo)
		if not response.success: return response
		c = 0
		for pid, info in response.processes.items():
			response = kill(sudo=sudo, pid=pid, loader=loader)
			if not response.success: return response
			c += 1
		if c == 0:
			return r3sponse.error(f"No processes found.")
		elif c == 1:
			return r3sponse.success(f"Successfully killed {c} process.")
		else:
			return r3sponse.success(f"Successfully killed {c} processes.")

	# kill pid.
	else:
		if log_level >= 0:
			loader = console.Loader(f"Killing process {pid}.")
		_sudo_ = Boolean(sudo).string(true="sudo ", false="")
		output = utils.__execute_script__(f"{_sudo_}kill {pid}")
		if output in ["terminated",""]:
			if output in [""]:
				response = processes(includes=pid)
				if not response.success: response
				try: 
					response.processes[pid]
					if log_level >= 0: loader.stop(success=False)
					return r3sponse.error(f"Failed to stop process {pid}.", log_level=log_level)
				except KeyError: a=1
			if log_level >= 0: loader.stop()
			return r3sponse.success(f"Successfully killed process {pid}.")
		else:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error(f"Failed to stop process {pid}, error: {output}", log_level=log_level)

# list all processes.
def processes(
	# root permission.
	sudo=False,
	# all processes that include a str.
	includes=None,
	# banned process names.
	banned=["grep"],
):
	_sudo_ = Boolean(sudo).string(true="sudo ", false="")
	if isinstance(includes, str):
		command = f"""{_sudo_}ps -ax | grep "{includes}" | """
	else:
		command = f"""{_sudo_}ps -ax | """
	#output = utils.__execute_script__(command + """awk '{print $1"|"$2"|"$3"|"$4"}' """)
	output = utils.__execute_script__(command + """awk '{$3="";print $0}' """)
	processes = {}
	for line in output.split("\n"):
		if line not in ["", " "]:
			array = line.split(" ")
			pid = array.pop(0)
			tty = array.pop(0)
			for i in array:
				process = array[0]
				if process not in ["", " "]: break
				else: array.pop(0)
			command = Array(array).string(joiner=" ")
			#try:
			#	pid,tty,_,process,command = line.split("|")
			#except ValueError: raise ValueError(f"Unable to unpack process line: [{line}], expected format: [4] seperator: [|].")
			if process not in banned:
				processes[pid] = {
					"pid":pid,
					"tty":tty,
					"process":process,
					"command":command,
				}
	return r3sponse.success(f"Successfully listed {len(processes)} processes.", {
		"processes":processes,
	})

#