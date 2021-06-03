#!/usr/bin/env python
#encoding=utf-8
import hashlib
import traceback
import random
import copy
import fcntl
import struct
import os
import time
import re
import json
import socket
import telnetlib
import commands
import hashlib
from syslog_log import _system_logs
from http_agent import  agent_list
from collections import namedtuple
from error_msg import RaiseVlues
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
            error_message = ""
            for i in range(number):
                try:
                    end = func(*args, **kw)
                    if end:
                        return end
                except Exception,e:
                    error_message = str(traceback.format_exc())
                if kwargs.get('debug',True) is True:
                    print "run function:%s try:%s error:%s" % (func.func_name,i,error_message)
                time.sleep(kwargs.get('sleep',0))
            return False
        return wrapper
    return decorator

def code_try_def(*args,**kwargs):
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
            error_message = ""
            error_str = ""
            end = {}
            for i in range(number):
                try:
                    end = func(*args, **kw)
                    if end["status"] is True:
                        return end
                except Exception,e:
                    error_str = str(e)
                    error_message = str(traceback.format_exc())
                if kwargs.get('debug',False) is True:
                    print "run function:%s try:%s error:%s" % (func.func_name,i,error_message)
                time.sleep(kwargs.get('sleep',0))
            end["error"] = error_message
            end["error_short"] = error_str
            return end
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
            _system_logs().error("jsondata error, data:%s error:%s" % (x,e))
            pass
    return x

def CurrTime():
    """
    :return: 2017-12-12 12:12:12
    """
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def CurrTime1():
    """
    :return: 2017-12-12 12:12
    """
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

def CurrDay():
    """
    :return: 2017-12-12
    """
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))



#unix时间转北京时间
def time_to_utf8(t):
    return time.strftime('%Y-%m-%d %H:%M', (time.localtime(t)))

def time_to_utf81(t):
    return time.strftime('%m-%d %H:%M', (time.localtime(t)))


def time_unix_format_bj(t):
    """
    :param t: 2021-06-03 17:08
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', (time.localtime(t)))

def time_bj_foramt_unix1(t):
    """
    :param t: 1622711491
    :return:
    """
    return time.mktime((datetime.datetime.strptime(t,"%Y-%m-%d %H:%M")).timetuple())

def time_bj_foramt_unix2(t):
    """
    :param t: 1622711491
    :return:
    """
    return time.mktime((datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S")).timetuple())

# 北京时间转unix时间
def time_bj_foramt_unix3(t):
    """
    :param t: 1622711491
    :return:
    """
    return time.mktime((datetime.datetime.strptime(t,"%Y-%m-%d")).timetuple())

def time_utc_format_bj1(t):
    bj_time = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M', t.timetuple()), '%Y-%m-%d %H:%M') + datetime.timedelta(hours=8)
    return bj_time.strftime("%Y-%m-%d %H:%M")

def time_utc_format_bj2(t):
    """
    :param t: 2017-04-13T20:09:33Z
    :return:
    """
    bj_time = datetime.datetime.strptime(time.strftime('%Y-%m-%d', t.timetuple()), '%Y-%m-%d') + datetime.timedelta(hours=8)
    return bj_time.strftime("%Y-%m-%d")


def dir_name(x):
    """
    :param x: directory path name
    :return: /a/b
    """
    if x:
        x = re.sub(r'/+$', "", str(x))
    return x

def file_name(x):
    """
    :param x: file path name
    :return: /a/b
    """
    if x:
        x = dir_name(x=re.sub(r'^/+',"",str(x)))
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
            if 0 < a <= 255 and b <= 255 and c <= 255 and 0 < d <= 255:
                return True
    return False


def check_ip_private(ip=None):
    """
    check ip is private
    :param ip:ip format is xxx.xxx.xxx.xxx
    :return:bool
    """
    if check_ip(ip):
        end = re.search(r'^10\.|^172\.16\.|^192\.168\.|^127\.0', ip)
        if end:
            return True
        elif 16 < int(ip.split(".")[1]) < 32 and re.search(r'^172\.',ip):
            return True
    return False

def check_ip_full_private(ip=None):
    """
    check ip is private
    :param ip:ip format is xxx.xxx.xxx.xxx/x.x.x.x
    :return:bool
    """
    if re.search(r'^\d+\.\d+\.\d+\.\d+\/\d+\.\d+\.\d+\.\d+$',ip):
        ip_name = str(ip).split("/")
        if check_ip_private(ip_name[0]):
            end = re.search(r'^\d+\.\d+\.\d+\.\d+$', ip_name[-1])
            if end:
                ip_mask = map(int,ip_name[-1].split("."))
                if max(ip_mask) <= 255 and min(ip_mask) >= 0:
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
    ip_command = "ip"
    if os.path.exists("/sbin/ip"):
        ip_command = "/sbin/ip"
    elif os.path.exists("/usr/sbin/ip"):
        ip_command = "/usr/sbin/ip"
    return [ {i[0]:[i[2],i[1]]}
       for i in  (re.findall(r'\d: (\w+): <.*\n\s+link/ether (\S+) brd \S+\n\s+inet (\S+)/\d+ \S+ ',commands.getoutput(ip_command + " addr")))
    ]

def set_list(data=[]):
    'get repeat index'
    x = []
    for i in set(data):
        if data.count(i) > 1:
            x.append(i)
    return x

def network_mac(interface):
    """
    with ipaddres get mac
    :param interface:
    :return:
    """
    DEVICE_NAME_LEN = 15
    MAC_START = 18
    MAC_END = 24
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,
                       struct.pack('256s', interface[:DEVICE_NAME_LEN]))
    return ''.join(['%02x:' % ord(char)
                    for char in info[MAC_START:MAC_END]])[:-1]


def set_dict(**kwargs):
    """
    set dict
    :param kwargs:
        :data: data dict
        :key:set key list
    :return: {}
    """
    new_dict = {}
    data = kwargs['data']
    _key = kwargs['key']
    for i in data.keys():
        if i in _key:
            continue
        new_dict[i]=data[i]
    return new_dict

def cache_file(*arg,**kwa):
    """
    cache data to file
    :param kwargs:
        :time: cache data time,unit:second
        :file: save data of file path
        :actuall_file: save data of file path
    :return: str
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_time = kwa['time']
            file_path = kwa.get('file', False)
            if not file_path:
                if kwargs.get('actuall_file',False) is False:
                    raise RaiseVlues('file_path not must be null')
                else:
                    file_path = kwargs['actuall_file']
            if os.path.exists(file_path):
                if (time.time() - os.stat(file_path).st_mtime) < cache_time:
                    with open(file_path) as P:
                        try:
                            return json.loads(P.read())
                        except ValueError, e:
                            pass
            file_lock = open(file_path + '_lock', "w+")
            fcntl.flock(file_lock.fileno(), fcntl.LOCK_EX)
            data = func(*args, **kwargs)
            with open(file_path, r'w+') as P:
                P.write(json.dumps(data))
            file_lock.close()
            return data
        return wrapper
    return decorator

