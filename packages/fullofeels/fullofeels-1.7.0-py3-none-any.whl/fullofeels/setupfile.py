
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Generates setup.py for a single module. I thought about
#   creating setups for multiple modules, but too much work
#   for what (for me anyway) is an unusual case. Multiple
#   modules implies a package with __init__.py with a different
#   name, possibly multiple authors, ...

from __future__ import division, print_function

import inspect, os
from os import path
import logging

from fullofeels import codegen
from fullofeels.i18nstr import _T

dquote = '"'

class SetupScript(object):
    """Build setup.py for extension module"""

    def __init__(self, options):
        """Options is argparse object"""
        self.opts = options
        self.sourceNames = []
        self.f = None
        # All the setup args and other things for final script
        self.args = {}
        self.setDefaultArgs()

    def setDefaultArgs(self):
        """Just mark everything as TODO for now"""
        # Keys with dunder names correspond to module vars
        for key in ("moduleName",
                    "sourceFileList",
                    "__version__",
                    "description",
                    "long_description",
                    "__author__",
                    "author_email",
                    "url",
                    "__license__",):
            self.args[key] = "TODO"

    def addExtension(self, modCoder):
        """Add CModCoder object to setup"""
        if self.f is None:
            # We're not generating C code, but do want to use backup and/or diff for output
            setupName = path.join(modCoder.basePath, "setup.py")
            self.f = codegen.CFile(setupName, diff=self.opts.diff, backup=self.opts.backup)
            logging.info("Create " + self.f.fileName)
        # Need the file name but not full path
        self.sourceNames.append(dquote + os.path.basename(modCoder.body.fileName) + dquote)
        # Assuming setup.py is for a single module
        self.args["moduleName"] = modCoder.name
        # Insert special values, as strings
        modAttr = modCoder.source.__dict__
        for arg in ("__version__", "__license__", "__author__"):
            if arg in modAttr:
                self.args[arg] = u"{}".format(modAttr[arg])
        # Docstring becomes description or long_description
        docString = inspect.getdoc(modCoder.source)
        if docString:
            if len(docString) < 80 and len(docString.splitlines()) == 1:
                self.args["description"] = docString
            else:
                self.args["long_description"] = docString


    def generate(self):
        """All modules added, so write the script"""
        logging.debug("Generate setup.py")
        # Need to build the source file list
        self.args["sourceFileList"] = ", ".join(self.sourceNames)
        self.f.write(setupCode.format(**self.args))

    def close(self):
        self.f.close()
        self.f = None


# Template for setup.py
# There are many, many options for a setup.py file. Because fullofeels
# is meant to get you started, not do everything, this just includes
# what IMHO are the most common and useful.
# If you add new template values, remember to update setDefaultArgs.

# This should be a Unicode string because output is Python, not C
setupCode = u"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension

theModule = Extension("{moduleName}",
        sources = [ {sourceFileList} ])

setup(name = "{moduleName}",
        version = "{__version__}",
        description = "{description}",
        long_description = \"\"\"{long_description}\"\"\",
        author = "{__author__}",
        author_email = "{author_email}",
        url = "{url}",
        license="{__license__}",
        ext_modules = [theModule]
        )
"""
