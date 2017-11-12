#!/usr/bin/env python
#encoding=utf-8
import psutil

def __format_int(x):
    'format k to GB'
    return round((float(x) / 1024 / 1024 / 1024),2)

def memory_info():
    t = psutil.virtual_memory()
    return {
        'total':__format_int(t.total),
        'used':__format_int(t.used),
        'free':__format_int(t.free),
        'percent':t.percent
    }


def __network(nework_name):
    return psutil.net_io_counters(pernic=True)[nework_name]

def network_send(nework_name='eth0'):
    'show network send data size,units:Mbps'
    return float(__network(nework_name).bytes_sent)/1024/1024/1024*8


def network_recv(nework_name='eth0'):
    'show network send data size,units:Mbps'
    return float(__network(nework_name).bytes_recv)/1024/1024/1024*8


def fdisk_info(fdisk_name):
    'get fdisk usage info'
    t = psutil.disk_usage(fdisk_name)
    return {
        "mountpoint": fdisk_name,
        "total": __format_int(t.total),
        "used": __format_int(t.used),
        "free": __format_int(t.free),
        "percent": t.percent,
    }

def cpu_load():
    Loadavg = {}
    with open("/proc/loadavg") as P:
        Conntent = P.read().split()
        Loadavg['lavg_1'] = Conntent[0]
        Loadavg['lavg_5'] = Conntent[1]
        Loadavg['lavg_15'] = Conntent[2]
    return Loadavg

def fdisk_all_info():
    return [fdisk_info(p.mountpoint) for p in psutil.disk_partitions()]

if __name__ == "__main__":
    print  network_send('eth0')