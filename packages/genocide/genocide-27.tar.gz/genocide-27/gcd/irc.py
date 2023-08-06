# This file is placed in the Public Domain.

"internet relay chat"

# imports

import ob
import os
import queue
import socket
import textwrap
import time
import threading
import  _thread

from ob import Cfg, Object, edit, format, save
from ob.bus import Bus
from ob.dbs import find, last
from ob.evt import Event
from ob.hdl import Bused, Handler, cmd
from ob.thr import launch
from ob.utl import locked

# defines

def init(hdl):
    i = IRC()
    ob.update(i.cmds, hdl.cmds)
    i.start()
    return i

saylock = _thread.allocate_lock()

# exceptions

class ENOUSER(Exception):

    pass

# classes

class Cfg(Cfg):

    channel = "#genocide"
    nick = "genocide"
    port = 6667
    server = "localhost"
    realname = "the king of the netherlands commits genocide"
    username = "genocide"

    def __init__(self):
        super().__init__()
        self.channel = Cfg.channel
        self.nick = Cfg.nick
        self.port = Cfg.port
        self.server = Cfg.server
        self.realname = Cfg.realname
        self.username = Cfg.username

class Event(Event):

    pass

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450

class IRC(Handler):

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._joined = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._trc = ""
        self.cc = "!"
        self.cfg = Cfg()
        self.cmds = Object()
        self.channels = []
        self.register("cmd", cmd)
        self.register("ERROR", self.ERROR)
        self.register("LOG", self.LOG)
        self.register("NOTICE", self.NOTICE)
        self.register("PRIVMSG", self.PRIVMSG)
        self.register("QUIT", self.QUIT)
        self.register("366", self.JOINED)
        self.speed = "slow"
        self.state = Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.users = Users()
        Bus.add(self)

    def _connect(self, server, port=6667):
        if ob.krn.cfg.resume:
            s = socket.fromfd(ob.krn.cfg.resume, socket.AF_INET, socket.SOCK_STREAM)
            ob.krn.resume[repr(self)] = s.fileno()
            s.command('PING", ":RESUME %s' % str(time.time()))
            s.connected.set()
            self.say(self.cfg.channel, 'done')
        else:
            addr = socket.getaddrinfo(server, port, socket.AF_INET)[-1][-1]
            s = socket.create_connection(addr)
            self.cfg.resume = s.fileno()
            os.set_inheritable(self.cfg.resume, os.O_RDWR)
        s.setblocking(True)
        s.settimeout(1200.0)
        self._sock = s
        self._fsock = self._sock.makefile("r")
        self._connected.set()
        return True

    def _parsing(self, txt):
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        if ob.krn.cfg.verbose:
            print(rawstr)
        o = Event()
        o.rawstr = rawstr
        o.orig = repr(self)
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
                o.type = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    @locked(saylock)
    def _say(self, channel, txt):
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            if not t:
                continue
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def _some(self):
        inbytes = self._sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self, server, nick, port=6667):
        nr = 0
        while not self.stopped:
            self.state.nrconnect += 1
            if self._connect(server, port):
                break
            time.sleep(10.0)
            nr += 1
        else:
            self._connected.set()
        if self._sock:
            self.logon(server, nick)

    def doconnect(self):
        assert self.cfg.server
        assert self.cfg.nick
        super().start()
        launch(self.input)
        launch(self.output)
        self.connect(self.cfg.server, self.cfg.nick, int(self.cfg.port) or 6667)

    def handle(self, event):
        if event.command in self.cbs:
            self.cbs[event.command](event)

    def input(self):
        self._connected.wait()
        while not self.stopped:
            try:
                e = self.poll()
            except (OSError, ConnectionResetError, socket.timeout) as ex:
                e = Event()
                e.error = str(ex)
                self.ERROR(e)
                break
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            self.handle(e)

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        assert self.cfg.username
        assert self.cfg.realname
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname))

    def output(self, once=False):
        while not self.stopped:
            channel, txt = self._outqueue.get()
            if channel is None:
                break
            if txt:
                self._say(channel, txt)
            if once:
                break
            time.sleep(0.01)

    def poll(self):
        if not self._buffer:
            self._some()
        if not self._buffer:
            return
        e = self._parsing(self._buffer.pop(0))
        cmd = e.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "366":
            self._joined.set()
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick)
        return e

    def raw(self, txt):
        if not self._sock:
            return
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        try:
            self._sock.send(txt)
        except (OSError, ConnectionResetError) as ex:
            e = Event()
            e.error = str(ex)
            self.LOG(e)
            self._connected.clear()
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt):
        self._outqueue.put_nowait((channel, txt))

    def start(self, cfg=None):
        if self.stopped:
            return
        if cfg is not None:
            self.cfg.update(cfg)
        else:
            last(self.cfg)
        assert self.cfg.channel
        assert self.cfg.server
        self.channels.append(self.cfg.channel)
        self._joined.clear()
        if not ob.krn.cfg.verbose:
            launch(self.doconnect)
        self._joined.wait()

    def stop(self):
        super().stop()
        self._outqueue.put((None, None))
        if self._sock:
            try:
                self._sock.shutdown(2)
            except OSError:
                pass

    def ERROR(self, event):
        self.state.nrerror += 1
        self.state.error = event.error
        self._connected.clear()
        self.stop()
        self.start()

    def JOINED(self, event):
        self._joined.set()

    def LOG(self, event):
        pass

    def NOTICE(self, event):
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % (self.cfg.nick.upper(), self.cfg.version or 1, self.cfg.username)
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, pevent):
        if pevent.txt.startswith("DCC CHAT"):
            if not self.users.allowed(pevent.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.encoding = "utf-8"
                ob.update(dcc.cmds, self.cmds)
                launch(dcc.connect, pevent)
                return
            except ConnectionError as ex:
                return
        if pevent.txt and pevent.txt[0] == self.cc:
            if not self.users.allowed(pevent.origin, "USER"):
                return
            pevent.type = "cmd"
            pevent.txt = pevent.txt[1:]
            super().dispatch(pevent)

    def QUIT(self, event):
        if self.cfg.server in event.orig:
            self.stop()

class DCC(Bused):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""
        self.stopped = False

    def raw(self, txt):
        self._fsock.write(str(txt).rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        pass

    def connect(self, dccevent):
        if self.stopped:
            return
        dccevent.parse()
        arguments = dccevent.old.txt.split()
        addr = arguments[3]
        port = int(arguments[4])
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((addr, port))
        except ConnectionRefusedError:
            self._connected.set()
            return
        s.setblocking(1)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.raw('Welcome %s' % dccevent.origin)
        self.origin = dccevent.origin
        self._connected.set()
        launch(self.input)
        super().start()

    def input(self):
        self._connected.wait()
        super().input()

    def poll(self):
        e = Event()
        e.type = "cmd"
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        txt = self._fsock.readline()
        e.txt = txt.rstrip()
        e._sock = self._sock
        e._fsock = self._fsock
        return e

    def say(self, channel, txt):
        self.raw(txt)

class User(Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Object):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = getattr(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return find("gcd.irc.User", s)

    def get_user(self, origin):
        u = list(self.get_users(origin))
        if u:
            return u[-1][-1]

    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        user.save()
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        user.save()
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

# commands

def cfg(event):
    c = Cfg()
    last(c)
    if not event.sets:
        return event.reply(format(c, skip=["username", "realname"]))
    edit(c, event.sets)
    save(c)
    event.reply("ok")

def dlt(event):
    if not event.res.args:
        return
    selector = {"user": event.res.args[0]}
    for fn, o in find("gcd.irc.User", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def met(event):
    if not event.res.args:
        return
    user = User()
    user.user = event.res.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")
