import socket
import sys
import re
class user:
    
    def connect(self, username, key):
        self.username = username
        self.key = key
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        host = 'irc.twitch.tv'
        port = 6667
        print('Connecting to twitch...')
        try:
            s.connect((host, port))
        except:
            print('Fail to connect to twitch!!')
            return False
        s.sendall(str.encode('PASS %s\r\n' % key))
        s.sendall(str.encode('NICK %s\r\n' % username))
        data = bytes.decode(s.recv(1024))
        if data == ':tmi.twitch.tv NOTICE * :Login unsuccessful\r\n':
            print('Wrong username or key!!')
            return False
        print('Success!!')
        self.s = s
        return True
    
    def join(self, channal):
        s = self.s
        s.sendall(str.encode('JOIN #%s\r\n' % channal))
        try:
            data = bytes.decode(self.s.recv(1024))
        except:
            print('Fail to join %s!!' % channal)
            return False
        print('Join to %s!!' % channal)
        return True

    def parse_message(self, msg):
        r = re.search(':(\w+)![a-zA-Z0-9_@\.]+ PRIVMSG #(\w+) :(.+)', msg)
        if not r:
            return r
        return {'username' : r.group(1), 'channal' : r.group(2), 'message' : r.group(3)}

    def new_messages(self):
        s = self.s
        try:
            data = bytes.decode(s.recv(1024))
        except:
            return []
        rt = []
        for msg in data.split('\r\n'):
            p_msg = self.parse_message(msg)
            if p_msg:
                rt.append(p_msg)
        return rt
