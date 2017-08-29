#!/usr/bin/env python
#encoding=utf-8
import hashlib
import random
import os
import time
import re
import json
import telnetlib
from syslog_log import _system_logs
from http_agent import  agent_list

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
            x = json.dumps(x,indent=indent,ensure_ascii=False)
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
        msg = ''
        Open = telnetlib.Telnet()
        Open.open(kwargs['ip'],int(kwargs['port']),timeout=kwargs.get('timeout',4))
        return True,msg
    except Exception, e:
        msg = e
    return False,msg

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
            if len([ i for i in end[0].split('.') if 255 > int(i) > 0]) == 4:
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

