#!/usr/bin/env python
#encoding=utf-8
#Created by gaolin on 2017-06-06 16:03

import re
import sys
import traceback
from error_msg import RaiseVlues
from dev_lib import check_ip
from collections import namedtuple
from req_check_language import alarm_language
reload(sys)
sys.setdefaultencoding( "utf-8" )

def check_bank(bank):
    'check bank number `bank number`'
    try:
        digits = list(map(int, str(bank)))
    except ValueError:
        return False
    j = sum(digits[-1::-2])
    o = 0
    for n in digits[-2::-2]:
        l = n * 2
        if l > 9: l = l - 9
        o += l
    return ((j + o) % 10) == 0


def check_card(card_number):
    'check card `card number`'
    id_number = str(card_number)
    try:
        map(int,str(id_number)[:-1])
    except ValueError,e:
        return False
    if 1800 < int(id_number[6:10]) < 2100:
        if int(id_number[10:12]) < 13 and int(id_number[12:14]) < 32:
            ratio = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            corres = {'0': 1, '1': 0, '2': 'x', '3': 9, '4': 8, '5': 7, '6': 6, '7': 5, '8': 4, '9': 3, '10': 2}
            j = 0
            for num, car in enumerate(list(id_number)[:-1]):
                j += int(car) * int(ratio[num])
            return str(corres[str(j % 11)]) == str(id_number.lower()[-1])
    return False


def check_mobile(x):
    """
    check mobile
        移动：a=['134', '135', '136', '137', '138', '139', '1390', '1391', '147', '150', '151', '152', '157', '158', '159', '1703', '1705', '1706', '178', '182', '183', '184', '187', '188']
        联通：b=['130', '131', '132', '145', '155', '156', '1707', '1708', '1709', '175', '176', '185', '186', '1860']
        电信：c=['133', '1330', '153', '1700', '1701', '1702', '173', '177', '180', '181', '189', '1890']
             print '|'.join(sorted(set([ i for i in a+b+c if len(str(i)) < 4 ])))

    :param x:moblie number
    :return:True
    """
    try:
        x = str(int(x))
        if len(x) == 11:
            if re.findall(r'^(?:130|131|132|133|134|135|136|137|138|139|145|147|150|151|152|153|155|156|157|158|159|173|175|176|177|178|180|181|182|183|184|185|186|187|188|189)',x):
                return True
    except ValueError,e:
        pass
    return False

def check_symbols(x,re_rule=False):
    """
    check text inclued symbols
    :param x:text
    :param re_rule:re.findall rule
    :return:
    """
    F = namedtuple('symbols', ['status', "symbols"])
    if re_rule is False:
        re_rule = re.compile(r'\*|%|\.\.')
    end = re.findall(re_rule,x)
    if end:
        end = F(False, ' '.join(end))
    else:
        end = F(True, '')
    return end

