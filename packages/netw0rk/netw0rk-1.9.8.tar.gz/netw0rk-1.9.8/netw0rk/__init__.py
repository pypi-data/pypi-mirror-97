#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from netw0rk.classes import *

# source path & version.
from dev0s import Version, Directory, Files, gfp
source = Directory(gfp.base(__file__))
base = Directory(source.fp.base())
try: version = Version(Files.load(source.join(".version.py")))
except: version = None