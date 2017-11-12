#!/usr/bin/env python
#encoding=utf-8
#Created by gaolin on 2017-06-06 16:03
import copy
import re
import sys
import json
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
    if x:
        if re_rule is False:
            re_rule = re.compile(r'\*|\.\.|\\')
        end = re.findall(re_rule,x)
        if end:
            end = F(False, ' '.join(end))
        else:
            end = F(True, '')
    else:
        end = F(False,'')
    return end

def check_mac(mac_name):
    if mac_name:
        if re.findall(r'^(?:[a-zA-Z0-9][a-zA-Z0-9]\:){5}[a-zA-Z0-9][a-zA-Z0-9]$',mac_name):
            return True
    return False


class check_req(object):
    'check argument `data={}`'
    def __init__(self,*args,**kwargs):
        """
        :param kwargs:
             :data: check data argument,type is dict
        """
        self.data = kwargs['data']
        self.verfy = copy.deepcopy(self.data)
        self.error = {'status':False,'data':{},'msg':'success'}

    def _number(self,data):#判断是否是数字
        'check data is number'
        try:
            float(data)
        except ValueError, e:
            return False
        return True

    def _number_or_str(self,data):#判断是否是数字
        'check data is number or str'
        if re.findall('^[0-9a-zA-Z]+$',data):
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
        'check data is time [2017-06-06]'
        status = False
        if re.findall('^\d{4}-\d{1,2}-\d{1,2}$',data):
            day1 = re.findall('\d{4}-(\d{1,2})-(\d{1,2})',data)
            status = self._mon_or_day_ok(day1[0])
        return status

    def _time_day_1(self,data):
        'check data is time [2017/06/06]'
        status = False
        if re.findall('^\d{4}/\d{1,2}/\d{1,2}$', data):
            day2 = re.findall('^\d{4}/(\d{1,2})/(\d{1,2})',data)
            status = self._mon_or_day_ok(day2[0])
        return status

    def _time_1(self,data):
        'check data is time [2009-06-23 12:12:12]'
        status = False
        print data,123
        if re.findall('^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$',data):
            day1 = re.findall('^\d{4}-(\d{1,2})-(\d{1,2})',data)
            status = self._mon_or_day_ok(day1[0])
        return status

    def _time_2(self,data):
        'check data is time [2009-06-23 12:12:12]'
        status = False
        if re.findall('^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}$',data):
            day1 = re.findall('^\d{4}-(\d{1,2})-(\d{1,2})',data)
            status = self._mon_or_day_ok(day1[0])
        return status

    # def _error(self,default_error,key_name,msg_error):
    def _error(self,**kwargs):
        errors_msg = kwargs['default'].get(kwargs['key_name'])
        msg = kwargs['msg']
        try:
            del self.verfy[kwargs['key_role']]
        except KeyError,e:
            pass
        if errors_msg:
            return errors_msg
        return msg

    def rule(self,*args,**kwargs):
        """
        check argument of rule,type is dict
        :param kwargs:
            :language:alalrm language,default is zh
            :rule:
                number:True     必须是数字[小数点/整数/负数]
                number_str:True 只能输入字母或数字
                time_day:true	必须输入正确格式的日期（ISO），例如：2009-06-23 只验证格式，不验证有效性。
                time_day_1:true	必须输入正确格式的日期（ISO），例如：1998/01/2 只验证格式，不验证有效性。
                times_1:true	必须输入正确格式的日期（ISO），例如：2009-06-23 12:12:12 只验证格式，不验证有效性。
                times_2:true	必须输入正确格式的日期（ISO），例如：2009-06-23 12:12 只验证格式，不验证有效性。
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
                mac:True	    必须是一个合法mac地址
                mobile:True	    必须是一个手机号码
                symbols:Ture    不得包含特殊符号:*,%,..,\
                json_load:Ture  必须是一个json可解析的格式
                domain:Ture     必须是一个域名
        :return: {}
        """
        try:
            language_name = kwargs.get('language','zh')
            for rule_name,rule_value in  kwargs['rule'].items(): #遍历所有规则
                end = self.data.get(rule_name) #判断某个字段是非启用过滤规则
                name_alias = rule_value.get('alias', '')
                default_error = rule_value.get('error', {})
                if not name_alias:
                    import warnings
                    warnings.warn("must be key of alias")
                if end:
                    end = unicode(str(end), "utf-8")
                    len_end = len(end)
                    if rule_value.get('number') is True: #判断values是否是数字
                        if self._number(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['number'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='number',msg=error_message)

                    if rule_value.get('minlength'): #判断values 位数是否小于n
                        minlength = rule_value.get('minlength')
                        if len_end < minlength:
                            error_message = "%s%s" % (name_alias,alarm_language['minlength'][language_name].replace('{number}',str(minlength)))
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='minlength',msg=error_message)

                    if rule_value.get('maxlength'): #判断values 位数是否大于n
                        maxlength = rule_value.get('maxlength')
                        if len_end > maxlength:
                            error_message = "%s%s" % (name_alias,alarm_language['maxlength'][language_name].replace('{number}',str(maxlength)))
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='maxlength',msg=error_message)

                    if rule_value.get('rangelength'):  # 判断values 位数是在x和y之间
                        rangelength = rule_value.get('rangelength')
                        minlength,maxlength = rangelength
                        if minlength > len_end or len_end > maxlength:
                            error_message = "%s%s" % (name_alias,alarm_language['rangelength'][language_name].replace('{number1}', str(minlength)).replace('{number2}', str(maxlength)))
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='rangelength',msg=error_message)

                    if rule_value.get('max'):  # 判断values 是否大于n
                        number_max = rule_value.get('max')
                        try:
                            end = int(end)
                            if number_max < end:
                                error_message = "%s%s" % (name_alias,alarm_language['max'][language_name].replace('{number}',number_max))
                                self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='max',msg=error_message)
                        except ValueError,e:
                            error_message = "%s%s" % (name_alias,alarm_language['max'][language_name].replace('{number}',str(number_max)))
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='max',msg=error_message)

                    if rule_value.get('min'):  # 判断values 是否小于n
                        number_mix = rule_value.get('min')
                        try:
                            end = int(end)
                            if number_mix > end:
                                error_message = "%s%s" % (name_alias,alarm_language['min'][language_name].replace('{number}',str(number_mix)))
                                self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='min',msg=error_message)
                        except ValueError, e:
                            error_message = "%s%s" % (name_alias, alarm_language['min'][language_name].replace('{number}',str(number_mix)))
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='min',msg=error_message)

                    if rule_value.get('number_str') is True:  # 判断values 是否是数字或字母
                        if self._number_or_str(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['number_str'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='number_str',msg=error_message)

                    if rule_value.get('time_day') is True:
                        time_day = rule_value.get('time_day')
                        if self._time_day(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['time_day'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='time_day',msg=error_message)

                    if rule_value.get('time_day_1') is True:
                        time_day = rule_value.get('time_day_1')
                        if self._time_day_1(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['time_day_1'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='time_day',msg=error_message)

                    if rule_value.get('times_1') is True:
                        time_day = rule_value.get('times_1')
                        if self._time_1(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['times_1'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='times_1',msg=error_message)

                    if rule_value.get('times_2') is True:
                        time_day = rule_value.get('times_2')
                        if self._time_2(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['times_2'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='times_2',msg=error_message)

                    if rule_value.get('file') is True:
                        if re.findall('\.\.',end):
                            error_message = "%s%s: .." % (name_alias,alarm_language['file'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='file',msg=error_message)
                        elif re.findall('\./', end):
                            error_message = "%s%s: ./" % (name_alias,alarm_language['file'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='file',msg=error_message)
                        elif re.findall('\*', end):
                            error_message = "%s%s*" % (name_alias,alarm_language['file'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='file',msg=error_message)
                        elif re.findall(' ', end):
                            error_message = "%s%s: ' '" % (name_alias,alarm_language['file'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='file',msg=error_message)
                        elif not re.findall('/', end):
                            error_message = "%s%s: '/'" % (name_alias, alarm_language['file1'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='file1',msg=error_message)

                    if rule_value.get('email') is True:
                        if not re.findall(r'^[\w|-|_|\.]+@[\w|-|_]+\.(?:com|cn|xin|top|site|net|cc|org|tv|\.)+$',end):
                            error_message = "%s%s" % (name_alias,alarm_language['email'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='email',msg=error_message)

                    if rule_value.get('bank') is True:
                        if check_bank(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['bank'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='bank',msg=error_message)

                    if rule_value.get('card') is True:
                        if check_card(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['card'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='card',msg=error_message)

                    if rule_value.get('ip') is True:
                        if check_ip(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['ip'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='ip',msg=error_message)

                    if rule_value.get('mac') is True:
                        if check_mac(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['mac'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='mac',msg=error_message)

                    if rule_value.get('mobile') is True:
                        if check_mobile(end) is False:
                            error_message = "%s%s" % (name_alias,alarm_language['mobile'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='mobile',msg=error_message)

                    if rule_value.get('symbols') is True:
                        end = check_symbols(end)
                        if end.status is False:
                            error_message = "%s%s:%s" % (name_alias, alarm_language['symbols'][language_name],end.symbols)
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='symbols',msg=error_message)

                    if rule_value.get('json_load') is True:
                        try:
                            json.loads(end)
                        except Exception,e:
                            error_message = "%s %s" % (name_alias, alarm_language['json_load'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='json_load',msg=error_message)

                    if rule_value.get('domain') is True:
                        if not re.findall(r'^[\w|\d|-]+\.[\w|\d|-|\.]{0,}[\w|\d]+$',end):
                            error_message = "%s%s" % (name_alias, alarm_language['domain'][language_name])
                            self.error['msg'] = self._error(key_role=rule_name,default=default_error,key_name='domain',msg=error_message)
                else:
                    try:
                        del self.verfy[rule_name]
                    except KeyError,e:
                        pass
                    self.error['msg'] = "%s%s" % (name_alias, alarm_language['default'][language_name])
                    self.error['data'] = self.verfy
        except Exception,e:
            # raise RaiseVlues(e)
            raise RaiseVlues(traceback.format_exc())
        if self.error['msg'] == 'success':
            self.error['status'] = True
        self.error['data'] = self.verfy
        return self.error

# print check_mac('b8:70:f4:1d:fc:61')
#
#
# import public_lib
# f = {'aaa': 'b8:70:f4:1d:fc:61'}
# for i in ['zh']:
#     print public_lib.json_data(check_req(data=f).rule(language=i,rule={
#         "aaa": {
#             "alias": "结束日期",
#             "mac": True,
#         }}))
