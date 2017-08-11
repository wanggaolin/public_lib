#!/usr/bin/env python
#encoding=utf-8
#Created by gaolin on 2017-06-06 16:03
# 'http post or get vrgument check'
import re
import traceback
from error_msg import RaiseVlues

def bank_check(bank):
    'check bank number `bank number`'
    digits = list(map(int, str(bank).strip()))
    j = sum(digits[-1::-2])
    o = 0
    for n in digits[-2::-2]:
        l = n * 2
        if l > 9: l = l - 9
        o += l
    return ((j + o) % 10) == 0


def card_check(card_number):
    'check card `card number`'
    id_number = str(card_number).strip()
    if 1800 < int(id_number[6:10]) < 2100:
        if int(id_number[10:12]) < 13 and int(id_number[12:14]) < 32:
            ratio = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            corres = {'0': 1, '1': 0, '2': 'x', '3': 9, '4': 8, '5': 7, '6': 6, '7': 5, '8': 4, '9': 3, '10': 2}
            j = 0
            for num, car in enumerate(list(id_number)[:-1]):
                j += int(car) * int(ratio[num])
            return str(corres[str(j % 11)]) == str(id_number.lower()[-1])
    return False

class req_check(object):
    'check argument `data={}`'
    def __init__(self,*args,**kwargs):
        'with data check `data`'
        self.data = kwargs['data']
        self.error = {'status':False,'data':self.data,'msg':'success'}

    def _number(self,data):#判断是否是数字
        'check data is number'
        status = True
        if re.findall('\.',data):
            try:
                float(data)
            except ValueError, e:
                status = False
        else:
            try:
                int(data)
            except ValueError,e:
                status = False
        return status

    def _number_or_str(self,data):#判断是否是数字
        'check data is number or str'
        status = False
        find_data = re.findall('[a-zA-Z0-9]+',data)
        if find_data:
            if find_data[0] == data:
                return True
        return status

    def _mon_or_day_ok(self,data):
        'check month or day in day is ok' #检查日期中，月和日是否合法
        status = True
        daymon,dayday = data
        if int(daymon) > 12 or int(dayday) > 31:
            status = False
        return status

    def _time_day(self,data):
        'check data is time [2017-06-06|2017/06/06]'
        status = False
        time_1 = re.findall('\d{4}-\d{2}-\d{2}',data)
        if time_1:
            if time_1[0] == data:
                day1 = re.findall('\d{4}-(\d{2})-(\d{2})',data)
                status = self._mon_or_day_ok(day1[0])
        time_2 = re.findall('\d{4}/\d{2}/\d{2}', data)
        if time_2:
            if time_2[0] == data:
                day2 = re.findall('\d{4}/(\d{2})/(\d{2})',data)
                status = self._mon_or_day_ok(day2[0])
        return status

    def rule(self,*args,**kwargs):
        'check rule `rule={}`'
        try:
            self.rule = kwargs['rule']
            for rule_name,rule_value in  self.rule.items(): #遍历所有规则
                end = self.data.get(rule_name) #判断某个字段是非启用过滤规则
                if end:
                    end = unicode(str(end), "utf-8")
                    len_end = len(end)
                    name_alias = rule_value.get('alias','')
                    if rule_value.get('number'): #判断values是否是数字
                        if self._number(end) is False:
                            self.error['msg'] = "%s必须是一个整数" % name_alias
                            return self.error

                    if rule_value.get('minlength'): #判断values 位数是否小于n
                        minlength = rule_value.get('minlength')
                        if len_end < minlength:
                            self.error['msg'] = "%s最少要输入%s个字符" % (name_alias,minlength)
                            return self.error

                    if rule_value.get('maxlength'): #判断values 位数是否大于n
                        maxlength = rule_value.get('maxlength')
                        if len_end > maxlength:
                            self.error['msg'] = "%s最多输入%s个字符" % (name_alias,maxlength)
                            return self.error

                    if rule_value.get('rangelength'):  # 判断values 位数是在x和y之间
                        rangelength = rule_value.get('rangelength')
                        minlength,maxlength = rangelength
                        if minlength > len_end or len_end > maxlength:
                            self.error['msg'] = "%s必须介于%s和%s之间的字符" % (name_alias, minlength,maxlength)
                            return self.error

                    if rule_value.get('max'):  # 判断values 是否大于n
                        number_max = rule_value.get('max')
                        try:
                            end = int(end)
                            if number_max < end:
                                self.error['msg'] = "%s不能大于%s" % (name_alias,number_max)
                                return self.error
                        except ValueError,e:
                            self.error['msg'] = "%s不能大于%s" % (name_alias,number_max)
                            return self.error

                    if rule_value.get('min'):  # 判断values 是否小于n
                        number_mix = rule_value.get('min')
                        try:
                            end = int(end)
                            if number_mix > end:
                                self.error['msg'] = "%s不能小于%s" % (name_alias, number_mix)
                                return self.error
                        except ValueError, e:
                            self.error['msg'] = "%s不能小于%s" % (name_alias, number_mix)
                            return self.error

                    if rule_value.get('number_str'):  # 判断values 是否是数字或字母
                        if self._number_or_str(end) is False:
                            self.error['msg'] = "%s只能输入字母或数字" % (name_alias)
                            return self.error

                    if rule_value.get('time_day'):  # 判断values 位数是否大于n
                        time_day = rule_value.get('time_day')
                        if self._time_day(end) is False:
                            self.error['msg'] = "%s必须是正确格式的日期" % (name_alias)
                            return self.error
        except Exception,e:
            raise RaiseVlues(e)
        self.error['status'] = True
        return self.error

