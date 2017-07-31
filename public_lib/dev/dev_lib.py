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

def bank_check(bank):
    'check bank number'
    digits = list(map(int, str(bank).strip()))
    j = sum(digits[-1::-2])
    o = 0
    for n in digits[-2::-2]:
        l = n * 2
        if l > 9: l = l - 9
        o += l
    return ((j + o) % 10) == 0


def card_check(card_number):
    'check card '
    id_number = str(card_number).strip()
    if 1800 < int(id_number[6:10]) < 2100:
        if int(id_number[10:12]) < 13 and int(id_number[12:14]) < 32:
            ratio = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            corres = {'0': 1, '1': 0, '2': 'x', '3': 9, '4': 8, '5': 7, '6': 6, '7': 5, '8': 4, '9': 3, '10': 2}
            j = 0
            for num, car in enumerate(list(id_number)[:-1]):
                j += int(car) * int(ratio[num])
            return str(corres[str(j % 11)]) == str(id_number.lower()[-1])
    return False


def hide_str(Str, start=2, end=3):
    'hide text'
    try:
        Number = len(Str)
        if Number > end > start:
            return Str[:start] + '*' * (end - start) + Str[end:Number]
        else:
            return Str
    except Exception, e:
        return Str


