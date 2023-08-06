#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# pip imports.
if OS in ["linux"]:
	import pyautogui
elif OS in ["macos"]:
	a=1

# the screen object class.
class Keyboard(object):
	def __init__(self):
		a=1
	def write(self, 
		# the string message.
		string, 
		# the sleep interval (int).
		sleep=None,
		# the interval between keystrokes.
		interval=0.25,
	):
		pyautogui.write(string, interval=interval)
		if isinstance(sleep, int):
			time.sleep(sleep)
	def press(self, 
		# the string message.
		key, 
		# the sleep interval (int).
		sleep=None,
	):
		pyautogui.press(key)
		if isinstance(sleep, int):
			time.sleep(sleep)
	def key_up(self, 
		# the string message.
		key, 
		# the sleep interval (int).
		sleep=None,
	):
		pyautogui.keyUp(key)
		if isinstance(sleep, int):
			time.sleep(sleep)
	def key_down(self, 
		# the string message.
		key, 
		# the sleep interval (int).
		sleep=None,
	):
		pyautogui.keyDown(key)
		if isinstance(sleep, int):
			time.sleep(sleep)
	def copy(self, 
		# the sleep interval (int).
		sleep=None,
	):
		pyautogui.hotkey('ctrl', 'c')
		if isinstance(sleep, int):
			time.sleep(sleep)
	def paste(self, 
		# the sleep interval (int).
		sleep=None,
	):
		pyautogui.hotkey('ctrl', 'v')
		if isinstance(sleep, int):
			time.sleep(sleep)


# initialized classes.
keyboard = Keyboard()