import uinput
d = uinput.Device([
    uinput.KEY_Z,
    uinput.KEY_X,
    uinput.KEY_A,
    uinput.KEY_S,
    uinput.KEY_C,
    uinput.KEY_ENTER,
    uinput.KEY_UP,
    uinput.KEY_DOWN,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT
    ])

mp = {
        'A' : uinput.KEY_Z,
        'B' : uinput.KEY_X,
        'L' : uinput.KEY_A,
        'R' : uinput.KEY_S,
        'UP' : uinput.KEY_C,
        'DOWN' : uinput.KEY_DOWN,
        'LEFT' : uinput.KEY_LEFT,
        'RIGHT' : uinput.KEY_RIGHT,
        'SELECT' : uinput.KEY_C,
        'START' : uinput.KEY_ENTER
        }

def press(msg):
    if msg in mp:
        d.emit_click(mp[msg])
        return True
    else:
        return False
