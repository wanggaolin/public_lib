#!/usr/bin/env python
#encoding=utf-8
import hashlib
import random
import os
import time
import re
import json
import socket
import commands
import telnetlib
import commands
import hashlib
from syslog_log import _system_logs
from http_agent import  agent_list
from collections import namedtuple
from termin import Terminal

def _read(file_path):
    """
    :param file_path:file path
    :return: file path conntext
    """
    with open(file_path,r'rb') as P:
        return P.read()

def code_try(*args,**kwargs):
    """
    '@function if return Ture of exit `number=count,` `sleep=0` `debug=True`'
    :param kwargs:
        :number: try count
        :sleep:  run code interval
        :debug:  debug info
    :return:True
    """
    def decorator(func):
        def wrapper(*args, **kw):
            number = kwargs['number']
            for i in range(number):
                end = func(*args, **kw)
                if end:
                    return end
                if kwargs.get('debug',True) is True:
                    print "run function:%s try:%s" % (func.func_name,i)
                time.sleep(kwargs.get('sleep',0))
            return False
        return wrapper
    return decorator


def all_file(dir_path):
    """
    :param dir_path: directory name
    :return:[]
    """

    return  [ os.path.join(PATH,File)
              for PATH,ROOT,FILES in os.walk(dir_path)
              for File in FILES
             ]

def json_data(x,indent=4):
    """
    :param x: json dump of data
    :param indent:indent default is 4
    :return: str
    """
    if x:
        try:
            if type(x) is str:
                x = json.loads(x)
            x = json.dumps(x, indent=indent, ensure_ascii=False)
        except Exception,e:
            _system_logs("jsondata error, data:%s error:%s" % x,e)
            pass
    return x

def CurrTime():
    """
    :return: 2017-12-12 12:12:12
    """
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def CurrDay():
    """
    :return: 2017-12-12
    """
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


def dir_name(x):
    """
    :param x: directory path name
    :return: /a/b
    """
    if x:
        if x[-1] == '/':
            x = x[0:-1]
    return x

def file_name(x):
    """
    :param x: file path name
    :return: /a/b
    """
    if x:
        x = dir_name(x)
        if x[0] == '/':
            x = str(x[1:]).replace('\\','/')
    return x

def telnet(*args,**kwargs):
    "telnet ip:port"
    try:
        status,msg = False,''
        Open = telnetlib.Telnet()
        Open.open(kwargs['ip'],int(kwargs['port']),timeout=kwargs.get('timeout',4))
        status = True
    except Exception, e:
        msg = e
    F = namedtuple('telnet', ['status', "msg"])
    return F(status,msg)

def hide_str(Str, start=2, end=3):
    'hide text `str  start=2 end=3`'
    try:
        Number = len(Str)
        if Number > end > start:
            return Str[:start] + '*' * (end - start) + Str[end:Number]
        else:
            return Str
    except Exception, e:
        return Str

def hash_id(x=False):
    if x is False:
        x = int(time.time()*100000000)
    return hashlib.sha1(str(x)).hexdigest()

def md5_id(x=False):
    if x is False:
        x = int(time.time()*100000000)
    return hashlib.md5(str(x)).hexdigest()

def user_agent():
    'get user-agent'
    return random.choice(agent_list)

def list_cut(List,Number=4):
    """
    with number cut list
    :param List: cut data
    :param Number: every list count
    :return: []
    """
    Count = 0
    Info = []
    for Num in range(len(List)):
        End = List[Count:Number + Count]
        Count  = Number + Count
        if End:
            Info.append(End)
    return Info

def check_ip(ip=None):
    """
    check ip format
    :param ip:ip format is xxx.xxx.xxx.xxx
    :return:bool
    """
    if ip:
        end = re.findall(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ip)
        if end:
            a,b,c,d = map(int,end[0].split('.'))
            if 0 < a < 255 and b < 255 and c < 255 and 0 < d < 255:
                return True
    return False


def check_ip_private(ip=None):
    """
    check ip is private
    :param ip:ip format is xxx.xxx.xxx.xxx
    :return:bool
    """
    if check_ip(ip):
        end = re.findall(r'^10\.|^172\.16\.|^192\.168\.', ip)
        if end:
            return True
    return False

