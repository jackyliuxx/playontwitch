import connect_to_twitch as ctt
import sys
import presskey_gba as kp
import time
import os
import config

def open_log_file():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    ndt = time.localtime()
    ndttp = (ndt.tm_year,ndt.tm_mon,ndt.tm_mday,ndt.tm_hour,ndt.tm_min,ndt.tm_sec)
    return open('logs/%d-%02d-%02d %02d:%02d:%02d.log' % ndttp , 'w')

def command_list(msg):
    op = []
    kg = 1
    while len(msg) and kg:
        kg = 0
        for i in kp.command:
            if len(i) > len(msg):
                continue
            if i == msg[:len(i)]:
                op.append(i)
                msg = msg[len(i):].lstrip()
                kg = 1
                break
        if len(op) > max_command:
            kg = 0
    if kg == 0:
        return []
    return op

def handle_message(msg, mode): 
    msg = msg.lstrip()
    if mode == 0:
        if msg in kp.command:
            return [msg]
    elif mode > 0:
        op = command_list(msg)
        for i in op:
            kp.press(i, presskey_delay)
            print(user, ':',i)
            print_log(user, i)

def print_log(user, msg):
    if not write_log:
        return
    nt = time.localtime()
    nttp = (nt.tm_year,nt.tm_mon,nt.tm_mday,nt.tm_hour,nt.tm_min,nt.tm_sec,user,msg)
    log.write('%d-%02d-%02d %02d:%02d:%02d %s : %s\n' % nttp)

def exit():
    print('')
    print('Exit!')
    if write_log:
        log.close()
    sys.exit()

# program start
if hasattr(config, 'username') and config.username:
    username = config.username
else:
    username = input('Enter your twitch username :')

if hasattr(config, 'key') and config.key and config.key != 'oauth:':
    key = config.key
else:
    key = 'oauth:' + input('Enter your twitch oauth token : oauth:')

if hasattr(config, 'channal') and config.channal:
    channal = config.channal
else:
    channal = input('Enter the channal you want to join :')

if hasattr(config, 'mode') and config.mode:
    mode = config.mode
else:
    mode = 0

if hasattr(config, 'write_log') and config.write_log:
    write_log = 1
else:
    write_log = 0

if hasattr(config, 'max_command'):
    max_command = config.max_command
else:
    max_command = 10

if hasattr(config, 'presskey_delay'):
    presskey_delay = config.presskey_delay
else:
    presskey_delay = 200

if hasattr(config, 'interval_time'):
    interval_time = config.interval_time
else:
    interval_time = 10

if len(sys.argv) > 1:
    mode = int(sys.argv[1])
if len(sys.argv) > 2:
    max_command = int(sys.argv[2])

if mode == 3:
    max_command = 99999999

if write_log:
    log = open_log_file()

a = ctt.user()
if not a.connect(username, key):
    print_log('********', 'Fail to connect to twitch.  %s  %s' % (username, key))
    exit()
else:
    print_log('********', 'Succeed to connect to twitch.  %s  %s' % (username, key))

if not a.join(channal):
    print_log('********', 'Fail to join #%s.' % channal)
    exit()
else:
    print_log('********', 'Succeed to join #%s.' % channal)

print_log('********', 'mode %d' % mode)

while True:
    if mode > 1:
        try:
            time.sleep(interval_time)
        except KeyboardInterrupt:
            exit()
    data = a.new_messages()
    for p in data:
        p['message'] = p['message'].upper()
    if data == None:
        exit()
    if mode == 0:
        for p in data:
            msg = p['message']
            user = p['username']
            msg = msg.strip()
            if msg in kp.command:
                kp.press(msg, presskey_delay)
                print(user, ':', msg)
                print_log(user, msg)

    elif mode == 1:
        for p in data:
            msg = p['message']
            user = p['username']
            op = command_list(msg)
            for i in op:
                kp.press(i, presskey_delay)
                print(user, ':', i)
                print_log(user, i)
    elif mode == 2:
        command_map = {}
        for p in data:
            msg = p['message']
            user = p['username']
            op = command_list(msg)
            if op != []:
                op = tuple(op)
                if op in command_map:
                    command_map[op]+=1
                else:
                    command_map[op]=1
        mx = 0
        op = ()
        for p in command_map:
            if command_map[p] > mx:
                mx = command_map[p]
                op = p
        for i in op:
            kp.press(i, presskey_delay)
            print('democracy', ':', i)
            print_log('democracy', i)
    elif mode == 3:
        fp = ['',[]]
        for p in data:
            msg = p['message']
            user = p['username']
            op = command_list(msg)
            if len(op) > len(fp[1]):
                fp[0] = user
                fp[1] = op
        for i in fp[1]:
            kp.press(i, presskey_delay)
            print(fp[0], ':', i)
            print_log(fp[0], i)

