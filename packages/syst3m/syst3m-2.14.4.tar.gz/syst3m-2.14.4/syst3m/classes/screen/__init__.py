#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# pip imports.
if OS in ["linux"]:
	import pyscreenshot as ImageGrab
elif OS in ["macos"]:
	a=1

# the screen object class.
class Screen(object):
	def __init__(self):
		a=1
	def get_pixel(self, x, y):
		im = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # X1,Y1,X2,Y2
		pixel = im.getpixel((0, 0))
		pixel = '#%02x%02x%02x' % pixel
		return pixel

# initialized classes.
screen = Screen()