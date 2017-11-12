#!/usr/bin/python
#coding=utf-8
import re
import traceback


def _read_file(FilePath):
    with open(FilePath) as P:
        return P.read()

def cpu_type():
    'get cpu type'
    try:
        info = set(re.findall('model name\t: (.*)',_read_file('/proc/cpuinfo')))
        if info:
            return ''.join(info)
        return 'null'
    except Exception, e:
        return e


def cpu_theroy_number():#cpu 逻辑核数
    'get cpu theroy count number'
    return len(re.findall(r'model name\t: ', _read_file('/proc/cpuinfo')))


def cpu_truth_number():#cpu 物理核数
    'get cpu truth number'
    return len(set(re.findall(r'physical id\t: (\d+)',_read_file('/proc/cpuinfo'))))

# def BaseNumber():  #序列号
#     try:
#         OrderNumber = commands.getoutput('dmidecode -t 2 | grep Serial')
#         return OrderNumber.split(':')[1].strip()
#     except Exception, e:
#         return e
#
#
# def BaseManu(): #主板制造商
#     try:
#         BaseManufacturer = commands.getoutput(\
#             "dmidecode |grep -A16 'System Information$' | egrep 'Manufacturer' | head  -1")
#         return BaseManufacturer.split(':')[1].strip()
#     except Exception, e:
#         return e
#
#
#
# def MemoryInfo():
#     try:
#         Speed = commands.getoutput("dmidecode | grep -A16 'Memory Device' | grep 'Speed'")
#         ChaCao = commands.getoutput("dmidecode | grep -P -A5 'Memory\s+Device' | grep Size | grep -v Range")
#         Step = [ Info.split(':')[1].strip() for  Info in Speed.split('\n')]
#         Groove = [ Info.split(':')[1].strip() for  Info in ChaCao.split('\n')]
#         Number = [ str(Num) for Num in range(1,len(Groove)+1)]
#         return zip(Number,Step,Groove)
#     except Exception, e:
#         return e
#
# def FdiskName():
#     try:
#         Info = commands.getoutput('lsblk')
#         Res = re.compile(r'^s')
#         ReKong = re.compile('\s+')
#         Name = []
#         for T in Info.split('\n'):
#             if re.findall(Res,T):
#                 if not 'rom' in T:
#                     Fdisk = re.sub(ReKong,' ',T).strip().split(' ')
#                     DiskName = os.path.join('/dev',Fdisk[0])
#                     # Name.append((DiskName,Fdisk[3],FdiskManu(DiskName),\
#                     #              FdiskSpeed(DiskName),FdiskNumber(DiskName)))
#                     Name.append((DiskName,Fdisk[3]))
#         return Name
#     except Exception, e:
#         return e
#
# def FdiskManu(DiskName):#硬盘厂商
#     try:
#         Info = commands.getoutput("hdparm -I %s | egrep 'Model Number'" % DiskName)
#         return Info.split(':')[1].strip()
#     except Exception, e:
#         return e
#
# def FdiskSpeed(DiskName):#硬盘转速
#     try:
#         Info = commands.getoutput("hdparm -I %s | egrep 'Nominal Media Rotation Rate'" % DiskName)
#         return Info.split(':')[1].strip()
#     except Exception, e:
#         return e
#
# def FdiskNumber(DiskName):#序列号
#     try:
#         Info = commands.getoutput("hdparm -I %s | egrep 'Serial Number'" % DiskName)
#         return Info.split(':')[1].strip()
#     except Exception, e:
#         return e