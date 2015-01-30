#!/usr/bin/env python
# this python script can load themes for pantheon terminal
#
# written for the linux distro 'elementary OS', maybe it also runs
# under other distros
#
# Usage:
# ./theme-switcher.py path/to/theme
#

import sys
import json
import os

# set settings string
sets = "gsettings set org.pantheon.terminal.settings"

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

if len(sys.argv) == 2:
    theme_path = sys.argv[1]
else:
    theme_path = raw_input("path to your theme: ")

print "trying to parse theme " + theme_path
theme = json.loads(open(theme_path, "r").read())

print "loaded theme '" + theme["name"] + "'"

os.system(sets + " opacity " + str(theme["style"]["opacity"]))
os.system(sets + " background \"" + theme["style"]["background"] + "\"")
os.system(sets + " foreground \"" + theme["style"]["foreground"] + "\"")
os.system(sets + " cursor-color \"" + theme["style"]["cursor-color"] + "\"")
os.system(sets + " palette \"" + createPalette() + "\"")
