#-------------------------------------------------------------------------------
# Name:        CommonLib
# Purpose:
# A collection of miscellaneous functions that I find useful
#
# Author:      Kaleb McCall
#
# Created:     01/03/2014
# Copyright:   (c) Kaleb McCall 2014
# Licence:
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#-------------------------------------------------------------------------------
import os
from importlib import import_module

def filenames(directory, endswith=None):
    """ Returns a list of all filenames in a given directory. Optional parameter
        can provide filetype matching """

    files = os.listdir()
    if endswith != None:
        files = [file for file in files if file.endswith(endswith)]
    return files

def import_func(module, func):
    """ Imports a function from a given module, function maintains useability
        with the rest of its' own module ie it still has access to constants,
        supporting functions etc """

    mod = import_module(module)
    return getattr(mod, func)