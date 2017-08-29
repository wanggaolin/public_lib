#!/usr/bin/env python
#encoding=utf-8
import requests
import json
import time
class RaiseVlues(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class _zabbix(object):
    'require:zabbix version 2.2'
    def __init__(self,*args,**kwargs):
        'request: `host` `timeout=20` '
        self.host = kwargs.get('host','')
        self.timeout = kwargs.get('timeout',20)
        self.LoginVerfy = False
        self.zabbix_agent = {'Zabbix_trapper': '2', 'Zabbix_agent_(active)': '7', 'JMX_agent': '16', 'IPMI_agent': '12', 'database_monitor': '11', 'web_item': '9', 'Zabbix_agent': '0', 'SNMPv3_agent': '6', 'SSH_agent': '13', 'TELNET_agent': '14', 'external_check': '10', 'SNMP_trap.': '17', 'simple_check': '3', 'SNMPv1_agent': '1', 'Zabbix_internal': '5', 'Zabbix_aggregate': '8', 'calculated': '15', 'SNMPv2_agent': '4'}
        self.base = {}

    def _req(self,*args,**kwargs):
        DefaultHead = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.13381.9 Safari/537.36 zabbix_api'}
        data = kwargs.get('data', {})
        data["jsonrpc"] = "2.0"
        data["id"] = "1"
        Html = requests.post(self.host+'/api_jsonrpc.php', data=json.dumps(data), headers=DefaultHead, timeout=self.timeout)
        try:
            return json.loads(Html.text)
        except ValueError,e:
            raise RaiseVlues('request error:%s' % Html.text)

    def login(self,*args,**kwargs):
        """
        zabbix login
        :param kwargs:
            :user:zabbix login of username
            :passwd:zabbix login of password
        :return:
        """
        Data = {
                "jsonrpc": "2.0","method": "user.login",
                "params": {
                    "user": kwargs.get('user',''),
                    "password": kwargs.get('passwd','')
                },"id": 1
            }
        self.LoginVerfy = self._req(data=Data).get('result',False)
        self.base = {"method": "", "params": "", "auth": self.LoginVerfy}

    def verfylogin(Fn):
        def Test(self, *args, **kwargs):
            if not self.LoginVerfy:
                raise loginfail('login fail')
            return Fn(self, *args, **kwargs)

        return Test


    @verfylogin
    def get_host(self, *args, **kwargs):
        """
        get host list
        :param kwargs:
            :host:zabbix of hostname
            :info:Ture or False,default False
        :return:{}
        """
        if kwargs.get('info', False) is True:
            output = 'extend'
        else:
            output = ["hostid", "host", "status", "error"]
        self.base['params'] = {"output": output,"filter": {"host": kwargs.get('host', [])}}
        self.base['method'] = "host.get"
        return self._req(data=self.base)

    @verfylogin
    def get_groupid(self, *args, **kwargs):
        """
        get group list
        :param kwargs:
          :info:Ture of Flase,default False
        :return:[]
        """
        if kwargs.get('info', False) is True:
            output = ["groupid", "name"]
        else:
            output = 'extend'
        self.base['params'] = {"output": output}
        self.base['method'] = "hostgroup.get"
        return self._req(data=self.base)

    @verfylogin
    def items_search(self, *args, **kwargs):
        """
        with keyword search items
        :param kwargs:
            :info: default is True
            :hostids:zabbix client hostid
            :key:  search keyword
        :return:[]
        """
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["name", "itemids", "key_", "webitems"]
        self.base['method'] = "item.get"
        self.base['params'] = {"output": output,"hostids": kwargs.get('hostid', ''),"webitems": True,"search": {"key_": kwargs.get('key', '')},}
        return self._req(data=self.base)

    def _history_type(self,x):
        f = {'float': 0, 'character': 1, 'log': 2, 'numeric': 3, 'text': 4}
        end = f.get(x,False)
        if end is False:
            raise RaiseVlues("type must be in:%s" % f.keys())
        return end

    @verfylogin
    def get_history(self, *args, **kwargs):
        """
        get items history data
        :param kwargs:
            :itemids: items id
            :limit: data count,defualt is 10
            :type:  history data type,default is numeric
        :return:{}
        """
        self.base['method'] = "history.get"
        self.base['params'] = {
                "output": "extend",
                "history": self._history_type(kwargs.get('type', 'numeric')),
                "itemids": kwargs.get('itemsid', 1),
                "limit": kwargs.get('limit', 10)
            }
        return self._req(data=self.base)

# if __name__ == "__main__":
    # F = _zabbix(host='http://zabbix.migang.com',timeout=15)
    # F.login(user='admin',passwd='zabbix')
    # print F.get_host(info=True)            #获取所有hosts
    # print F.get_host(host='172.16.1.6',info=True) #获取某个host详细信息
    # print F.get_groupid(info=True)        #获取所有主机组ID,
    # print F.items_search(hostid='10105')   #查询所有tiesm
    # print F.items_search(hostid='10105',key="cpu")   #模糊过滤items
    # print F.get_history(
    #     itemsid=23754,  # 监控项目id
    #     limit=2,  # limit 获取监控的最后n个值
    #     type='numeric'
    # )   #获取items历史数据

#     print help(abc)
