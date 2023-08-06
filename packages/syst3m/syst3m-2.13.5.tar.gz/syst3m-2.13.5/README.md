# syst3m
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: macos & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"> 
</p>

## Table of content:
  * [Description](#description)
  * [Installation](#installation)
  * [CLI Usage](#cli-usage)
  * [Code Examples](#code-examples)

# Description:
Python & cli toolset for the os system.

# Installation:
Install the package.

	pip3 install syst3m --upgrade && python3 -c 'import syst3m' --create-alias syst3m --sudo

# CLI Usage:
	Usage: syst3m <mode> <options> 
	Modes:
	    --user myuser : Configure a system user (linux).
	        --check : Check the existance of the specified group.
	        --create : Create the specified group.
	        --delete : Delete the specified group.
	        --password MyPassword : Set the password of the specifed user (leave password blank for safe prompt).
	        --add-groups group1,group2 : Add the specified user to groups.
	        --delete-groups group1,group2 : Remove the specified user from groups.
	    --group mygroup : Configure a system group (linux).
	        --list-users : List the users of the specified group.
	        --add-users user1,user2 : Add users from the specified group.
	        --delete-users user1,user2 : Delete users from the specified group.
	        --force-users user1,user2 : Add the specified users to the group and remove all others.
	    --disk-space : Get the free disk space (linux).
	    --size /path/to/file : Get the size of a file / directory (linux).
	    -h / --help : Show the documentation.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020 - 2021. All rights reserved.

# Code Examples:

### Table of content:
- [__Browser__](#browser)
  * [get](#get)
  * [get_element](#get_element)
- [__Cache__](#cache)
  * [set](#set)
  * [get](#get-1)
  * [load](#load)
- [__Color__](#color)
  * [remove](#remove)
  * [fill](#fill)
  * [boolean](#boolean)
- [__Disks__](#disks)
  * [list](#list)
- [__Env__](#env)
  * [fill](#fill-1)
  * [get](#get-2)
  * [get_string](#get_string)
  * [get_boolean](#get_boolean)
  * [get_integer](#get_integer)
  * [get_array](#get_array)
  * [get_tuple](#get_tuple)
  * [get_dictionary](#get_dictionary)
  * [set](#set-1)
  * [set_string](#set_string)
  * [set_boolean](#set_boolean)
  * [set_integer](#set_integer)
  * [set_array](#set_array)
  * [set_tuple](#set_tuple)
  * [set_dictionary](#set_dictionary)
- [__Ext4__](#ext4)
  * [erase](#erase)
  * [partition](#partition)
  * [format](#format)
  * [mount](#mount)
  * [unmount](#unmount)
- [__Group__](#group)
  * [create](#create)
  * [delete](#delete)
  * [check](#check)
  * [list_users](#list_users)
  * [delete_users](#delete_users)
  * [add_users](#add_users)
  * [check_users](#check_users)
- [__Loader__](#loader)
  * [run](#run)
  * [stop](#stop)
  * [mark](#mark)
  * [hold](#hold)
  * [release](#release)
- [__Output__](#output)
  * [instance](#instance)
- [__ProgressLoader__](#progressloader)
  * [next](#next)
  * [stop](#stop-1)
- [__Symbol__](#symbol)
- [__User__](#user)
  * [delete](#delete-1)
  * [check](#check-1)
  * [set_password](#set_password)
  * [add_groups](#add_groups)
  * [delete_groups](#delete_groups)
- [__WebServer__](#webserver)
  * [set](#set-2)
  * [get](#get-3)
  * [app](#app)
  * [get](#get-4)
  * [set](#set-3)
  * [active](#active)
  * [run](#run-1)
  * [fork](#fork)
  * [stop](#stop-2)
  * [start_thread](#start_thread)
  * [get_thread](#get_thread)
  * [token](#token)
  * [running](#running)

## Browser:
The browser object class.
``` python 

# initialize the browser object class.
browser = syst3m.classes.browser.Browser(
    # the driver.
    driver="chromedriver", )

```

#### Functions:

##### get:
``` python

# call browser.get.
_ = browser.get(url)

```
##### get_element:
``` python

# call browser.get_element.
_ = browser.get_element(
    # the element type.
    element="input",
    # the attribute name.
    attribute="name",
    # the attributes value.
    value="username",
    # the parent element (default is browser.driver).
    parent=None,  )

```

## Cache:
The cache object class.
``` python 

# initialize the cache object class.
cache = syst3m.classes.cache.Cache(path=None)

```

#### Functions:

##### set:
``` python

# call cache.set.
_ = cache.set(data=None, group=None, id=None, format="str")

```
##### get:
``` python

# call cache.get.
_ = cache.get(group=None, id=None, format="str")

```
##### load:
``` python

# call cache.load.
_ = cache.load()

```

## Color:
The color object class.
``` python 

# initialize the color object class.
color = syst3m.classes.color.Color()

```

#### Functions:

##### remove:
``` python

# call color.remove.
_ = color.remove(string)

```
##### fill:
``` python

# call color.fill.
_ = color.fill(string)

```
##### boolean:
``` python

# call color.boolean.
_ = color.boolean(boolean, red=True)

```

## Disks:
The disks object class.
``` python 

# initialize the disks object class.
disks = syst3m.classes.disks.Disks()

```

#### Functions:

##### list:
``` python

# call disks.list.
_ = disks.list()

```

## Env:
The env object class.
``` python 

# initialize the env object class.
env = syst3m.classes.env.Env()

```

#### Functions:

##### fill:
``` python

# call env.fill.
_ = env.fill(string)

```
##### get:
``` python

# call env.get.
_ = env.get(id, default=None, format="str")

```
##### get_string:
``` python

# call env.get_string.
_ = env.get_string(id, default=None)

```
##### get_boolean:
``` python

# call env.get_boolean.
_ = env.get_boolean(id, default=None)

```
##### get_integer:
``` python

# call env.get_integer.
_ = env.get_integer(id, default=None)

```
##### get_array:
``` python

# call env.get_array.
_ = env.get_array(id, default=None)

```
##### get_tuple:
``` python

# call env.get_tuple.
_ = env.get_tuple(id, default=None)

```
##### get_dictionary:
``` python

# call env.get_dictionary.
_ = env.get_dictionary(id, default=None)

```
##### set:
``` python

# call env.set.
_ = env.set(id, value, format="unknown")

```
##### set_string:
``` python

# call env.set_string.
_ = env.set_string(id, value)

```
##### set_boolean:
``` python

# call env.set_boolean.
_ = env.set_boolean(id, value)

```
##### set_integer:
``` python

# call env.set_integer.
_ = env.set_integer(id, value)

```
##### set_array:
``` python

# call env.set_array.
_ = env.set_array(id, value)

```
##### set_tuple:
``` python

# call env.set_tuple.
_ = env.set_tuple(id, value)

```
##### set_dictionary:
``` python

# call env.set_dictionary.
_ = env.set_dictionary(id, value, subkey="")

```

## Ext4:
The ext4 object class.
``` python 

# initialize the ext4 object class.
ext4 = syst3m.classes.disks.Ext4()

```

#### Functions:

##### erase:
``` python

# call ext4.erase.
response = ext4.erase(
    # the device without partition number (/dev/sdb).
    device=None, )

```
##### partition:
``` python

# call ext4.partition.
response = ext4.partition(
    # the device without partition number (/dev/sdb).
    device=None, )

```
##### format:
``` python

# call ext4.format.
response = ext4.format(
    # the device with partition number (/dev/sdb1).
    device=None,
    # the assigned label (name).
    label=None, )

```
##### mount:
``` python

# call ext4.mount.
response = ext4.mount(
    # the device with partition number (/dev/sdb1).
    device=None, 
    # the mountpoint path.
    path=None, )

```
##### unmount:
``` python

# call ext4.unmount.
response = ext4.unmount(
    # the mountpoint path.
    path=None, )

```

## Group:
The group object class.
``` python 

# initialize the group object class.
group = syst3m.classes.system.Group(
     
    # string format.
    name=None,
    users=[], # all authorized user identifiers.
    # boolean format.
    get_users=False, # (only gets filled if the storages group exists.) )

```

#### Functions:

##### create:
``` python

# call group.create.
response = group.create(users=None)

```
##### delete:
``` python

# call group.delete.
response = group.delete()

```
##### check:
``` python

# call group.check.
response = group.check()

```
##### list_users:
``` python

# call group.list_users.
response = group.list_users()

```
##### delete_users:
``` python

# call group.delete_users.
response = group.delete_users(users=[])

```
##### add_users:
``` python

# call group.add_users.
response = group.add_users(users=[])

```
##### check_users:
``` python

# call group.check_users.
response = group.check_users(users=[])

```

## Loader:
The loader object class.
``` python 

# initialize the loader object class.
loader = syst3m.classes.console.Loader(message, autostart=True, log_level=0, interactive=True)

```

#### Functions:

##### run:
``` python

# call loader.run.
_ = loader.run()

```
##### stop:
``` python

# call loader.stop.
_ = loader.stop(message=None, success=True, response=None, quiet=False)

```
##### mark:
``` python

# call loader.mark.
_ = loader.mark(new_message=None, old_message=None, success=True, response=None)

```
##### hold:
``` python

# call loader.hold.
_ = loader.hold()

```
##### release:
``` python

# call loader.release.
_ = loader.release()

```

## Output:
The output object class.
``` python 

# initialize the output object class.
output = syst3m.classes.console.Output(
    # the success message (param #1).
    message=None,
    # the attributes (param #2).
    attributes={},
    # the error message (param #3).
    error=None, )

```

#### Functions:

##### instance:
``` python

# call output.instance.
_ = output.instance()

```

## ProgressLoader:
The progress_loader object class.
``` python 

# initialize the progress_loader object class.
progress_loader = syst3m.classes.console.ProgressLoader(message, index=0, max=10, log_level=0)

```

#### Functions:

##### next:
``` python

# call progress_loader.next.
_ = progress_loader.next(count=1, decimals=2)

```
##### stop:
``` python

# call progress_loader.stop.
_ = progress_loader.stop(message=None, success=True, response=None)

```

## Symbol:
The symbol object class.
``` python 

# initialize the symbol object class.
symbol = syst3m.classes.color.Symbol()

```
## User:
The user object class.
``` python 

# initialize the user object class.
user = syst3m.classes.system.User(
    # the users username.
    username=None, )

```

#### Functions:

##### delete:
``` python

# call user.delete.
response = user.delete()

```
##### check:
``` python

# call user.check.
response = user.check(silent=False)

```
##### set_password:
``` python

# call user.set_password.
response = user.set_password(password=None)

```
##### add_groups:
``` python

# call user.add_groups.
response = user.add_groups(groups=[])

```
##### delete_groups:
``` python

# call user.delete_groups.
response = user.delete_groups(groups=[])

```

## WebServer:
The web_server object class.
``` python 

# initialize the web_server object class.
web_server = syst3m.classes.cache.WebServer(
    id="webserver",
    host="127.0.0.1",
    port=52379,
    path=None,
    default={},
    # do not use.
    serialized={}, )

```

#### Functions:

##### set:
``` python

# call web_server.set.
response = web_server.set(group=None, id=None, data=None, timeout=3)

```
##### get:
``` python

# call web_server.get.
response = web_server.get(group=None, id=None, timeout=3)

```
##### app:
``` python

# call web_server.app.
_ = web_server.app()

```
##### get:
``` python

# call web_server.get.
response = web_server.get()

```
##### set:
``` python

# call web_server.set.
response = web_server.set()

```
##### active:
``` python

# call web_server.active.
response = web_server.active()

```
##### run:
``` python

# call web_server.run.
_ = web_server.run()

```
##### fork:
``` python

# call web_server.fork.
response = web_server.fork(timeout=15, sleeptime=1)

```
##### stop:
``` python

# call web_server.stop.
response = web_server.stop()

```
##### start_thread:
``` python

# call web_server.start_thread.
response = web_server.start_thread(thread, group="daemons", id=None)

```
##### get_thread:
``` python

# call web_server.get_thread.
response = web_server.get_thread(group="daemos", id=None)

```

#### Properties:
```python

# the token property.
token = web_server.token
```
```python

# the running property.
running = web_server.running
```

#### alias:
The syst3m.classes.defaults.alias function.
``` python

# call syst3m.classes.defaults.alias.
_ = syst3m.classes.defaults.alias(
    # the source name.
    alias=None, 
    # the source path.
    executable=None,
    # can use sudo.
    sudo=False,
    # overwrite.
    overwrite=False, )

```
#### check_group:
The syst3m.classes.system.check_group function.
``` python

# call syst3m.classes.system.check_group.
response = syst3m.classes.system.check_group(id, users=[], create=False, overwrite=False)

```
#### check_os:
The syst3m.classes.disks.check_os function.
``` python

# call syst3m.classes.disks.check_os.
response = syst3m.classes.disks.check_os(supported=["linux"], error=False)

```
#### check_user:
The syst3m.classes.system.check_user function.
``` python

# call syst3m.classes.system.check_user.
response = syst3m.classes.system.check_user(id, create=False)

```
#### execute:
The syst3m.classes.console.execute function.
``` python

# call syst3m.classes.console.execute.
_ = syst3m.classes.console.execute(
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
    serialize=False, )

```
#### input:
The syst3m.classes.console.input function.
``` python

# call syst3m.classes.console.input.
_ = syst3m.classes.console.input(message, yes_no=False)

```
#### kill:
The syst3m.classes.defaults.kill function.
``` python

# call syst3m.classes.defaults.kill.
response = syst3m.classes.defaults.kill(
    # option 1:
    # the process id.
    pid=None, 
    # option 2:
    # all processes that includes.
    includes=None,
    # root permission required.
    sudo=False,
    # loader.
    log_level=0, )

```
#### log_level:
The syst3m.classes.defaults.log_level function.
``` python

# call syst3m.classes.defaults.log_level.
_ = syst3m.classes.defaults.log_level(default=0)

```
#### operating_system:
The syst3m.classes.defaults.operating_system function.
``` python

# call syst3m.classes.defaults.operating_system.
_ = syst3m.classes.defaults.operating_system(supported=["*"])

```
#### processes:
The syst3m.classes.defaults.processes function.
``` python

# call syst3m.classes.defaults.processes.
response = syst3m.classes.defaults.processes(
    # root permission.
    sudo=False,
    # all processes that include a str.
    includes=None,
    # banned process names.
    banned=["grep"], )

```
#### pwd:
The syst3m.classes.defaults.pwd function.
``` python

# call syst3m.classes.defaults.pwd.
_ = syst3m.classes.defaults.pwd()

```
#### source_path:
The syst3m.classes.defaults.source_path function.
``` python

# call syst3m.classes.defaults.source_path.
_ = syst3m.classes.defaults.source_path(path, back=1)

```
