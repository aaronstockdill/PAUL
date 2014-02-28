#-------------------------------------------------------------------------------
# Name:        P.A.U.L. Parser
# Purpose:
# A command processing wrapper. The object processes a sentance and sends the
# valid data to the relevant module.
#
# Author:      Kaleb McCall
# Created:     28/02/2014
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

import brain
import os
import common

DECLARATIVE = 0
IMPERATIVE = 1
INTERROGATIVE = 2
MODULES_FOLDER = "Modules"

class Parser(object):
    """ Main Parsing object, handles module lists and session information """

    def __init__(self):
        """ Constructor """
        self.memory = {}
        self.modules = [{}, {}, {}]
        self.working_sentance = None


    def parse(self, sentance):
        """ Takes a sentance, processes, and directs it to the relevant module """
        self.working_sentance = sentance
        if sentance.kind == "IMP":
            # Imperative
            # Check for hidden interrogative, ie *GO* to x and *SEARCH* for y
            pass
        elif sentance.kind == "INT":
            # Interrogative
            pass
        else:
            # Declarative
            pass
        self.working_sentance = None


    def load_modules(self):
        """ Load all modules in the Modules folder """
        modules = common.filenames("{}\\{}".format(__file__, MODULES_FOLDER), ".py")
        keywords = {}
        for module in modules:
            func = common.import_func(module, "main")
            module_type, name, keywords = func()
            self.modules[module_type][name] = module


    def _declarative(self, info):
        """ Parse some information """
        pass


    def _imperative(self, command):
        """ Parse a command """
        pass


    def _interrogative(self, question):
        """ Parse a question """
        pass