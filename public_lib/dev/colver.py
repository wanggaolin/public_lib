#!/usr/bin/env python
#coding=utf-8
from error_msg import RaiseVlues

class _color(object):
    def __init__(self):
        'print color font'
        self.font_color = {
            "red": 31,
            "green": 32,
            "yellow":33,
            "bule": 34,
            "purple":35
        }

    def red(self,x,color):
        """
        :param x: conntext
        :param color:=color name of read or green ...
        :return:conntext
        """
        try:
            return "\033[1;%sm%s\033[m" % (self.font_color[color],x)
        except KeyError,e:
            raise RaiseVlues("color mush be:%s"% self.font_color.keys())

    def red_number(self,x,num):
        """
        :param x:conntext
        :param num: color number of 31,32,33,34,35
        :return: conntext
        """
        return "\033[1;%sm%s\033[m" % (int(num),x)


def color(x,name='red',number=False):
    """
    :param x: conntext
    :param name: color name of read or green ...
    :param number: color number of 31,32,33,34,35
    :return: conntext
    """
    if number:
        if 0 < int(number) < 255:
            return _color().red_number(x,number)
        else:
            raise RaiseVlues("color number must be 1~255")
    else:
        return _color().red(x, name)