def uname():
    'get system uname'
    return re.split(r'\n|\\n',_read('/etc/issue'))[0].strip()

def ping(ip=False,interval=1,count=3,debug=False):
    """
    :param ip:ping destination
    :param interval:send package interval
    :param count:send package count
    :param debug:False
    :return:
    """
    Shell = "ping -c {count} -i {interval} {ip}".format(count=count,interval=interval,ip=ip)
    ShellEnd = commands.getoutput(Shell)
    status = False
    min = avg = max = mdev = text = lost = ''
    F = namedtuple('ping', ['status', 'min', 'avg', 'max', 'mdev', 'lost','text'])
    re_end = re.findall('min/avg/max/mdev = (.*) ms', ShellEnd)
    if re_end:
        lost = re.findall(r'(\d+%) packet loss',ShellEnd)[0]
        End = re_end[0].split('/')
        status = True
        End.insert(0,status)
    else:
        End = [min,avg,max,mdev,status]
    if debug:
        text = ShellEnd
    End.append(lost)
    End.append(text)
    return F._make(End)

def terminal_size():
    "get terminal size"
    F = namedtuple('terminal_size', ['width', "height"])
    t = Terminal()
    return F._make([t.width,t.height])

def file_md5(file=''):
    "show file hash md5s"
    try:
        with open(file, r"rb") as P:
            return hashlib.md5(P.read()).hexdigest()
    except (OSError,IOError),e:
        pass
    return False

def file_diff(file1='',file2=''):
    """
    diff two file is identical
    :param file1: file path
    :param file2: file path
    :return: True or Flase
    """
    try:
        if os.path.getsize(file1) == os.path.getsize(file2):
            with open(file1, r"rb") as P1:
                with open(file2, r"rb") as P2:
                    while 1:
                        text1 = P1.read(1024*1000)
                        text2 = P2.read(1024*1000)
                        if text1 and text2:
                            if hashlib.md5(text1).hexdigest() != hashlib.md5(text2).hexdigest():
                                return False
                        else:
                            return True
    except (OSError,IOError),e:
        pass
    return False


class _file_copy:
    def __init__(self,file1='',file2=''):
        self.file1 = file1
        self.file2 = file2
        self.msg = [False,'']

    def _copy(self,des1,des2):
        try:
            with open(des1, r"rb") as P1:
                with open(des2, r"w+") as P2:
                    while 1:
                        text = P1.read(1024*1024)
                        if text:
                            P2.write(text)
                        else:
                            self.msg[0] = True
                            return True
        except Exception, e:
            self.msg[1] = e
        return False

    def copy_file(self):
        self._copy(self.file1,self.file2)
        return self.msg

    def copy_dir(self):
        try:
            for PATH, ROOT, FILES in os.walk(self.file1):
                os.makedirs(PATH.replace(self.file1,self.file2,1))
                for File in FILES:
                    i =  os.path.join(PATH,File)
                    if self._copy(des1=i,des2=i.replace(self.file1,self.file2,1)) is False:
                        return self.msg
        except Exception, e:
            self.msg[1] = e
        return self.msg

def file_copy(file1='',file2=''):
    """
    copy file1 to file2
    :param file1: file path
    :param file2: file path
    :return:tuple
    """
    F = namedtuple('copy', ['status', 'source', 'destination', 'msg'])
    file1 =  dir_name(file1)
    file2 =  dir_name(file2)
    if os.path.exists(file1):
        if os.path.isfile(file1):
            end = _file_copy(file1=file1,file2=file2).copy_file()
        else:
            end = _file_copy(file1=file1,file2=file2).copy_dir()
        return F._make([end[0], file1, file2, end[1]])
    else:
        return F._make([False, file1, file2, '%s: No such file or directory' % file1])

def host_name():
    'get system name'
    return socket.gethostname()

def host_ip():
    'get system ip'
    return [ {i[0]:[i[2],i[1]]}
       for i in  (re.findall(r'\d: (\w+): <.*\n\s+link/ether (\S+) brd \S+\n\s+inet (\S+)/\d+ brd \S+ ',commands.getoutput("ip addr")))
    ]

def set_list(data=[]):
    'get repeat index'
    x = []
    for i in set(data):
        if data.count(i) > 1:
            x.append(i)
    return x