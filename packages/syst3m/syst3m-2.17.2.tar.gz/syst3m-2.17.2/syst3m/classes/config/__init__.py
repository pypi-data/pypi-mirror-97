#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# source.
from dev0s import *
ALIAS = "syst3m"

# 
SOURCE_PATH = Defaults.source_path(path=__file__, back=3)
OS = Defaults.operating_system(supported=["macos", "linux"])

# imports.
#try: 

# pip imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, time, random, threading, urllib, flask, logging, multiprocessing

# inc imports.
from dev0s import *


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
