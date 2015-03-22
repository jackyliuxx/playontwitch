import subprocess as sp
import re
import time
mp = {
        'UP' : 'Up',
        'DOWN' : 'Down',
        'LEFT' : 'Left',
        'RIGHT' : 'Right',
        'A' : 'z',
        'B' : 'x',
        'L' : 'a',
        'R' : 's',
        'SELECT' : 'c',
        'START' : 'Return'
        }

command = ['UP', 'DOWN','LEFT','RIGHT',
        'A', 'B', 'L','R',
        'SELECT', 'START']

def press(key, delay):
    sp.call('xdotool search --onlyvisible --name VBA-M key --delay %d %s' % (delay, mp[key]), shell=True)

