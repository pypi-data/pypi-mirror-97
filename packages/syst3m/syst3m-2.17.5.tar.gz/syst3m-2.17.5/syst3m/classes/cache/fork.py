#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, ast, json
from dev0s import *
sys.path.insert(1, FilePath(__file__).base(back=4))
from syst3m.classes.cache import WebServer
webserver = WebServer(serialized=ast.literal_eval(CLI.get_argument("--serialized")[1:-1]))
webserver.start()