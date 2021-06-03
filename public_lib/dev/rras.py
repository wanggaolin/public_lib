#!/usr/bin/env python
#encoding=utf-8
from dev_lib import CurrTime
import rrdtool
import time
import os
import random
import sys
import tempfile
reload(sys)
sys.setdefaultencoding( "utf-8" )

class rrd:
    def __init__(self):
        self.rrd_name = False
        self.interval = 300                     #数据时间戳间隔时间,单位秒
        self.start_time = False                 #数据开始时间和结束时间，不指定默认为根据数据选择
        self.end_time = False
        self.photo_width = 650
        self.photo_height = 230
        self.time_format = '%Y-%m-%d %H\:%M\:%S'
        self.units = ''
        self.y_desc = ''
        self.title = CurrTime()
        self.img = '/tmp/1.png'

    def rrd_create(self,**kwargs):
        create_time_start = kwargs['data_start_time']
        if create_time_start > self.start_time:
            create_time_start = self.start_time
        if self.rrd_name is False:
            self.rrd_name = tempfile.mkstemp(text=True, suffix='.'+str(int(time.time()*1000))+'.rrd', prefix='.putlic_lib.')[-1]
        heartbeat_inter = str(int(self.interval+self.interval*0.5))
        data_statis = kwargs['data_count']
        c1 = [
            self.rrd_name, '--step', str(self.interval), '--start',  str(create_time_start-2),
                'RRA:AVERAGE:0.5:1:600',
                'RRA:AVERAGE:0.5:6:700',
                'RRA:AVERAGE:0.5:24:775',
                'RRA:AVERAGE:0.5:288:797',
                'RRA:MAX:0.5:1:600',
                'RRA:MAX:0.5:6:700',
                'RRA:MAX:0.5:24:775',
                'RRA:MAX:0.5:444:797',
                'RRA:MIN:0.5:1:600',
                'RRA:MIN:0.5:6:700',
                'RRA:MIN:0.5:24:775',
                'RRA:MIN:0.5:444:797',
                   # 'RRA:AVERAGE:0.5:1:%s' % data_statis,
                   # 'RRA:MAX:0.5:2:%s' % data_statis,
                   # 'RRA:MIN:0.5:2:%s' % data_statis,
        ]
        for lable_name in kwargs['lable']:
            c1.append("DS:%s:GAUGE:%s:0:U" % (lable_name['name_hide'],heartbeat_inter))
        rrdtool.create(*[ _x.encode("utf-8") for _x in c1 ])

    def str(self,x):
        return x.encode("utf-8")

    def update(self,data_value):
        """
        :param data_value: [time,value1,valu2]
        """
        return rrdtool.updatev(self.str(self.rrd_name),':'.join(data_value))

    def color(self):
        return ['#1A7C11', '#F63100', '#2774A4', '#A54F10', '#FC6EA3', '#6C59DC', '#AC8C14', '#611F27', '#F230E0',
                      '#5CCD18', '#BB2A02', '#5A2B57', '#89ABF8', '#7EC25C', '#274482', '#Add']

    def photo_create(self,**kwargs):
        """
        :param kwargs:
            :data_count: create photo data count
        :return:
        """
        time_cha = float(self.end_time - self.start_time)
        x_inter  = int(time_cha / 10/60)
        x_grid = "MINUTE:%s:MINUTE:%s:MINUTE:%s:0:" % (x_inter*3,x_inter*2,x_inter)

        if (time_cha/60/60/24/365) > 1:  #year
            x_grid = x_grid + "%y-%m"

        elif (time_cha/60/60/24/31) > 1:  #month
            x_grid = x_grid + "%B"

        elif (time_cha/60/60/24) > 1:  #day
            x_grid = x_grid + "%d"

        elif (time_cha/60/60) > 1:  #hour
            x_grid = x_grid + "%H:%M"
        else:
            x_grid = x_grid + "%H:%M"
            if x_inter < 1:
                x_inter = int(time_cha / 6)
                x_grid = "SECOND:%s:SECOND:%s:SECOND:%s:0:" % (x_inter * 3, x_inter * 2,x_inter)
                x_grid = x_grid + "%H:%M:%S"

        x = {
            "x_lable_size":1,
            "x_min_inter":1,
            "y_desc":self.y_desc,
            "start":time.strftime(self.time_format, (time.localtime(self.start_time))),
            "end":time.strftime(self.time_format, (time.localtime(self.end_time))),
        }

        f1 = [
            self.img, "--start", str(self.start_time-2),"--end", str(self.end_time+1),"--vertical-label=%(y_desc)s" % x,
            "--x-grid", x_grid,
            "--width", str(self.photo_width), "--height", str(self.photo_height), "--title",self.title,
            "--watermark",kwargs['company'],
            "COMMENT:From %(start)s To %(end)s\c" % x,
            "COMMENT:\\r",
            "TEXTALIGN:right",
            "--color","FONT#000000",
            "--color","BACK#F3F3F3",
            "--color","CANVAS#FDFDFD",
            "--color","SHADEA#CBCBCB",
            "--color","SHADEB#999999",
            "--color","AXIS#2C4D43",
            "--color","ARROW#2C4D43",
            "--color","FRAME#2C4D43",
            # "--font","TITLE:11:'Arial'",
            # "--font","AXIS:8:'Arial'",
            # "--font","LEGEND:8:'Courier'",
            # "--font","UNIT:8:'Arial'",
            "--slope-mode",
        ]

        for number,lable_name in enumerate(kwargs['lable']):
            n = {
                "lable_name":lable_name['name'],
                "key_name":lable_name['name_hide'],
                "key_cal":lable_name['name_cal'],
                "rrd_name":self.rrd_name,
                "color":lable_name.get('color',self.color()[number]),
                "unit": self.units,
                "type":lable_name.get('type','LINE1')
            }
            f1.append("DEF:%(key_name)s=%(rrd_name)s:%(key_name)s:AVERAGE" % n)
            f1.append("%(type)s:%(key_name)s%(color)s:%(lable_name)s   " % n)
            f1.append("CDEF:%(key_cal)s=%(key_name)s" % n)
            f1.append("GPRINT:%(key_cal)s:AVERAGE:Avg\:%%6.2lf%%S%(unit)s" % n)
            f1.append("COMMENT: ")
            f1.append("GPRINT:%(key_cal)s:MAX:Max\:%%6.2lf%%S%(unit)s" % n)
            f1.append("COMMENT: ")
            f1.append("GPRINT:%(key_cal)s:MIN:Min\:%%6.2lf%%S%(unit)s\\l" % n)
        rrdtool.graph(*[ self.str(_x) for _x in f1])
        return self.img

    def load(self,data):
        """
        {
            "time":[1529205520,1529205521], #时间戳
            "lable":[{"name":"w1","type":"AREA".'color':'#5A2B57'},{"name":"w2"}], #name:标签,type:绘图类型，默认线性[LIN1],name图表颜色[默认自动分配]
            "w1":[1,2],     #w1对应的数据
            "w2":[5,9],     #w2对应的数据
        }
        :return:
        """
        if self.start_time is False:
            self.start_time = int(data['time'][0])
        if self.end_time is False:
            self.end_time = int(data['time'][-1])
        lable_data = []
        for lable_id,lable_z in enumerate(data['lable']):
            lable_z["name_hide"] = "a" + str(lable_id)
            lable_z["name_cal"] = "ac" + str(lable_id)
            lable_data.append(lable_z)

        k = {
            "lable":lable_data,
            "data_count":len(data['time']),
            "company":data.get("company","demo from brach@lssin.com"),
            "data_start_time":int(data['time'][0])
        }
        self.rrd_create(**k)
        for num in xrange(len(data['time'])):
            w = [ str(data[lable_name['name']][num]) for lable_name in data['lable']]
            w.insert(0,str(data['time'][num]))
            self.update(w)
        self.photo_create(**k)
        if os.path.exists(self.rrd_name):
            os.remove(self.rrd_name)
        return  self.img

if __name__ == "__main__":
    F = rrd()
    F.interval = 5
    F.units = 'G'
    F.y_desc = 'xxxxx'
    F.title = '测试图表'
    F.img = '1.png'
    F.start_time = 1529206065-5
    l = {
        'time': ['1529206065', '1529206070', '1529206075', '1529206080', '1529206085'],
        'lable': [{'type': 'AREA', 'name': 'w1123','color':'#5A2B57'}, {'name': 'w2'}],
        'w2': [81, 2, 60, 80, 78],
        'w1123': [3, 24, 59, 11, 11]
    }
    print F.load(l)

