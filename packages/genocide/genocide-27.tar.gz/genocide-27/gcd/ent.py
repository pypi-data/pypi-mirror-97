# This file is placed in the Public Domain.

"log/todo"

# imports

import ob

# classes

class Log(ob.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(ob.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

# commands

def dne(event):
    if not event.res.args:
        return
    selector = {"txt": event.res.args[0]}
    for fn, o in ob.dbs.find("gcd.ent.Todo", selector):
        o._deleted = True
        ob.save(o)
        event.reply("ok")
        break

def log(event):
    if not event.res.rest:
        return
    l = Log()
    l.txt = event.res.rest
    ob.save(l)
    event.reply("ok")

def tdo(event):
    if not event.res.rest:
        return
    o = Todo()
    o.txt = event.res.rest
    ob.save(o)
    event.reply("ok")
