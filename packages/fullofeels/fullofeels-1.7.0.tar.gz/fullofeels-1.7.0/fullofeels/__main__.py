#!/usr/bin/python

#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Program to generate skeleton code, AKA the boring bits,
#   for a Python module implemented in C.
#   Named after a Monty Python sketch with inaccurate translation

#   VERSION
#   1.0     Apr 2016    Modules, methods, classes, object builtin methods
#   1.1     Nov 2016    Sequence, mapping, number, and buffer builtin methods
#   1.2     Feb 2017    Can specify argument types for PyArg_ParseTuple
#   1.3     Oct 2017    Properties on class become members in struct
#   1.4     Nov 2017    Generates setup.py for module
#   1.5     Jan 2019    Now run as -m package, not separate script
#   1.6     Feb 2021    Automate testing on Windows, cleanup for PyPI release
#   1.7     Mar 2021    Type annotations recognised for parameters

from __future__ import division, print_function

import sys, os, inspect, argparse
import importlib
from os import path
import logging

import fullofeels
from fullofeels.i18nstr import _T
from fullofeels import py27, py3x, ccode, setupfile

__version__ = "1.7"

def loadModuleObject(srcName):
    """Load the given filename as a Python module"""
    modName = path.splitext(path.basename(srcName))[0]
    modDir = path.dirname(srcName)
    # Modifying the search path could maybe cause problems for other
    # modules later on, but fullofeels is almost always used for
    # just one module so not worth worrying about
    if modDir:
        sys.path.append(modDir)
    mod = importlib.import_module(modName)
    # If the load fails, usually means a syntax error in the module source
    # Presumably the user will want to fix it rather than keep going
    return mod

def parseArgs(argv):
    """Return arguments object with various options for code generation"""
    parser = argparse.ArgumentParser(
        description=_T("Creates module.h, module.c, setup.py skeleton code for native extension module"))
    parser.add_argument("sources", metavar="module.py", nargs="+",
            help=_T("Python module file name"))
    parser.add_argument("-c", dest="ext", action="store_const", const=".c", default=".c",
            help=_T("Create .h/.c files (default)"))
    parser.add_argument("-cpp", dest="ext", action="store_const", const=".cpp", default=".c",
            help=_T("Create .h/.cpp"))
    parser.add_argument("-objc", dest="ext", action="store_const", const=".m", default=".c",
            help=_T("Create .h/.m"))
    parser.add_argument("-nosetup", dest="createSetup", action="store_false", default=True,
            help=_T("Do not create setup.py"))
    parser.add_argument("-backup", dest="backup", action="store_true", default=False,
            help=_T("Backup existing files first"))
    parser.add_argument("-diff", dest="diff", action="store_true", default=True,
            help=_T("Diff new code into existing file"))
    parser.add_argument("-print", dest="printf", action="store_true", default=False,
            help=_T("Add printf statements to all method stubs"))
    parser.add_argument("-ascii", dest="ascii", action="store_true", default=False,
            help=_T("My C compiler does not understand UTF-8"))
    parser.add_argument("-hifdef", dest="hdrIfDef", action="store_true", default=False,
            help=_T("Insert old style #ifdef header guards instead of #pragma once"))
    parser.add_argument("-info", dest="logLevel", action="store_const", const=logging.INFO, default=logging.WARNING,
            help=_T("Show INFO level log messages"))
    parser.add_argument("-debug", dest="logLevel", action="store_const", const=logging.DEBUG, default=logging.WARNING,
            help=_T("Show DEBUG level log messages"))
    parser.add_argument("-v", "-version", action="version", version="fullOfEels " + __version__)

    cmdArgs = parser.parse_args(argv)
    return cmdArgs


##      Main

options = parseArgs(sys.argv[1:])
logging.basicConfig(level=options.logLevel, format="%(levelname)s: %(message)s")

# Rare (?) usage that won't work
if options.createSetup and len(options.sources) > 1:
    logging.warning("Cannot create setup.py for multiple modules")
    options.createSetup = False

ccode.setOptions(options)

# Pick code generator
major = ccode.targetVersion[0]
if major < 2 or major > 3:
    raise RuntimeError(_T("Not sure how to generate C code for Python version {0}").format(major))

# For now, just one
if major == 2:
    coder = py27.CModCoder(options)
elif major == 3:
    coder = py3x.CModCoder(options)

if options.createSetup:
    setup = setupfile.SetupScript(options)

# This creates a dummy fullofeels package that can be imported
# by the module being loaded without worrying about the path.
# Contains a few utility decorators and classes.
# Yeah this is not best practice
sys.modules["fullofeels"] = fullofeels.visible

for src in options.sources:
    mod = loadModuleObject(src)
    coder.config(mod)
    try:
        coder.beginModule()
        coder.genDefinitions()
        coder.genInitFunction()
        coder.endModule()
        if options.createSetup:
            setup.addExtension(coder)
    finally:
        coder.close()

if options.createSetup:
    try:
        setup.generate()
    finally:
        setup.close()

logging.debug("Done.")
