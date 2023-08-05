
# imports
from syst3m.classes.config import *
from syst3m.classes.color import color
from syst3m.classes import defaults
import getpass

# input.
_input_ = input
def input(message, yes_no=False, check=False, password=False, default=None):
	message = color.fill(message)
	if len(message) > 0 and message[0].upper() != message[0]: message = String(message).capitalized_word()
	if yes_no:
		while True:
			if len(message) > 0 and message[len(message)-1] == " ": message = message[:-1]
			elif len(message) > 0 and message[len(message)-1] == ".": message = message[:-1]
			else: break
		value = _input_(message+" (y/n): ")
		if value in ["yes", 'y', "YES", "Y"]:
			return True
		else:
			return False
	else:
		while True:
			if len(message) > 0 and message[len(message)-1] == " ": message = message[:-1]
			elif len(message) > 0 and message[len(message)-1] == ":": message = message[:-1]
			else: break
		if password:
			value = getpass.getpass(message+": ")
		else:
			value = _input_(message+": ")
			if value in [""]: value = default
		if check:
			if password:
				if getpass.getpass("Enter the same passphrase: ") != password:
					print("Passphrases do not match.")
					return default
				else:
					return password
			else:
				if input(f"({value}) correct?", yes_no=True):
					return value
				else:
					return default
		else:
			return value

# execute & output.
class Output(ResponseObject):
	def __init__(self, 
		# the success message (param #1).
		message=None,
		# the attributes (param #2).
		attributes={},
		# the error message (param #3).
		error=None,
	):
		dictionary = {
			"success":error == None,
			"message":message,
			"error":error,
		}
		for key,value in attributes.items():
			dictionary[key] = value
		ResponseObject.__init__(self, dictionary)
		if self.success:
			self.str = str(self.output)
		else:
			self.str = str(self.error)
	def __len__(self):
		return len(self.str)
	def __str__(self):
		return str(self.str)
	def __bool__(self):
		return bool(self.success)
	# support default iteration.
	def __iter__(self):
		return iter(str(self))
	# support '==' & '!=' operator.
	def __eq__(self, dictionary):
		if isinstance(dictionary, dict):
			return str(self.sort()) == str(Dictionary(dictionary).sort())
		elif isinstance(dictionary, Dictionary):
			return str(self.sort()) == str(dictionary.sort())
		else:
			try:
				return str(self.sort()) == str(dictionary.sort())
			except:
				return False
	def __ne__(self, dictionary):
		if isinstance(dictionary, dict):
			return str(self.sort()) != str(Dictionary(dictionary).sort())
		elif isinstance(dictionary, Dictionary):
			return str(self.sort()) != str(dictionary.sort())
		else:
			try:
				return str(self.sort()) != str(dictionary.sort())
			except:
				return False
	# support 'in' operator.
	def __contains__(self, string):
		if isinstance(path, (list, Array)):
			for i in string:
				if i in self.str:
					return True
			return False
		else:
			return string in self.str
		#
	# object instance.
	def instance(self):
		return "Output"
		#
def execute(
	# option 1:
	# the command in str format (str is saved to a script & then executed).
	command="ls .",
	# joiner for when command is in list format.
	joiner="\n",
	# option 2:
	path=None,
	# the executive.
	executive="sh",
	# the arguments passed to the script.
	arguments=[], 
	# the subprocess shell parameter.
	shell=False,
	# asynchronous (cant capture output).
	async_=False,
	# serialize to dict.
	# aka expect dict format.
	serialize=False,
):
	# excute.
	delete = False
	if path == None:
		delete = True
		path = f"/tmp/tmp_script_{String('').generate()}"
		if isinstance(command, list):
			command = Array(array=command).string(joiner=joiner)
		Files.save(path, command)
		response_str = f"command ({command})"
	else:
		response_str = f"script ({path})"
	if async_:
		proc = subprocess.Popen(
			[executive, path] + arguments,
			shell=shell,)
		return Output(message=f"Succesfully executed {response_str}.", attributes={
			"output":"",
			"process":proc,
			"pid":proc.pid,
		})
	try:
		proc = subprocess.run(
			[executive, path] + arguments,
			check=True,
			capture_output=True,
			text=True,
			shell=shell,
		)
	except subprocess.CalledProcessError as error:
		exception = String(str(error))
		if "Command '[" in exception:
			to_replace = f"'{exception.slice_array()}'"
			exception = exception.replace(str(to_replace), "[ ... ]")
		error_, output = error.stderr, error.output
		if isinstance(error_, bytes): error_ = error_.decode()
		if isinstance(output, bytes): output = output.decode()
		if defaults.options.log_level <= 0:
			return Output(error=f"Failed to execute {response_str}, (exception: {exception}), (error: {error_}).")
		else:
			return Output(error=f"Failed to execute {response_str}, (exception: {exception}), (output: {output}), (error: {error_}).")
	error_, output = proc.stderr, proc.stdout
	if isinstance(error_, bytes): error_ = error_.decode()
	if isinstance(output, bytes): output = output.decode()
	if error_ != "":
		if defaults.options.log_level <= 0:
			return Output(error=f"Failed to execute {response_str}, (error: {error_}).")
		else:
			return Output(error=f"Failed to execute {response_str}, (output: {output}), (error: {error_}).")
	if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
	if delete:
		Files.delete(path)
	if serialize:
		try: response = r3sponse.ResponseObject(json=output)
		except Exception as e: 
			if loader != None: loader.stop(success=False)
			return Output(error=f"Failed to serialize (output: {output}).")
		return response
	else:
		return Output(message=f"Succesfully executed {response_str}.", attributes={
			"output":output,
			"process":proc,
			"pid":None,
		})

