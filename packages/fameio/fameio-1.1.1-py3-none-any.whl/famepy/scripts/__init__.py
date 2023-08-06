# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

from famepy.scripts.make_config import run as make_config
from famepy.scripts.convert_results import run as convert_results


def makeFameRunConfig():
	if len(sys.argv) != 2:
		print("Usage: makeFameRunConfig <path/to/configuration/file.yaml>")
	else:
		make_config(sys.argv[1])


def convertFameResults():
	if len(sys.argv) > 2:
		convert_results(sys.argv[1], sys.argv[2].upper())
	elif len(sys.argv) == 2:
		convert_results(sys.argv[1])
	else:
		print("Usage: convertFameResults <path/to/result/file.pb> ['list', 'of', 'agents']")
