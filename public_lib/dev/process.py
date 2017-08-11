#!/usr/bin/env python
#encoding=utf-8
import re
import commands
from collections import namedtuple

class _pid(object):
    def __init__(self,command_name):
        self.name = command_name

    def _show_pid(self):
        'return command of pid'
        AllPid = []
        Re = re.compile(r'\s+')
        for Info in commands.getoutput("ps -ef | egrep %s | grep -v 'grep'" % self.name).split('\n'):
            Info = re.sub(Re, ' ', Info).strip()
            if Info:
                Info = Info.split(' ')[1]
                AllPid.append(Info)
        return AllPid

    def _usage_memory(self,all_pid):
        re_f = re.compile(r'VmRSS:\s+(\d+)\s+')
        memory_count = 0
        for i in all_pid:
            with open('/proc/%s/status' % i) as P:
                end = re.findall(re_f,P.read())
                if end:
                    memory_count += int(end[0])
        return memory_count

    def main(self):
        all_pid = self._show_pid()
        memory_count = self._usage_memory(all_pid)
        F = namedtuple('pid',['memory',"pid"])
        return F(memory_count,all_pid)


def pid(pid_name):
    'show pid memory pid  '
    return _pid(pid_name).main()
