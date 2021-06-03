#!/usr/bin/env python
#encoding=utf-8

class RaiseVlues(Exception):
    def __init__(self,value):
        """
        :param value:message text
        """
        self.value = value
        self.message = value

    def __str__(self):
        return repr(self.value)
