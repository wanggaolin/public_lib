#!/usr/bin/env python
#encoding=utf-8
import os
import time
import json
import telnetlib

def all_file(dir_path):
    'show file or directory in directory'
    return  [ os.path.join(PATH,File)
              for PATH,ROOT,FILES in os.walk(dir_path)
              for File in FILES
             ]

def json_data(x,indent=4):
    'return beautiful json'
    if x:
        try:
            if type(x) is str:
                x = json.loads(x)
            x = json.dumps(x,indent=indent,ensure_ascii=False)
        except Exception,e:
            pass
    return x

def CurrTime():
    'curr time of 2017-12-12 12:12:!2'
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def CurrDay():
    'curr data of 2017-12-12'
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


def dir_name(x):
    "reutn directory path name"
    if x:
        if x[-1] == '/':
            x = x[0:-1]
    return x

def telent(*args,**kwargs):
    "telet ip:port"
    try:
        msg = ''
        Open = telnetlib.Telnet()
        Open.open(kwargs['ip'],int(kwargs['port']),timeout=kwargs.get('timeout',4))
        return True,msg
    except Exception, e:
        msg = e
    return False,msg
