#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random
from fil3s import *
from r3sponse import r3sponse

# functions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# source.
SOURCE_NAME = ALIAS = "cl1"
SOURCE_PATH = FilePath(__file__).base(back=3)
OS = __get_operating_system__()

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME = os.environ.get('HOME')
HOME_BASE = gfp.base(path=HOME)
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["macos"]: 
	MEDIA = f"/Volumes/"
	GROUP = "wheel"
