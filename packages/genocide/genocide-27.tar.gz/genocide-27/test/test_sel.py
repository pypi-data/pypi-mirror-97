# This file is placed in the Public Domain.

"select tests"

# imports

import unittest

from ob.krn import cfg
from ob.sel import Select

from test.run import exec

# classes

class Test_Select(unittest.TestCase):

    def test_sel(self):
        for x in range(cfg.index or 1):
            tests(t)

# functions

def tests(t):
    for cmd in t.cmds:
        exec(cmd)

# runtime

t = Select()
t.start()
