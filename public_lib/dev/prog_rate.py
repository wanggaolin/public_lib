#!/usr/bin/env python
#encoding=utf-8
import time
import sys

def format_time_int(t):
    'format int to time 00:00:00'
    end = ["00","00","00"]
    t = float(t)
    if t < 60:
        end[2] = int(t)
    else:
        f = int(t/60)
        if f < 60:
            end[1] = f
            end[2] = int(t - (60*f))
        else:
            h = int(t/60/60)
            end[0] = h
            x = int(t - (60*60*int(t/60/60)))
            if x < 60:
                end[2] = x
            else:
                p = int(x / 60)
                end[1] = p
                end[2] = int(x - (60 * p))
    return ':'.join([ str(i).rjust(2,'0') for i in end])


class proging_rate(object):
    def __init__(self,*args,**kwargs):
        """
        :param args:
            screen_max:Ergodic max value
            screen_name:show screen value
        :param kwargs:
        """
        self.screen_max = kwargs['screen_max']
        self.screen_name = kwargs.get('screen_name',self.screen_max)
        self.number = 0
        self.rate_symbol = kwargs.get('rate_symbol','*')
        self.start_time = time.time()

    #Speed of progress[%]
    def _rate(self):
        return "%0.2f" % ((float(self.number) / self.screen_max)*100)

    def update(self,data):
        """
        :param data:show value
        :return:
        """
        try:
            self._rate()
            data = str(data)
            rate = self._rate()
            sys.stdout.write("\r{rate_symbol}|{current}/{screen_name}|{rate}% [Time:{time}]".format(
                screen_name=self.screen_name,
                current=data.rjust(len(self.screen_name),' '),
                rate=rate,
                rate_symbol=(self.rate_symbol * int(round(float(rate)))).ljust(100,' '),
                time=format_time_int(time.time()-self.start_time)
            ))
            self.number += 1
            sys.stdout.flush()
        except KeyboardInterrupt,e:
            pass

    def end(self):
        self.update(self.screen_name)
        print ""

if __name__ == "__main__":
    pass