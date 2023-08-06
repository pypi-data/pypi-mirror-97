#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, glob, platform, subprocess, random
import traceback as _traceback_

# inc imports.
from fil3s import *

# functions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# source.
ALIAS = SOURCE_NAME = "r3sponse"
SOURCE = Directory(gfp.base(__file__, back=3))
OS = __get_operating_system__()

# options.
ERROR_TRACEBACK = os.environ.get("R3SPONSE_ERROR_TRACEBACK")
if str(ERROR_TRACEBACK) in ["True", "true", True]: ERROR_TRACEBACK = True
else: ERROR_TRACEBACK = False
