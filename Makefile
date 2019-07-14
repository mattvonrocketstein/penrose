##
#
##
SHELL := bash -xeuo pipefail -c
MAKEFLAGS += --warn-undefined-variables

THIS_MAKEFILE = $(abspath $(firstword $(MAKEFILE_LIST)))
SRC_ROOT := $(shell dirname ${THIS_MAKEFILE})
MAKE_LIB_DIR := ${SRC_ROOT}/.makefiles
export SRC_ROOT


HFS := /Applications/Houdini/Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources
HOUDINI_DESKTOP_DIR := /Users/matt-admin/Desktop
HOUDINI_OS := 'MacOS
HOUDINI_TEMP_DIR := /tmp/houdini_temp
HOUDINI_USER_PREF_DIR := /Users/matt-admin/Library/Preferences/houdini/17.5
HSITE := /Applications/Houdini/Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/site
export HFS HOUDINI_TEMP_DIR HOUDINI_USER_PREF_DIR #HOUDINI_OS HOUDINI_DESKTOP_DIR

HBIN:=/Applications/Houdini//Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/bin
BLBIN:=/Applications/Blender/blender.app/Contents/MacOS/
PATH:=$(value PATH):${HBIN}:${BLBIN}
export PATH

panic-%:
	export output=$$(ps aux|grep -i ${*} \
	| grep -v grep \
	| awk '{print $$2}' |  xargs -I % -n 1 bash -x -c 'kill -KILL %') \
	||  true


panic: panic-blender panic-houdini

conf:
	hconfig

hou: test panic-houdini
	penrose hx ./houdini/demo-1.py

test:
	export output=$$(! flake8 ./penrose/dorothy.py | grep 'Error\|E112') \
	; export status=$$? \
	; echo $$output \
	; exit $$status

blend:
	path=${SRC_ROOT}/blender/lib.py \
	make blendr

blendr:
	${BLBIN} --foreground --python-console --python $${path}

# shell:
# 	/Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python
#
# https://github.com/kiryha/Houdini/wiki/python-for-artists
# karabiner
# http://www.tokeru.com/cgwiki/index.php?title=HoudiniUserInterfaceTips
#
# scad2stl:
# 	/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD \
# 	 -o $${path}.stl $${path}
#
# python:
# 	@/Applications/Houdini/Houdini17.5.293/Houdini*/Contents/MacOS/happrentice
#
# #https://houdinitricks.com/quicktip-icp-houdini-shell-utility/
# icp:
# 	/Applications/Houdini//Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/bin/icp
# run-%:
# 	ls ${*}; \
# 	cat tests/${*} | make python
