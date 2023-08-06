#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, socket, time

# inc imports.
import syst3m
from dev0s import *

# source.
ALIAS = "netw0rk"
SOURCE_PATH = Defaults.source_path(__file__, back=3)
OS = Defaults.operating_system(supported=["macos", "linux"])
Defaults.alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

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

