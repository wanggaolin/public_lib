#!/usr/bin/env python
#encoding=utf-8
#Created by gaolin on 2017-08-10 10:49
import  public_lib
import time

F = public_lib.proging_rate(screen_max=10, screen_name='10M', rate_symbol='#')
for i in range(10):
    F.update("%sM" % i)
    time.sleep(3)
F.end()
