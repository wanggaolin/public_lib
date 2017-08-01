#!/usr/bin/env python
#encoding=utf-8
import psutil

def __memroy():
    return psutil.virtual_memory()

def __format_int(x):
    'format k to GB'
    return float("%0.2f" % (float(x) / 1024 / 1024 / 1024))

def __fdisk(fdisk_name):
    return psutil.disk_usage(fdisk_name)

def memroy_free():
    'show free memory,units:MB'
    return  __format_int(__memroy().free)

def memroy_total():
    'show memory total,units:GB'
    return  __format_int(__memroy().total)

def fdisk_total(disk_name='/'):
    'show fdisk size,units:GB'
    return __format_int(__fdisk(disk_name).total)

def fdisk_free(disk_name='/'):
    'show fdisk free size,units:GB'
    return __format_int(__fdisk(disk_name).free)

def __network(nework_name):
    return psutil.net_io_counters(pernic=True)[nework_name]

def network_send(nework_name='eth0'):
    'show network send data size,units:GB'
    return __format_int(float(__network(nework_name).bytes_sent) / 8 / 1024)

def network_recv(nework_name='eth0'):
    'show network send data size,units:GB'
    return __format_int(float(__network(nework_name).bytes_recv) / 8 / 1024)

if __name__ == "__main__":
    print network_recv()
