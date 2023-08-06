#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from netw0rk.classes import *

# source path & version.
import fil3s
source = fil3s.gfp.base(__file__)
try: version = fil3s.Files.load(source+".version.py").replace("\n","").replace(" ","")
except: version = None