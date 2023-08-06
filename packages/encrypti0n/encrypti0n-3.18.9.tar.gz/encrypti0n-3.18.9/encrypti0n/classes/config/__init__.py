#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, random
import syst3m, cl1
from r3sponse import r3sponse
from fil3s import *

# source.
ALIAS = "encrypti0n"
SOURCE_NAME = "encrypti0n"
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=3)
BASE = syst3m.defaults.source_path(SOURCE_PATH)
OS = syst3m.defaults.operating_system(supported=["linux", "macos"])
syst3m.defaults.alias(alias=ALIAS, executable=f"{SOURCE_PATH}/", sudo=True)

# file settings.
ADMINISTRATOR = "administrator"
OWNER = os.environ.get("USER")
GROUP = "root"
if OS in ["macos"]: GROUP = "wheel"
SUDO = True
ADMIN_PERMISSION = 700
READ_PERMISSION = 750
WRITE_PERMISSION = 770

