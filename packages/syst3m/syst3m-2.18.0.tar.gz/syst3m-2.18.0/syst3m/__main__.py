#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys
from dev0s import *
sys.path.insert(1, gfp.base(path=__file__, back=2))

# imports.
from syst3m.classes.config import *
import syst3m

# the cli object class.
class CLI_(CLI.CLI):
	def __init__(self):
		
		# defaults.
		CLI.CLI.__init__(self,
			modes={
				"--user myuser":"Configure a system user (linux).",
				"    --check":"Check the existance of the specified user.",
				"    --create":"Create the specified user.",
				"    --delete":"Delete the specified user.",
				"    --password MyPassword":"Set the password of the specifed user (leave password blank for safe prompt).",
				"    --add-groups group1,group2":"Add the specified user to groups.",
				"    --delete-groups group1,group2":"Remove the specified user from groups.",
				"--group mygroup":"Configure a system group (linux).",
				"    --check":"Check the existance of the specified group.",
				"    --create":"Create the specified group.",
				"    --delete":"Delete the specified group.",
				"    --list-users":"List the users of the specified group.",
				"    --add-users user1,user2":"Add users from the specified group.",
				"    --delete-users user1,user2":"Delete users from the specified group.",
				"    --force-users user1,user2":"Add the specified users to the group and remove all others.",
				"--disk-space":"Get the free disk space (linux).",
				"--size /path/to/file":"Get the size of a file / directory (linux).",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):

		# check arguments.
		self.arguments.check(json=Defaults.options.json)

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, json=Defaults.options.json)

		# version.
		elif self.arguments.present(['--version']):
			self.stop(message=f"{ALIAS} version:"+Files.load(f"{SOURCE_PATH}/.version").replace("\n",""), json=Defaults.options.json)

		# config.
		#elif self.arguments.present('--config'):
		#	if JSON:
		#		print(CONFIG.dictionary)
		#	else:
		#		os.system(f"nano {CONFIG.file_path.path}")

		# user.
		elif self.arguments.present(['--user']):
			Defaults.operating_system(supported=["linux"])

			# initialize a user object.
			user = syst3m.User(self.arguments.get("--user"))

			# check if the user exists.
			if self.arguments.present(['--check']):
				response = user.check()
				Response.log(response)
				if response.success: print("User existance:",response["exists"])

			# create a user.
			elif self.arguments.present(['--create']):
				response = user.create()
				Response.log(response)

			# delete a user.
			elif self.arguments.present(['--delete']):
				response = user.delete()
				Response.log(response)

			# set a users password.
			elif self.arguments.present(['--password']):
				password = self.get_password(retrieve=True, message=f"Enter a new password of user [{user.username}]:")
				response = user.set_password(password=password)
				Response.log(response)

			# add the user to groups.
			elif self.arguments.present(['--add-groups']):
				groups = self.arguments.get("--delete-groups").split(",")
				response = user.add_groups(groups=groups)
				Response.log(response)

			# delete the user from groups.
			elif self.arguments.present(['--delete-groups']):
				groups = self.arguments.get("--delete-groups").split(",")
				response = user.add_groups(groups=groups)
				Response.log(response)


			# invalid.
			else:  self.invalid()

		# group.
		elif self.arguments.present(['--group']):
			Defaults.operating_system(supported=["linux"])

			# initialize a group object.
			group = syst3m.Group(self.arguments.get("--group"))

			# check if the group exists.
			if self.arguments.present(['--check']):
				response = group.check()
				Response.log(response)
				if response.success: 
					print("Group existance:",response["exists"])

			# create a group.
			elif self.arguments.present(['--create']):
				response = group.create()
				Response.log(response)

			# delete a group.
			elif self.arguments.present(['--delete']):
				response = group.delete()
				Response.log(response)

			# list the current users.
			elif self.arguments.present(['--list-users']):
				response = group.list_users()
				Response.log(response)
				if response.success: 
					print(f"Users of group {group.name}:",response["users"])

			# add users to the group.
			elif self.arguments.present(['--add-users']):
				users = self.arguments.get("--add-users").split(",")
				response = group.add_users(users=users)
				Response.log(response)

			# delete users from the group.
			elif self.arguments.present(['--delete-users']):
				users = self.arguments.get("--delete-users").split(",")
				response = group.delete_users(users=users)
				Response.log(response)

			# check if the specified users are enabled and remove all other users.
			elif self.arguments.present(['--force-users']):
				users = self.arguments.get("--force-users").split(",")
				response = group.check_users(users=users)
				Response.log(response)


			# invalid.
			else:  self.invalid()

		# free disk space.
		elif self.arguments.present(["--disk-space"]):
			Defaults.operating_system(supported=["linux"])
			import shutil
			import math
			def size(size_bytes):
			   if size_bytes == 0:
			       return "0B"
			   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
			   i = int(math.floor(math.log(size_bytes, 1024)))
			   p = math.pow(1024, i)
			   s = round(size_bytes / p, 2)
			   return "%s %s" % (s, size_name[i])
			total, used, free = shutil.disk_usage(__file__)
			print(f"total: {size(total)}, used: {size(used)}, free: {size(free)}")

		# size.
		elif self.arguments.present(["--size"]):
			fp = FilePath(self.arguments.get("--size"))
			if not fp.exists(): 
				print(f"File path [{fp.path}] does not exist.")
				sys.exit(1)
			else:
				loader = Console.Loader(f"Retrieving size of {fp.path} ...")
				size = fp.size()
				loader.stop()
				print(f"Size {fp.path}: {size}")

		# invalid.
		else: self.invalid(json=Defaults.options.json)

		#
	def get_password(self, retrieve=False, check=False, message="Password:"):
		password = self.arguments.get("--password", required=retrieve, default=None)
		if password == None:
			password = utils.__prompt_password__(message)
			if check and password != utils.__prompt_password__("Enter the same password:"):
				print("Passwords do not match.")
				sys.exit(1)
		else: password = password.replace("\\","").replace("\ ","")
		return password
# main.
if __name__ == "__main__":
	cli = CLI_()
	if "--developer" in sys.argv:
		cli.start()
	else:
		try:
			cli.start()
		except KeyboardInterrupt:
			print("Aborted: KeyboardInterrupt")