# the loader object class.
class Loader(threading.Thread):
	def __init__(self, message, autostart=True, log_level=0, interactive=True):
		threading.Thread.__init__(self)
		self.message = self.__clean_message__(message)
		self.last_message = str(self.message)
		self.log_level = log_level
		self.interactive = interactive
		if autostart and self.log_level >= 0: 
			if self.interactive:
				try:
					self.start()
				except KeyboardInterrupt as e:
					self.stop(success=False)
					raise KeyboardInterrupt(f"{e}")
			else:
				print(self.message+".")
	def run(self):
		if self.log_level >= 0: 
			self.running = True
			self.released = True
			while self.running:
				if not self.released:
					time.sleep(1)
				else:
					for i in ["|", "/", "-", "\\"]:
						if not self.released: break
						if self.message != self.last_message:
							print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
							self.message = self.__clean_message__(self.message)
						print(f"{self.message} ... {i}", end="\r")
						self.last_message = self.message
						if not self.running: break
						time.sleep(0.33)
		self.running = "stopped"
	def stop(self, message=None, success=True, response=None, quiet=False):
		if self.log_level >= 0:
			if response == None:
				if message == None: message = self.message
			else:
				if response["error"] == None:
					message = response["message"]
				else:
					success = False
					message = "Error: "+response["error"]
			if self.interactive:
				self.running = False
				for i in range(120):
					if self.running == "stopped": break
					time.sleep(0.5)
				if self.running != "stopped": raise ValueError(f"Unable to stop loader [{self.message}].")
			if not quiet:
				if self.interactive:
					print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
					if success:
						print(f"{message} ... done")
					else:
						print(f"{message} ... {color.red}failed{color.end}")
				else:
					if success:
						print(f"{message}. done")
					else:
						print(f"{message}. {color.red}failed{color.end}")
	def mark(self, new_message=None, old_message=None, success=True, response=None):
		if self.log_level >= 0: 
			if response != None:
				if response["error"] == None:
					success = True
				else:
					success = False
			if old_message == None: old_message = self.message
			if self.interactive:
				print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
				if success:
					print(f"{old_message} ... done")
				else:
					print(f"{old_message} ... {color.red}failed{color.end}")
			else:
				if success:
					print(f"{old_message}. done")
				else:
					print(f"{old_message}. {color.red}failed{color.end}")
			if new_message != None: self.message = new_message
	def hold(self):
		if self.log_level >= 0: 
			self.released = False
			time.sleep(0.33)
	def release(self):
		if self.log_level >= 0: 
			self.released = True
			time.sleep(0.33)
	# system functions.
	def __clean_message__(self, message):
		message = color.fill(str(message))
		if message[-len(" ..."):] == " ...": message = message[:-4]
		if message[-len("."):] == ".": message = message[:-1]
		if message[0].upper() != message[0]: message = message[1:]+message[0].upper()+message[1:]
		return message
	def __empty_message__(self, length=len("hello world")):
		s = ""
		for i in range(length): s += " "
		return s

# the loader object class.
class ProgressLoader(threading.Thread):
	def __init__(self, message, index=0, max=10, log_level=0):
		threading.Thread.__init__(self)
		self.message = message
		if self.message[-len(" ..."):] == " ...": self.message = self.message[:-4]
		if self.message[-len("."):] == ".": self.message = self.message[:-1]
		if self.message[0].upper() != self.message[0]: self.message = self.message[1:]+self.message[0].upper()+self.message[1:]
		self.message = color.fill(self.message)
		self.index = index
		self.max = max
		self.progress = None
		self.last_message = None
		self.log_level = log_level
	def next(self, count=1, decimals=2):
		self.index += count
		p = round((self.index / self.max) * 100, decimals)
		if p != self.progress:
			self.progress = p
			self.last_message = f"{self.message} ... {self.progress}%"
			if self.log_level >= 0:
				print(self.last_message, end="\r")
	def stop(self, message=None, success=True, response=None):
		if self.log_level >= 0:
			if response == None:
				if message == None: message = self.message
			else:
				if response["error"] == None:
					message = response["message"]
				else:
					success = False
					message = "Error: "+response["error"]
			if self.last_message != None:
				print(self.__empty_message__(length=len(f"{self.last_message}")), end="\r")
			if success:
				print(f"{message} ... done")
			else:
				print(f"{message} ... {color.red}failed{color.end}")
	def __empty_message__(self, length=len("hello world")):
		s = ""
		for i in range(length): s += " "
		return s