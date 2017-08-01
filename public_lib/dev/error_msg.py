#!/usr/bin/env python
#encoding=utf-8

class RaiseVlues(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)