class check_req(object):
    'check argument `data={}`'
    def __init__(self,*args,**kwargs):
        """
        :param kwargs:
             :data: check data argument,type is dict
        """
        self.data = kwargs['data']
        self.error = {'status':False,'data':self.data,'msg':'success'}

    def _number(self,data):#判断是否是数字
        'check data is number'
        try:
            print data
            float(data)
        except ValueError, e:
            return False
        return True

    def _number_or_str(self,data):#判断是否是数字
        'check data is number or str'
        if re.findall('^\w+$',data):
            return True
        return False

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
        """
        check argument of rule,type is dict
        :param kwargs:
            :language:alalrm language,default is zh
            :rule:
                number:True     必须是数字[小数点/整数/负数]
                number_str:True 只能输入字母或数字
                time_day:true	必须输入正确格式的日期（ISO），例如：2009-06-23/1998/01/22。只验证格式，不验证有效性。
                minlength:10	输入长度最小是 10 的字符串（汉字算一个字符）。
                maxlength:5	    输入长度最多是 5 的字符串（汉字算一个字符）。
                rangelength:[5,10]	输入长度必须介于 5 和 10 之间的字符串（汉字算一个字符）。
                max:5	        输入的数字不能大于 5。
                min:10	        输入的数字不能小于 10。
                file:True	    必须是一个文件路径。
                email:True	    必须是一个邮箱
                bank:True	    必须是一个银行卡号
                card:True	    必须是一个身份证号
                ip:True	        必须是一个合法ip地址
                mobile:True	    必须是一个手机号码
                symbols:Ture    不得包含特殊符号:*,%
        :return: {}
        """
        try:
            language_name = kwargs.get('language','zh')
            for rule_name,rule_value in  kwargs['rule'].items(): #遍历所有规则
                end = self.data.get(rule_name) #判断某个字段是非启用过滤规则
                name_alias = rule_value.get('alias', '')
                if not name_alias:
                    import warnings
                    warnings.warn("must be key of alias")
                if end:
                    end = unicode(str(end), "utf-8")
                    len_end = len(end)
                    if rule_value.get('number') is True: #判断values是否是数字
                        if self._number(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['number'][language_name])

                    if rule_value.get('minlength'): #判断values 位数是否小于n
                        minlength = rule_value.get('minlength')
                        if len_end < minlength:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['minlength'][language_name].replace('{number}',str(minlength)))

                    if rule_value.get('maxlength'): #判断values 位数是否大于n
                        maxlength = rule_value.get('maxlength')
                        if len_end > maxlength:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['maxlength'][language_name].replace('{number}',str(maxlength)))

                    if rule_value.get('rangelength'):  # 判断values 位数是在x和y之间
                        rangelength = rule_value.get('rangelength')
                        minlength,maxlength = rangelength
                        if minlength > len_end or len_end > maxlength:
                            self.error['msg'] = "%s%s" % (name_alias,
                               alarm_language['rangelength'][language_name].replace('{number1}', str(minlength)).replace('{number2}', str(maxlength)))

                    if rule_value.get('max'):  # 判断values 是否大于n
                        number_max = rule_value.get('max')
                        try:
                            end = int(end)
                            if number_max < end:
                                self.error['msg'] = "%s%s" % (name_alias,alarm_language['max'][language_name].replace('{number}',number_max))
                        except ValueError,e:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['max'][language_name].replace('{number}',str(number_max)))

                    if rule_value.get('min'):  # 判断values 是否小于n
                        number_mix = rule_value.get('min')
                        try:
                            end = int(end)
                            if number_mix > end:
                                self.error['msg'] = "%s%s" % (name_alias, alarm_language['min'][language_name].replace('{number}',str(number_mix)))
                        except ValueError, e:
                            self.error['msg'] = "%s%s" % (name_alias, alarm_language['min'][language_name].replace('{number}',str(number_mix)))

                    if rule_value.get('number_str') is True:  # 判断values 是否是数字或字母
                        if self._number_or_str(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['number_str'][language_name])

                    if rule_value.get('time_day') is True:
                        time_day = rule_value.get('time_day')
                        if self._time_day(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['time_day'][language_name])

                    if rule_value.get('file') is True:
                        if re.findall('\.\.',end):
                            self.error['msg'] = "%s%s.." % (name_alias,alarm_language['file'][language_name])
                        elif re.findall('\./', end):
                            self.error['msg'] = "%s%s./" % (name_alias,alarm_language['file'][language_name])
                        elif re.findall('\*', end):
                            self.error['msg'] = "%s%s*" % (name_alias,alarm_language['file'][language_name])
                        elif re.findall(' ', end):
                            self.error['msg'] = "%s%s空格" % (name_alias,alarm_language['file'][language_name])

                    if rule_value.get('email') is True:
                        if not re.findall(r'^[\w|-|_]+@[\w|-|_]+\.(?:com|cn|xin|top|site|net|cc|org|tv|\.)+$',end):
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['email'][language_name])

                    if rule_value.get('bank') is True:
                        if check_bank(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['bank'][language_name])

                    if rule_value.get('card') is True:
                        if check_card(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['card'][language_name])

                    if rule_value.get('ip') is True:
                        if check_ip(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['ip'][language_name])

                    if rule_value.get('mobile') is True:
                        if check_mobile(end) is False:
                            self.error['msg'] = "%s%s" % (name_alias,alarm_language['mobile'][language_name])

                    if rule_value.get('symbols') is True:
                        end = check_symbols(end)
                        if end.status is False:
                            self.error['msg'] = "%s%s:%s" % (name_alias, alarm_language['symbols'][language_name],end.symbols)

                    if self.error['msg'] != 'success':
                        return self.error
                else:
                    self.error['msg'] = "%s%s" % (name_alias, alarm_language['default'][language_name])
                    return self.error
        except Exception,e:
            raise RaiseVlues(e)
        self.error['status'] = True
        return self.error
#
#
# import public_lib
# # for i in ['zh','en']:
# for i in ['zh']:
#     print public_lib.json_data(check_req(data=
#               {
#                   "a":'asdasdasd'
#               }).rule(language=i,rule={
#                 "a":{
#                     "alias": "手机号",  # 别名
#                     "rangelength":[100,120],
#                  }
#     }))
#
#
#
