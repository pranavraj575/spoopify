from threading import Thread
from time import sleep as naptime, time as tim
from collections import defaultdict
import sys, os

DIR = os.path.abspath(sys.argv[0])
DIR = DIR[:DIR.rindex(os.sep) + 1]

try:
    import pwr
except:
    pass

try:
    import win32gui as wins
except:
    print("hacking")
    os.system("pip install pywin32")
    os.system("pip3 install pywin32")
    print("we're in\n")
    os.system("python " + DIR + "horsefingers.py")
    quit(69)
try:
    from pycaw.pycaw import AudioUtilities as peepee, ISimpleAudioVolume as mandm
except:
    print("hacking 2: electric boogaloo")
    os.system("pip install pycaw")
    os.system("pip3 install pycaw")
    print("we're in\n")
    os.system("python " + DIR + "horsefingers.py")
    quit(420)

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
    def __init__(self, win: window, basetime=.3, lowbutt=42.0, facto=1/.69, winfact=4.20, max_butt_factor=10):
        self.win = win
        self.stor = win.storage
        self.basetim = basetime
        self.lowbutt = lowbutt
        self.facto = facto
        self.winfact = winfact
        self.mbf = max_butt_factor
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
                    self.tim *= self.lowbutt/(pwr.battry() - 1 + self.lowbutt/self.mbf)
        except:
            pass
        self.wintime = self.winfact*self.tim

    def __str__(self):
        return 'base: ' + str(self.basetim) + '\n' + 'delay: ' + str(self.tim) + '\n' + 'window time: ' + str(
            self.wintime)

reckey=DIR + "reccy.txt"
def record(reccy,clout):
    pee=list(reccy)
    pee.sort(key=lambda arr:reccy[arr],reverse=True)
    snake=''
    for thing in pee:
        snake+=thing+"\t"+str(reccy[thing])+"\n"
    clout(snake)
reccy = defaultdict(lambda: 0)
try:
    reccy.update({thingy.split("\t")[0]: float(thingy.split("\t")[1]) for thingy in
                  open(reckey, "r").read().strip().split("\n")})
except:
    pass

go = True
def end():
    global go
    global reccy
    while go:
        penis=input().lower()
        if penis == ":q":
            sonic_smut.end()
            go = False
        if penis == "h":
            record(reccy,lambda snake:print(snake.replace("\t",":\t")))



print("enter :q to quit")
enderman = Thread(target=end, daemon=True)
enderman.start()
x = storage()
sonic_smut = sound()
sonic_smut.here()

pp = window(x)
hot = timing(pp)
hot.start()
current = ''
stim = tim()
while go:
    while not pp.exists() and go:
        naptime(hot.wintime)
        current=''
    readout = ''
    changed = False
    if pp.text() != current:
        if current:
            reccy[current]+=tim()-stim
            record(reccy,lambda snake:open(reckey,"w").write(snake))
        stim = tim()
        current = pp.text()
        readout = current + '\n'
        changed = True
    if x.isAd(current):
        if changed: readout = 'MUTED: ' + readout
        sonic_smut.deaf()
    else:
        sonic_smut.here()
    print(readout, end='')
    naptime(hot.tim)
