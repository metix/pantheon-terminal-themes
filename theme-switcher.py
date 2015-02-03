#!/usr/bin/env python
# this python script can load (and save) themes for pantheon terminal
#
# written for the linux distro 'elementary OS', maybe it also runs
# under other distros
#
# Usage:
# set a theme:
# ./theme-switcher.py load [options] path/to/theme
#	[options]
#		--font      load font and fontsize too (if font is defined in theme)
#
# save currrent theme:
# ./theme-switcher.py save [options] path/to/newtheme
#	[options]
#		--font      save font and fontsize too
#
# print all color variations of current eheme
# ./theme-switcher.py test
#

import sys
import json
import os
import argparse
import fileinput
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

def test_colors():
	text = "hello world"
	for i in range(7):
		# dark
		sys.stdout.write("3%dm \33[2;3%dm%s\33[0m " % (i, i, text))

		# light
		sys.stdout.write("\33[0;3%dm%s\33[0m " % (i, text))

		# bold
		sys.stdout.write("\33[1;3%dm%s\33[0m " % (i, text))

		# underline
		sys.stdout.write("\33[4;3%dm%s\33[0m " % (i, text))

		# strike
		sys.stdout.write("\33[9;3%dm%s\33[0m\n" % (i, text))

parser = argparse.ArgumentParser(description='theme switcher for pantheon-terminal')
subparsers = parser.add_subparsers(help="describes the mode")

parser_save = subparsers.add_parser("save", help="save current file")
parser_save.set_defaults(which="save")
parser_save.add_argument("--font", action="store_true", help="save font and fontsize too")
parser_save.add_argument("themefile", help="path of theme-file")

parser_load = subparsers.add_parser("load", help="load a theme of a theme-file")
parser_load.set_defaults(which="load")
parser_load.add_argument("--font", action="store_true", help="load font and fontsize too (if defined)")
parser_load.add_argument("themefile", help="path of theme-file")

parser_test = subparsers.add_parser("test", help="print text with all color variation")
parser_test.set_defaults(which="test")

try:
	args = parser.parse_args()
except IOError, msg:
	parser.error(str(msg))

if args.which == "test":
	test_colors()
	sys.exit(0)

elif args.which == "load":
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
	if args.font == True and "font" in theme["style"]:
		setValue("font", theme["style"]["font"])

	print "loaded theme '" + theme["name"] + "'"
elif args.which == "save":
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
	if args.font == True:
		theme["style"]["font"] = getValue("font")
	theme["style"]["palette"] = parsePalette()
	theme_json = json.dumps(OrderedDict(theme), indent=4, separators=(',', ': '))

	try:
		if os.path.isfile(args.themefile):
			decision = raw_input("theme is already defined. override? [y/n]? ")
			if decision != "y":
				print "abort."
				sys.exit(0)
		open(args.themefile, "w").write(theme_json)
	except IOError, msg:
		print "error while writing theme: " + str(msg)
		sys.exit(-1)

	print "saved to " + args.themefile
