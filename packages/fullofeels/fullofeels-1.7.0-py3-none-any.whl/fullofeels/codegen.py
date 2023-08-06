
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Writing C output files

from __future__ import division, print_function

import os
from os import path
import shutil
import difflib
from io import StringIO
import codecs

from fullofeels.i18nstr import _T

# HACK to support Python 2 and 3 because StringIO only works with unicode.
# If I run python2 with -U to auto convert, a bunch of site-packages raise
# exceptions in their init code. Nothing I can do about that.
# Wrapping strings with unicode works for Python2, but unicode() does
# not exist in Python 3. So fake it until I decide to support only 3
import sys
if sys.version_info[0] > 2:
    def unicode(s): return s


# Standard indent 4 spaces
indentStr = "    "

class CFile(object):
    """Text output only file with convenience routines for C code"""

    def __init__(self, fileName, diff=False, backup=False):
        """Diff puts old/new comparison in output, backup makes .bak of old"""
        self.fileName = fileName
        self.backup = backup
        self.diff = diff
        #
        # DON'T open actual file. Wait until get to close(), so any
        # errors don't wipe out previous file without creating new
        self.f = StringIO()
        self.iLevel = 0

    def close(self):
        """Actually write file contents"""
        # Backup if requested
        if self.backup and os.path.isfile(self.fileName):
            shutil.copy2(self.fileName, self.fileName + ".bak")
        #
        self.f.flush()
        self.f.seek(0)
        if self.diff and os.path.isfile(self.fileName):
            self.writeDiffOutput()
        else:
            # Easy
            out = codecs.open(self.fileName, 'w', 'utf-8')
            for line in self.f.readlines():
                out.write(line)
            out.close()
        self.f.close()
        self.f = None

    def writeDiffOutput(self):
        # Read the existing file
        oldFile = open(self.fileName, 'r')
        oldCode = oldFile.readlines()
        oldFile.close()
        newCode = self.f.readlines()
        # Run diff
        diff = difflib.Differ()
        finalVersion = diff.compare(oldCode, newCode)
        # and write
        out = codecs.open(self.fileName, 'w', 'utf-8')
        for line in finalVersion:
            # Only want prefix on differences
            if line[0] not in '-+?!':
                line = line[2:]
            out.write(line)
        out.close()

    def code(self, line, semi=None):
        """Write a line of code, indented and appending \n.
           If it ends with { or } or comma and semi is not True, no semicolon
           If it doesn't and semi is not False, gets a semicolon.
           Might sound weird, but see how it gets used"""
        if line.endswith("{") or line.endswith("}") or line.endswith(","):
            if semi == True:
                line += ";"
        else:
            if semi != False:
                line += ";"
        pad = indentStr * self.iLevel
        self.f.write(unicode(pad + line + "\n"))

    def LF(self):
        """Insert blank line"""
        self.write("\n")

    def comment(self, text):
        """Write out text as C comment. Can be multiline"""
        lines = [s.strip() for s in text.splitlines()]
        if len(lines) == 1:
            pad = indentStr * self.iLevel
            self.f.write(unicode(pad + "/* " + lines[0] + " */\n"))
        else:
            self.f.write(unicode("/*" + indentStr[2:] + lines[0] + "\n"))
            for s in lines[1:-1]:
                self.f.write(unicode(indentStr + s + "\n"))
            self.f.write(unicode(indentStr + lines[-1] + indentStr[0:-2] + "*/\n"))

    def indent(self):
        """Increase indent level by 1"""
        self.iLevel += 1

    def unindent(self):
        """Decrease, don't let it go negative"""
        self.iLevel = max(self.iLevel - 1, 0)

    def setIndent(self, level):
        """Reset indent level"""
        if level < 0:
            raise ValueError(_T("Set indent level {0} negative!").format(level))
        self.iLevel = level

    # Standard file output, unchanged

    def write(self, s):
        self.f.write(unicode(s))

    def writelines(self, lines):
        # Have to loop because of unicode conversion in Python 2
        #self.f.writelines(lines)
        for s in lines:
            self.f.write(unicode(s))
