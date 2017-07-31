#!/usr/bin/env python
#encoding=utf-8

class RaiseVlues(Exception):
    def __init__(self,message,value=False):
        Exception.__init__(self)
        self.message=message
        if value:
            self.value = value

