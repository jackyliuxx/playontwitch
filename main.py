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

def handle_message(p, mode): 
    user = p['username']
    msg = p['message']
    msg = msg.lstrip()
    if mode == 0:
        if msg in kp.command:
            kp.press(msg, presskey_delay)
            print(user, ':', msg)
            if write_log:
                print_log(user, msg)

    elif mode == 1:
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
                return
        if kg == 0:
            return False
        for i in op:
            kp.press(i, presskey_delay)
            print(user, ':',i)
            if write_log:
                print_log(user, i)

def print_log(user, msg):
    nt = time.localtime()
    nttp = (nt.tm_year,nt.tm_mon,nt.tm_mday,nt.tm_hour,nt.tm_min,nt.tm_sec,user,msg)
    log.write('%d-%02d-%02d %02d:%02d:%02d %s : %s\n' % nttp)

def exit():
    print('')
    print('Exit!')
    sys.exit()
    if write_log:
        log.close()

# program start
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
if len(sys.argv) > 2:
    max_command = int(sys.argv[2])

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

while True:
    data = a.new_messages()
    if data == None:
        exit()
    for p in data:
        p['message']=p['message'].upper()
        handle_message(p, mode)
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        exit()

