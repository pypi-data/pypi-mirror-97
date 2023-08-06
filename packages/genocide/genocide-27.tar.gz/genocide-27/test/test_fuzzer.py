# This file is placed in the Public Domain.

"fuzz arguments"

# imports

import inspect
import ob
import ob.hdl
import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from ob.evt import Event
from ob.krn import cfg, parse
from ob.hdl import Handler
from ob.utl import get_exception

from test.run import h

# defines

def cb(event):
    if cfg.verbose:
        print("yoo")

exclude = ["announce", "direct", "poll", "handler", "input", "doconnect", "raw", "say", "start"]
exc = []
result = []

values = ob.Object()
values["txt"] = "yoo2"
values["key"] = "txt"
values["value"] = ob.Object()
values["d"] = {}
values["hdl"] = h
values["event"] = Event({"txt": "thr", "error": "test"})
values["path"] = cfg.wd
values["channel"] = "#operbot"
values["orig"] = repr(values["hdl"])
values["obj"] = ob.Object()
values["d"] = {}
values["value"] = 1
values["pkgnames"] = "op"
values["name"] = "operbot"
values["callback"] = cb
values["e"] = Event()
values["mod"] = ob.hdl.cmd
values["mns"] = "irc,udp,rss"
values["sleep"] = 60.0
values["func"] = cb
values["origin"] = "test@shell"
values["perm"] = "USER"
values["permission"] = "USER"
values["text"] = "yoo"
values["server"] = "localhost"
values["nick"] = "bot"
values["rssobj"] = ob.Object()
values["o"] = ob.Object()
values["handler"] = h

# classes

class Test_Fuzzer(unittest.TestCase):

    def test_fuzz(self):
        global exc
        m = ob.mods("ob,gcd")
        for x in range(cfg.index or 1):
            for mod in m:
                fuzz(mod)
        exc = []

# functions

def get_values(vars):
    args = []
    for k in vars:
        res = ob.get(values, k, None)
        if res:
            args.append(res)
    return args

def handle_type(ex):
    if cfg.verbose:
        print(ex)

def fuzz(mod, *args, **kwargs):
    for name, o in inspect.getmembers(mod, inspect.isclass):
        o.stopped = True
        if "_" in name:
            continue
        try:
            oo = o()
        except TypeError as ex:
            handle_type(ex)
            continue
        for name, meth in inspect.getmembers(oo):
            if "_" in name or name in exclude:
                continue
            try:
                spec = inspect.getfullargspec(meth)
                args = get_values(spec.args[1:])
            except TypeError as ex:
                handle_type(ex)
                continue
            try:
                print(meth)
                res = meth(*args, **kwargs)
                if cfg.verbose:
                    print("%s(%s) -> %s" % (name, ",".join([str(x) for x in args]), res))
            except Exception as ex:
                if cfg.verbose:
                    print(get_exception())
