#!/usr/bin/env python
#encoding=utf-8
import hashlib
import random
import os
import time
import json
import telnetlib
from syslog_log import _system_logs
from http_agent import  agent_list

def all_file(dir_path):
    'show file or directory in directory `argument:directory path name`'
    return  [ os.path.join(PATH,File)
              for PATH,ROOT,FILES in os.walk(dir_path)
              for File in FILES
             ]

def json_data(x,indent=4):
    'return beautiful json `[f]` `indent=4`'
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
    'curr time of 2017-12-12 12:12:!2'
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def CurrDay():
    'curr data of 2017-12-12'
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


def dir_name(x):
    "reutn directory path name `argument:directory path name`"
    if x:
        if x[-1] == '/':
            x = x[0:-1]
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


def code_try(*args,**kwargs):
    '@function if return Ture of exit `number=count,` `sleep=0` `debug=True`'
    def decorator(func):
        def wrapper(*args, **kw):
            number = kwargs['number']
            for i in range(number):
                if func(*args, **kw) is True:
                    break
                if kwargs.get('debug',True) is True:
                    print "run function:%s try:%s" % (func.func_name,i)
                time.sleep(kwargs.get('sleep',0))
            return True
        return wrapper
    return decorator

def hash_id(x=False):
    if x is False:
        x = int(time.time()*10000)
    return hashlib.sha1(str(x)).hexdigest()

def md5_id(x=False):
    if x is False:
        x = int(time.time()*10000)
    return hashlib.md5(str(x)).hexdigest()

def user_agent():
    'get user-agent'
    return random.choice(agent_list)

