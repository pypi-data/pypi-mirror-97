#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# traceback.
class Traceback(object):
	def __init__(self,
		# the imported traceback (#1).
		traceback="syst3m.objects.Traceback",
		# the raw traceback (#2).
		raw_traceback="syst3m.classes.objects.Object",
	):
		self._traceback_ = traceback
		self._raw_traceback_ = traceback
	# imported traceback.
	@property
	def traceback(self):
		return self.__traceback__()
	def __traceback__(self, 
		# the function name (optional) (#1).
		function=None,
		# the parameter name (optional) (#2).
		parameter=None,
		# the attrbiute name (optional) (#3).
		attribute=None,
		# raw traceback.
		raw=False,
	):
		options = ""
		if attribute != None:
			options += f".{attribute}"
		elif function != None:
			options += f".{function}"
			if parameter != None:
				options += f".{parameter}"
		if raw:
			return f"<{self._raw_traceback_}{options}>"
		else:
			return f"<{self._traceback_}{options}>"

# object.
class Object(Traceback):
	def __init__(self, 
		# the imported traceback.
		traceback="syst3m.objects.Object",
		# the raw traceback.
		raw_traceback="syst3m.classes.objects.Object",
	):
		Traceback.__init__(self, traceback=traceback, raw_traceback=raw_traceback)
	# iterate over self keys & variables.
	def items(self):
		return vars(self).items()
	def keys(self):
		return list(vars(self).keys())
	def values(self):
		return list(vars(self).values())
	def dict(self, keys=[]):
		if keys == []:
			items = self.items()
		else:
			items = []
			for i in keys: items.append([i, self[i]])
		dictionary = {}
		for key, value in items:
			dictionary[key] = value
		return dictionary
	# assign self variables by dictionary.
	def assign(self, dictionary, serialize=True):
		if not isinstance(dictionary, dict):
			raise TypeError("You can only self assign with a dictionary as parameter.")
		for key,value in dictionary.items():
			if serialize:
				if value in ["True", "true", "TRUE"]: value = True
				elif value in ["False", "false", "FALSE"]: value = False
				elif value in ["None", "none", "null"]: value = None
			self[key] = value
	# get attributes.
	def attributes(self, keys=[]):
		return self.dict(keys=keys)
	# support item assignment.
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)
	def __delitem__(self, key):
		delattr(self, key)

# thread.
class Thread(Object, threading.Thread):
	def __init__(self, 
		# the threads id (#1).
		id="Thread",
		# the imported traceback.
		traceback="syst3m.objects.Thread",
		# the raw traceback.
		raw_traceback="syst3m.classes.objects.Thread",
		# the threads log level.
		log_level=-1,
	):
		Object.__init__(self, traceback=traceback, raw_traceback=raw_traceback)
		threading.Thread.__init__(self)
		self.log_level = log_level
		try:
			self.id = id
		except: a=1
		self.__status__ = "initialized"
		self.__response__ = None
	# stop the thread.
	def run(self):
		r3sponse.log(f"Starting thread {self.id}.", log_level=self.log_level, required_log_level=0)
		self.__status__ = "running"
		try:
			response = self.__run__()
		except AttributeError: response = None
		if response != None:
			try: success = bool(response["success"])
			except: success = True
			if not success: 
				r3sponse.log(response=response, log_level=self.log_level, required_log_level=0)
				return response
		self.send_stop()
		return r3sponse.success(f"Started thread {self.id}.", log_level=self.log_level, required_log_level=0)
	def safe_start(self, timeout=120, sleeptime=1):
		r3sponse.log(f"Stopping thread {self.id}.", log_level=self.log_level, required_log_level=0)
		self.start()
		for i in range(timeout/sleeptime):
			if self.running: break
			time.sleep(sleeptime)
		if not self.running: 
			self.response = r3sponse.error(f"Unable to start thread {self}.", log_level=self.log_level, required_log_level=0)
			return self.response
		self.response = r3sponse.success(f"Stopped thread {self.id}.", log_level=self.log_level, required_log_level=0)
		return self.response
	def safe_stop(self, timeout=120, sleeptime=1):
		r3sponse.log(f"Stopping thread {self.id}.", log_level=self.log_level, required_log_level=0)
		try:
			response = self.__stop__()
		except AttributeError: response = None
		if response != None:
			try: success = bool(response["success"])
			except: success = True
			if not success: 
				r3sponse.log(response=response, log_level=self.log_level, required_log_level=0)
				self.response = response
				return self.response
		self.send_stop()
		for i in range(timeout/sleeptime):
			if self.stopped: break
			time.sleep(sleeptime)
		if not self.stopped: 
			self.response = r3sponse.error(f"Unable to stop thread {self}.", log_level=self.log_level, required_log_level=0)
			return self.response
		self.response = r3sponse.success(f"Stopped thread {self.id}.", log_level=self.log_level, required_log_level=0)
		return self.response
	def send_stop(self, response=None):
		if response != None:
			self.__response__ = response
		self.__status__ = "stopping"
	def send_crash(self, response=None):
		if response != None:
			self.__response__ = response
		self.__status__ = "crashed"
	#properties
	@property
	def run_permission(self):
		return self.__status__ in ["running"]
	@property
	def running(self):
		return self.__status__ in ["running", "stopping"]
	@property
	def stopped(self):
		return self.__status__ in ["stopped"]
	@property
	def crashed(self):
		return self.__status__ in ["crashed"]
	@property
	def response(self):
		return self.__response__
	# str representation.
	def __str__(self):
		if self.crashed:
			try: error = self.response.error
			except: error = None
		if error != None:
			return f"<{self.__traceback__()[1:-1]} (crashed: {crashed}) (error: {error}) >"
		else:
			return f"<{self.__traceback__()[1:-1]} (running: {running}) (stopped: {stopped}) (crashed: {crashed}) >"
	# representation.
	def __repr__(self):
		return str(self)
	