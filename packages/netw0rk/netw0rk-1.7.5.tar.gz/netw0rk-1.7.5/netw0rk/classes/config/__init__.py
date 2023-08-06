#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, socket, time

# inc imports.
import syst3m, cl1
from fil3s import *
from r3sponse import r3sponse

# source.
ALIAS = "netw0rk"
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=3)
OS = syst3m.defaults.operating_system(supported=["macos", "linux"])
syst3m.defaults.alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["macos"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