class cache:
    def __init__(self,**kwargs):
        self.file_path = kwargs.get("file","/tmp/."+str(int(time.time()*10000)))
        self.file_lock = self.file_path+'.lock'

    @code_try(number=3,sleep=1,debug=False)
    def _save(self,data,type=None):
        file_lock = open(self.file_lock + '_lock', "w+")
        fcntl.flock(file_lock.fileno(), fcntl.LOCK_EX)
        with open(self.file_path, r'w+') as P:
            P.write(json.dumps({"data":data,"time":CurrTime()}))
        file_lock.close()
        return True

    def save(self,data,type=None):
        return self._save(data,type=None)

    def get(self,data_value=False):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path) as P:
                    return json.loads(P.read())["data"]
        except ValueError,e:
            pass
        return data_value



def locks(*arg,**kwa):
    """
    cache data to file
    :param kwargs:
        :file: lock file path
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            file_path = kwa['lock']
            file_lock = open(file_path + '.lock', "a+")
            fcntl.flock(file_lock.fileno(), fcntl.LOCK_EX)
            data = func(*args, **kwargs)
            file_lock.close()
            return data
        return wrapper
    return decorator


def text_column(**kwargs):
    """
    Format column alignment
    :param kwargs:
        data:[
            [x,x,x,x],
            [x1,x1,x1,x1],
        ]
    :return: text
    """
    defloumn = kwargs.get("size",2)
    data = kwargs["data"]
    s = max([ len(_a) for _a in data ])
    for _num,_num_data in enumerate(data):
        if len(_num_data) < s:
            _num_data.extend([ "" for _n in range(s-len(_num_data)) ])

    max_size = {}
    for _col,_col_data in enumerate(map(list,zip(*data))):
        max_size[str(_col)] = max([ len(_l) for _l in _col_data ])+defloumn

    p = []
    for i in data:
        txt = []
        for _s1,_s2 in enumerate(i):
            txt.append( _s2.ljust(max_size[str(_s1)]))
        p.append("".join(txt))
    return "\n".join(p)


def ip_format_int( x):
    if x == 'localhost':
        return 11
    else:
        return int(socket.ntohl(struct.unpack("I", socket.inet_aton(x))[0]))

def ip_format_str(dec_value):
    ip = ''
    t = 2 ** 8
    dec_value = int(dec_value)
    for _ in range(4):
        v = dec_value % t
        ip = '.' + str(v) + ip
        dec_value = dec_value // t
    ip = ip[1:]
    return ip


def process_lock(*args,**kwargs):
    def decorator(func):
        def wrapper(*args, **kw):
            try:
                file_lock = open(kwargs["pid"] + '.lock', "a+")
                fcntl.flock(file_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return func(*args, **kw)
            except Exception,e:
                if re.search("Resource temporarily unavailable",str(traceback.format_exc())):
                    if kwargs.get("alert"):
                        raise public_lib.RaiseVlues("The process is already running")
                    exit()
                Loging().error(traceback.format_exc())
            return False
        return wrapper
    return decorator

def netowkr_mask_int(x):
    return sum( [bin(int(i)).count('1') for i in x.split('.')])


if __name__ == "__main__":
    text_column(data=[
        ["a","b","c11111111122","d","e","1","水电费"],
        ["a123123","b1","c","11","e","f21"],
        ["a5","b","csdfsdf","d22","e","f"],
        ["a57","b12","c","d","e","f123123"],
        ["a5","b23","c","d","e25","f123123"],
    ])
    """
    [
        [1,2,3],
        [11,22,33],
    ]   
        
    [
        [1,11],
        [2,22],
        [3,33],
    ]
    """
    print(ip_hide_str(3232235777))
    # print check_ip_full_private("192.168.1.1/255.255.255.256")
