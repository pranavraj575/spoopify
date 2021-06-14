from threading import Thread
from time import sleep as naptime
try:
    import pwr
except:
    pass
import win32gui as wins
from pycaw.pycaw import AudioUtilities as peepee, ISimpleAudioVolume as mandm
import sys

class sound:
    def __init__(self, name='Spotify.exe'):
        self.name = name
        self.ent = False

    def _dd(self, vv):
        if not self.ent:
            for s in peepee.GetAllSessions():
                if s.Process and s.Process.name() == self.name:
                    while s._ctl.QueryInterface(mandm).GetMasterVolume() != vv:
                        s._ctl.QueryInterface(mandm).SetMasterVolume(vv, None)
                    assert s._ctl.QueryInterface(mandm).GetMasterVolume() == vv

    def here(self):
        self._dd(1)

    def deaf(self):
        self._dd(0)

    def end(self):
        self.here()
        self.ent = True

DIR = sys.argv[0].replace('\\', '/')
DIR = DIR[:DIR.rfind('/') + 1]

class storage:
    def __init__(self, wl='whitelist.txt', bl='blacklist.txt', gb='goodBoy.txt', cc='cancer.txt',
                 dir=DIR):
        self.wl = dir + wl
        self.bl = dir + bl
        self.gb = dir + gb
        self.cc = dir + cc
        self.resetLists()

    def resetLists(self):
        self.whiteList = self._getOrMake(self.wl, set())
        self.blackList = self._getOrMake(self.bl, {'Spotify', 'Advertisement', 'Spotify Free'})
        self.goodBoy = self._getOrMake(self.gb, {'Recorded at Spotify Studios'})
        self.blocked = self._getOrMake(self.cc, {'Spotify'})
        self.allKnown = self.whiteList | self.blackList

    def _getOrMake(self, ff, ll):
        try:
            for it in self._listt(ff):
                if it not in ll:
                    ll.add(it)
        except:
            pass
        return ll

    def _listt(self, free):
        poop = open(free, 'r')
        dd = set(poop.read().strip().split('\n'))
        poop.close()
        return dd

    def _record(self, free, graceful):
        graceful = list(graceful)
        graceful.sort(key=str.lower)
        pp = open(free, 'w')
        for thing in graceful:
            pp.write(thing + '\n')
        pp.close()

    def isAd(self, t):
        blocc = False
        for thing in self.blocked:
            if thing in t:
                blocc = True
        good = False
        for thing in self.goodBoy:
            if thing in t:
                good = True
        return (' - ' not in t and t not in self.whiteList) or (
                not t in self.whiteList and (t in self.blackList or (not good and blocc)))

class window:
    def __init__(self, storage):
        self.n = None
        self.storage = storage
        self.find()

    def _allOpen(self):
        def c(a, b):
            if wins.IsWindowVisible(a) and wins.GetWindowText(a):
                pp.append(a)

        pp = []
        wins.EnumWindows(c, None)
        return pp

    def find(self):
        for x in self._allOpen():
            if wins.GetWindowText(x) in self.storage.allKnown:
                self.n = x
                return True
        self.n = None
        return False

    def exists(self):
        try:
            return bool(wins.GetWindowText(self.n))
        except:
            return False

    def text(self):
        return wins.GetWindowText(self.n)

    def __str__(self):
        return str(self.n)

class timing:
    def __init__(self, win: window, basetime=.3, lowbutt=50, facto=2, winfact=10):
        self.win = win
        self.stor = win.storage
        self.basetim = basetime
        self.lowbutt = lowbutt
        self.facto = facto
        self.winfact = winfact
        self._setDelays()
        self.thing = Thread(target=self.Handler, daemon=True)

    def start(self):
        self.thing.start()

    def Handler(self):
        global go
        while go:
            if not self.win.exists():
                self.win.find()
            self._setDelays()
            naptime(self.wintime)
            self.stor.resetLists()

    def _setDelays(self):
        self.tim = self.basetim
        try:
            if not pwr.charging():
                self.tim *= self.facto
                if pwr.battry() < self.lowbutt:
                    self.tim *= self.lowbutt / pwr.battry()
        except:
            pass
        self.wintime = self.winfact * self.tim

go = True

def end():
    global go
    while go:
        if input() == ":q":
            sonic.end()
            go = False

print("enter :q to quit")
ender = Thread(target=end, daemon=False)
ender.start()
x = storage()
sonic = sound()
sonic.here()
pp = window(x)
hot = timing(pp)
hot.start()
current = ''
while go:
    while not pp.exists() and go:
        naptime(hot.wintime)
    readout = ''
    changed = False
    if pp.text() != current:
        current = pp.text()
        readout = current + '\n'
        changed = True
    if x.isAd(current):
        if changed: readout = 'MUTED: ' + readout
        sonic.deaf()
    else:
        sonic.here()
    print(readout, end='')
    naptime(hot.tim)