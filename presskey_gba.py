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

mpk = ['UP', 'DOWN','LEFT','RIGHT',
        'A', 'B', 'L','R',
        'SELECT', 'START']

def _press(username, key):
    print(username, ':', key)
    sp.call('xdotool search --onlyvisible --name VBA-M key --delay 200 %s' % mp[key], shell=True)
    # time.sleep(0.1)

def press(p, mode):
    username = p['username']
    msg = p['message']
    msg = msg.lstrip()
    if mode == 0:
        if msg in mpk:
            _press(username, msg)
            return True
        else:
            return False
    elif mode == 1:
        op = []
        kg = 1
        while len(msg) and kg:
            kg = 0
            for i in mpk:
                if len(i) > len(msg):
                    continue
                if i == msg[:len(i)]:
                    op.append(i)
                    msg = msg[len(i):].lstrip()
                    kg = 1
                    break
            if len(op)>6:
                return False
        if kg == 0:
            return False
        for i in op:
            _press(username, i)
        return True
