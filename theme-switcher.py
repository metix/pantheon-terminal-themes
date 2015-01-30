#!/usr/bin/env python
# this python script can load (and save) themes for pantheon terminal
#
# written for the linux distro 'elementary OS', maybe it also runs
# under other distros
#
# Usage:
# set a theme:
# ./theme-switcher.py --load path/to/theme
#
# save currrent theme:
# ./theme-switcher.py --save path/to/newtheme
#

import sys
import json
import os
import argparse
from subprocess import Popen, PIPE
from collections import OrderedDict

# path of the pantheon terminal settings
ppath = "org.pantheon.terminal.settings"

def getValue(key):
	try:
		return Popen(["gsettings", "get", ppath, key], stdout=PIPE).communicate()[0].rstrip().replace("'", "")
	except OSError, msg:
		print "error while trying to execute 'gsettings': " + str(msg)
		sys.exit(-1)

def setValue(key, value):
	try:
		Popen(["gsettings", "set", ppath, key, value], stdout=PIPE).communicate()[0]
	except OSError, msg:
		print "error while trying to execute 'gsettings': " + str(msg)
		sys.exit(-1)

parser = argparse.ArgumentParser(description='theme switcher for pantheon-terminal')

parser.add_argument('--load', '-l', action="store_true", help="load a theme")
parser.add_argument('--save', action="store_true", help="save the current theme in a new file")
parser.add_argument("themefile", help="path of .theme file")

try:
	args = parser.parse_args()
except IOError, msg:
	parser.error(str(msg))

if args.load == False and args.save == False or args.load == True and args.save == True:
	parser.error("you have to say '--load' to set a theme xor '--save' to save the current theme")
elif args.load == True:
	print "trying to parse theme " + args.themefile

	try:
		theme = json.loads(open(args.themefile, "r").read())
	except ValueError, msg:
		print "error while parsing json: " + str(msg)
		sys.exit(-1)
	except IOError, msg:
		print "error while reading file: " + str(msg)
		sys.exit(-1)

	def createPalette():
	    palette = theme["style"]["palette"]["black"] + ":"
	    palette += theme["style"]["palette"]["red"] + ":"
	    palette += theme["style"]["palette"]["green"] + ":"
	    palette += theme["style"]["palette"]["yellow"] + ":"
	    palette += theme["style"]["palette"]["blue"] + ":"
	    palette += theme["style"]["palette"]["magenta"] + ":"
	    palette += theme["style"]["palette"]["cyan"] + ":"
	    palette += theme["style"]["palette"]["white"] + ":"
	    palette += theme["style"]["palette"]["lightblack"] + ":"
	    palette += theme["style"]["palette"]["lightred"] + ":"
	    palette += theme["style"]["palette"]["lightgreen"] + ":"
	    palette += theme["style"]["palette"]["lightyellow"] + ":"
	    palette += theme["style"]["palette"]["lightblue"] + ":"
	    palette += theme["style"]["palette"]["lightmagenta"] + ":"
	    palette += theme["style"]["palette"]["lightcyan"] + ":"
	    palette += theme["style"]["palette"]["lightwhite"]
	    return palette

	setValue("opacity", str(theme["style"]["opacity"]))
	setValue("background", theme["style"]["background"])
	setValue("foreground", theme["style"]["foreground"])
	setValue("cursor-color", theme["style"]["cursor-color"])
	setValue("palette", createPalette())

	print "loaded theme '" + theme["name"] + "'"
elif args.save == True:
	def parsePalette():
		palette = getValue("palette").split(":")
		jpalette = OrderedDict({})
		jpalette["black"] = palette[0]
		jpalette["red"] = palette[1]
		jpalette["green"] = palette[2]
		jpalette["yellow"] = palette[3]
		jpalette["blue"] = palette[4]
		jpalette["magenta"] = palette[5]
		jpalette["cyan"] = palette[6]
		jpalette["white"] = palette[7]
		jpalette["lightblack"] = palette[8]
		jpalette["lightred"] = palette[9]
		jpalette["lightgreen"] = palette[10]
		jpalette["lightyellow"] = palette[11]
		jpalette["lightblue"] = palette[12]
		jpalette["lightmagenta"] = palette[13]
		jpalette["lightcyan"] = palette[14]
		jpalette["lightwhite"] = palette[15]

		return jpalette

	theme = OrderedDict({})
	theme["name"] = ""
	theme["description"] = ""
	theme["url"] = ""
	theme["version"] = ""
	theme["style"] = OrderedDict({})
	theme["style"]["opacity"] = int(getValue("opacity"))
	theme["style"]["background"] = getValue("background")
	theme["style"]["foreground"] = getValue("foreground")
	theme["style"]["cursor-color"] = getValue("cursor-color")
	theme["style"]["palette"] = parsePalette()
	theme_json = json.dumps(OrderedDict(theme), indent=4, separators=(',', ': '))

	try:
		open(args.themefile, "w").write(theme_json)
	except IOError, msg:
		print "error while writing theme: " + str(msg)
		sys.exit(-1)

	print "saved to " + args.themefile
