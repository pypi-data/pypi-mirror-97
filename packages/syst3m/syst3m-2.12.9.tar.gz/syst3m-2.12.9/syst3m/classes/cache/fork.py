#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, cl1, json
from fil3s import *
sys.path.insert(1, FilePath(__file__).base(back=4))
from syst3m.classes.cache import WebServer
webserver = WebServer(serialized=json.loads(cl1.get_argument("--serialized")[1:-1]))
webserver.start()