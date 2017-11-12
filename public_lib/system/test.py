#!/usr/bin/env python
#encoding=utf-8
import public_lib
import  public_lib.system
def system_info():
    'describe'
    return {
        "host":public_lib.host_name(),
        "version":public_lib.uname(),
        "network":public_lib.host_ip(),
        "cpu_type":public_lib.system.cpu_type(),
        "cpu_theroy_number":public_lib.system.cpu_theroy_number(),
        "cpu_truth_number":public_lib.system.cpu_truth_number(),
        "memory":public_lib.system.memory_info(),
        "fdisk":public_lib.system.fdisk_all_info(),
    }


if __name__ == "__main__":
    print public_lib.json_data(system_info())