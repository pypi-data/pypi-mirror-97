#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import utils, console, defaults, objects

# the service object class.
class Service(objects.Object):
	# launchd: 
	# 	$ tail -f /var/log/system.log
	#	https://medium.com/swlh/how-to-use-launchd-to-run-services-in-macos-b972ed1e352
	#	https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/
	def __init__(self,
		# the service id.
		id=None,
		# the user & group on which the service will be run.
		user=None,
		group=None,
		# the start command.
		start=None,
		# the service description.
		description="",
		# restart on crash.
		restart=True,
		# the restart limit.
		restart_limit=5,
		# the restart delay.
		restart_delay=10,
		# the path to the log file.
		logs=None,
		# the path to the error file.
		errors=None,
		# the object's log level.
		log_level=0,
		# the import traceback.
		traceback="syst3m.service.Service",
	):	

		# defaults.
		objects.Object.__init__(self, traceback=traceback)

		# vars.
		self.id = id
		self.user = user
		self.group = group
		self.start_ = start
		self.description = description
		self.restart_limit = restart_limit
		self.restart_delay = restart_delay
		self.log_level = log_level
		self.options = []
		self.logs, self.errors = None, None
		if restart:
			self.options.append("restart_")
		if logs != None: 
			self.options.append("logs")
			self.logs = File(path=logs)
			if not Files.exists(path=self.logs.fp.base()):
				os.system(f"mkdir -p {self.logs.fp.base()}")
			if self.logs.fp.exists(): self.logs.load()
		if errors != None: 
			self.options.append("errors")
			self.errors = File(path=errors)
			if not Files.exists(path=self.errors.fp.base()):
				os.system(f"mkdir -p {self.errors.fp.base()}")
			if self.errors.fp.exists(): self.errors.load()

		# attributes.
		if defaults.vars.os in ["macos"]:
			self.service = File(path=f"/Library/LaunchDaemons/{self.id}.plist")
		else:
			self.service = File(path=f"/etc/systemd/system/{self.id}.service")

		#
	# functions.
	def create(self):

		# check params.
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="create"),
			parameters={
				"id":self.id,
				"user":self.user,
				"start":self.start_,
			})
		if not response.success: return response

		# checks.
		if self.service.fp.exists(): 
			return r3sponse.error(f"Service [{self.service.fp.path}] already exists (call service.check() instead).")

		# save.
		r3sponse.log(f"&ORANGE&Root permission&END& required to save changes to [{self.service.fp}].", log_level=self.log_level)
		self.service.save(data=self.__create__(), sudo=True)
		self.service.fp.ownership.set("root", sudo=True)
		self.service.fp.permission.set(700, sudo=True)

		# handler.
		if self.service.fp.exists(): 
			return r3sponse.success(f"Successfully created service {self.id}.")
		else:
			return r3sponse.error(f"Failed to create service {self.id}.")

		#
	def check(self):

		# check params.
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="check"),
			parameters={
				"id":self.id,
				"user":self.user,
				"start":self.start_,
			})
		if not response.success: return response
		
		# checks.
		if not self.service.fp.exists(): 
			return self.create()

		# save.
		self.service.load(sudo=True)
		data = self.__create__()
		if self.service.data != data:
			r3sponse.log(f"&ORANGE&Root permission&END& required to save changes to [{self.service.fp}].", log_level=self.log_level)
			self.service.save(data=data, sudo=True)

		# always set permissions.
		self.service.fp.ownership.set("root", sudo=True)
		self.service.fp.permission.set(700, sudo=True)
		
		# handler.
		if self.service.fp.exists(): 
			return r3sponse.success(f"Successfully checked service {self.id}.")
		else:
			return r3sponse.error(f"Failed to check service {self.id}.")

		#
	def delete(self):

		# checks.
		if not self.service.fp.exists(): 
			return r3sponse.error(f"Service [{self.service.fp.path}] does not already exist.")

		# save.
		self.service.fp.delete(sudo=True, forced=True)

		# handler.
		if not self.service.fp.exists(): 
			return r3sponse.success(f"Successfully deleted service {self.id}.")
		else:
			return r3sponse.error(f"Failed to delete service {self.id}.")

		#
	# control functions.
	def start(self):
		
		# launchd.
		if defaults.vars.os in ["macos"]:
			command = ""
			for i in [self.id]:
				command += f"sudo launchctl start {i} &&"
			command = command[:-3]
			output = console.execute(command)
			if not output.success: return output
			elif str(output) in ["", "\n"]:
				return r3sponse.success(f"Successfully started {self.id}.")
			else:
				return r3sponse.error(f"Failed to start {self.id}.")

		# systemd.
		else:
			command = ""
			for i in [self.id]:
				command += f"sudo systemctl start {i} &&"
			command = command[:-3]
			output = console.execute(command)
			if not output.success: return output
			elif str(output) in ["", "\n"]:
				return r3sponse.success(f"Successfully started {self.id}.")
			else:
				return r3sponse.error(f"Failed to start {self.id}.")

		#
	def stop(self):
		
		# launchd.
		if defaults.vars.os in ["macos"]:
			command = ""
			for i in [self.id]:
				command += f"sudo launchctl stop {i} &&"
			command = command[:-3]
			output = console.execute(command)
			if not output.success: return output
			elif str(output) in ["", "\n"]:
				return r3sponse.success(f"Successfully stopped {self.id}")
			else:
				return r3sponse.error(f"Failed to stop {self.id}")

		# systemd.
		else:
			command = ""
			for i in [self.id]:
				command += f"sudo systemctl stop {i} &&"
			command = command[:-3]
			output = console.execute(command)
			if not output.success: return output
			elif str(output) in ["", "\n"]:
				return r3sponse.success(f"Successfully stopped {self.id}")
			else:
				return r3sponse.error(f"Failed to stop {self.id}")

		#
	def restart(self):
		
		# launchd.
		if defaults.vars.os in ["macos"]:
			response = self.stop()
			if not response.success: return response
			response = self.start()
			if not response.success: return response
			return r3sponse.success(f"Successfully restarted {self.id}")

		# systemd.	
		else:
			command = ""
			for i in [self.id]:
				command += f"sudo systemctl restart {i} &&"
			command = command[:-3]
			output = console.execute(command)
			if not output.success: return output
			elif str(output) in ["", "\n"]:
				return r3sponse.success(f"Successfully restarted {self.id}")
			else:
				return r3sponse.error(f"Failed to restarted {self.id}")

		#
	def status(self):
		
		# launchd.
		if defaults.vars.os in ["macos"]:
			output = console.execute(f"sudo launchctl list | grep {self.id}")
			if not output.success: return output
			else:
				return r3sponse.success(f"Successfully retrieved the status of {self.id}",{
					"status":str(output),
				})

		# systemd.
		else:
			output = console.execute(f"sudo systemctl status {self.id}")
			if not output.success: return output
			else:
				return r3sponse.success(f"Successfully retrieved the status of {self.id}",{
					"status":str(output),
				})

			#
	# cli functions.
	def tail(self, live=True):
		if defaults.vars.os in ["macos"]:
			if live:
				os.system(f"tail -f /var/log/system.log | grep {self.id}")
			else:
				os.system(f"cat /var/log/system.log | grep {self.id}")
		else:
			raise ValueError("Coming soon.")
	# system functions.
	def __create__(self):
		
		# lauchd.
		if defaults.vars.os in ["macos"]:

			# checks.
			if not isinstance(self.start_, (list, Array)): 
				raise ValueError(f"{self.__traceback__()} attribute [start] requires to be a [list] or [Array] not [{self.start_.__class__.__name__}].")

			# vars.
			arguments, restart, logs, errors, group = "", "", "", "", ""

			# arguments.
			if len(self.start_) >= 0:
				arguments =  f'    <key>ProgramArguments</key>' + '\n'
				arguments += f'    <array>' + '\n'
				for i in self.start_:
					arguments += f'        <string>{i}</string>' + '\n'
				arguments += f'    </array>' + '\n'

			# group.
			if self.group != None:
				group = (
					"    <key>GroupName</key>" + "\n" +
					f"    <string>{self.group}</string>" + "\n" +
					"")

			# restart.
			if "restart" in self.options:
				restart = (
					f'    <key>StartInterval</key>' + '\n' +
					f'    <integer>{self.restart_delay}</integer>' + '\n' +
					"")

			# logs.
			if "logs" in self.options:
				logs = (
					f"    <key>StandardOutPath</key>" + "\n" +
					f"    <string>{self.logs.fp.path}</string>" + "\n" +
					"")

			# errors.
			if "errors" in self.options:
				errors = (
					"    <key>StandardErrorPath</key>" + "\n" +
					f"    <string>{self.errors.fp.path}</string>" + "\n" +
					"")

			# combine.
			service = (
				f'<?xml version="1.0" encoding="UTF-8"?>' + '\n' +
				f'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' + '\n' +
				f'<plist version="1.0">' + '\n' +
				f'<dict>' + '\n' +
				f'    <key>Label</key>' + '\n' +
				f'    <string>{self.id}</string>' + '\n' +
				f"    <key>UserName</key>" + "\n" +
				f"    <string>{self.user}</string>" + "\n" +
				group + 
				arguments +
				restart +
				logs +
				errors + 
				f'</dict>' + '\n' +
				f'</plist>' + '\n' +
				'')
			
		# systemd.	
		else:

			# checks.
			if isinstance(start, (list, Array)):
				start = Array(start).string(joiner=" ")
			else:
				start = str(self.start_)

			# build.
			service = (
				f"[Unit]" + "\n" +
				f"Description={self.description}" + "\n" +
				f"After=network.target" + "\n" +
				f"StartLimitIntervalSec=0" + "\n" +
				f"" + "\n" +
				f"[Service]" + "\n" +
				f"Type=simple" + "\n" +
				f"ExecStart={start}" + "\n" +
				f"User={self.user}" + "\n" +
				f""
			)

			# group.
			if self.group != None:
				service += (
					f"Group={self.group}" + "\n" +
					"")

			# restart.
			if "restart" in self.options:
				service += (
					f"Restart=always" + "\n" +
					f"RestartSec=1" + "\n" +
					"")
				if self.restart_limit != None:
					service += ( 
						f"StartLimitBurst={self.restart_limit}" + "\n" +
						f"StartLimitIntervalSec={self.restart_delay}" + "\n" +
						f"")

			# additional build.
			service += (
				f"" + "\n" +
				f"[Install]" + "\n" +
				f"WantedBy=multi-user.target" + "\n" +
				f"")

		# handler.
		if service[len(service)-1] == "\n": service = service[:-1]
		return service

#