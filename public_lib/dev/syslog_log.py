#!/usr/bin/env python
#encoding=utf-8

import syslog

class _syslog(object):
    def __int__(self):
        pass

    def info(self,*args,**kwargs):
        syslog.syslog(syslog.LOG_INFO,*args,**kwargs)

    def debug(self,*args,**kwargs):
        syslog.syslog(syslog.LOG_DEBUG,*args,**kwargs)

    def waring(self, *args, **kwargs):
        syslog.syslog(syslog.LOG_WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        syslog.syslog(syslog.LOG_ERR, *args, **kwargs)

_system_logs = _syslog()
