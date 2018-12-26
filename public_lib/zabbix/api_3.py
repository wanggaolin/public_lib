#!/usr/bin/env python
#encoding=utf-8
import requests
import json
import threading
import sys


class RaiseVlues(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class _zabbix(object):
    'require:zabbix version 2.2'
    def __init__(self,*args,**kwargs):
        'request: `host` `timeout=20` '
        self.host = kwargs.get('host','127.0.0.1')
        self.timeout = kwargs.get('timeout',20)
        self.LoginVerfy = False
        self.base = {}
        self.zabbix_agent = {'Zabbix_trapper': '2', 'Zabbix_agent_(active)': '7', 'JMX_agent': '16', 'IPMI_agent': '12', 'database_monitor': '11', 'web_item': '9', 'Zabbix_agent': '0', 'SNMPv3_agent': '6', 'SSH_agent': '13', 'TELNET_agent': '14', 'external_check': '10', 'SNMP_trap.': '17', 'simple_check': '3', 'SNMPv1_agent': '1', 'Zabbix_internal': '5', 'Zabbix_aggregate': '8', 'calculated': '15', 'SNMPv2_agent': '4'}
        self.data_type = {'float': 0, 'character': 1, 'log': 2, 'numeric': 3, 'text': 4}
        self.graph_type = {'default': 0, 'stacked': 1, 'pie': 2, 'exploded': 3}

    def json_data(self,x):
        return json.dumps(x, indent=4, ensure_ascii=False)

    def _req(self,*args,**kwargs):
        DefaultHead = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.13381.9 Safari/537.36 zabbix_api'}
        data = kwargs['data']
        data["jsonrpc"] = "2.0"
        data["id"] = "1"
        # print self.json_data(data)
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
            "jsonrpc": "2.0","method": "user.login","id": 1,
            "params": {"user": kwargs.get('user','admin'),"password": kwargs.get('passwd','zabbix')},

        }
        self.LoginVerfy = self._req(data=Data).get('result',False)
        self.base = {"method": "", "params": "", "auth": self.LoginVerfy}

    def verfylogin(Fn):
        def Test(self, *args, **kwargs):
            if not self.LoginVerfy:
                raise RaiseVlues('login fail')
            return Fn(self, *args, **kwargs)
        return Test

    def verfy_graph_type(Fn):
        'check graph type'
        def Test(self, *args, **kwargs):
            graphtype = kwargs.get('graphtype','')
            if graphtype in self.graph_type.keys():
                return Fn(self, *args, **kwargs)
            else:
                raise ValueError('graph_type must be in:%s' % '/'.join(self.graph_type.keys()))
        return Test

    def verfy_agent_type(Fn):
        'check monitor agent type'
        def Test(self, *args, **kwargs):
            agent_type = kwargs.get('agent_type','')
            if agent_type in self.zabbix_agent.keys():
                return Fn(self, *args, **kwargs)
            else:
                raise ValueError('agent_type must be in:%s' % '/'.join(self.zabbix_agent.keys()))
        return Test

    def verfy_data_type(Fn):
        'check monitor data value of type'
        def Test(self, *args, **kwargs):
            Type = kwargs.get('type','')
            if Type in self.data_type.keys():
                return Fn(self, *args, **kwargs)
            else:
                raise ValueError('data type must be in:%s' % '/'.join(self.data_type.keys()))
        return Test

    def list_to_list(self,**kwargs):
        """
        :param kwargs:(data=[1,2],key='hostid2')
        :return:[{'hostid2': 1}, {'hostid2': 2}]
        """
        host_list = []
        for i in kwargs['data']:
            host_list.append({kwargs['key']: i})
        return host_list

    @verfylogin
    def host_get(self, *args, **kwargs):
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
        self.base['params'] = {"output": output,"filter": {"host": kwargs.get('host')}}
        self.base['method'] = "host.get"
        return self._req(data=self.base)

    @verfylogin
    def host_id_exists(self, *args, **kwargs):
        """
        with hostid verfy host is true ir false
        :param kwargs:
            hostid: host id
        """
        self.base['params'] = {"output": ["hostid"],"hostids":kwargs['hostid']}
        self.base['method'] = "host.get"
        return self._req(data=self.base)

    @verfylogin
    def host_create(self,*args,**kwargs):
        """
        create host monitor
        :param kwargs:
            :ip : ip addres
            :name : host name
            :groups : group id ,defualt=8
        :return:
        """
        Ipaddres = kwargs['ip']
        self.base['method'] = "host.create"
        self.base['params'] = {
            "host": kwargs.get('name',Ipaddres),
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": Ipaddres,
                "dns": "",
                "port": "10050"
            }],
            "groups": [{"groupid": kwargs.get('groupid',8)}
            ],
        }
        return self._req(data=self.base)

    @verfylogin
    def host_delete(self,*args,**kwargs):
        """
        with host id delte monitor of host
        :param kwargs:
            :hostid_list : [hostid1,hostid2]
        :return:
        """
        self.base['method'] = "host.delete"
        self.base['params'] = kwargs['hostid_list']
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
            output = ["name", "itemids", "description", "webitems","key_","units","error"]
        self.base['method'] = "item.get"
        self.base['params'] = {"output": output,"hostids": kwargs['hostid'],"webitems": True,"search": {"key_": kwargs.get('key', '')},}
        return self._req(data=self.base)

    @verfylogin
    def items_get(self, *args, **kwargs):
        """
        get items info
        :param kwargs:
            :info: default is True
            :itemsid:zabbix monitor of itemsid
        :return:[]
        """
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["name", "itemids", "description", "webitems","key_","units","error"]
        self.base['method'] = "item.get"
        self.base['params'] = {"output": output,"itemids":kwargs['itemsid']}
        return self._req(data=self.base)

    @verfylogin
    def items_exists(self, *args, **kwargs):
        """
        show items exists of hosts
        :param kwargs:
            key_ : items key name
            hostid : host id
        :return:
        """
        self.base['method'] = "item.get"
        self.base['params'] = self.base['params'] = {"output": "itemid","hostids": kwargs['hostid'],"search": {"key_": kwargs.get('key', '')},}
        return self._req(data=self.base)

    @verfylogin
    def items_delete(self, *args, **kwargs):
        self.base['method'] = "item.delete"
        self.base['params'] = kwargs['itemslist']
        return self._req(data=self.base)

    @verfylogin
    @verfy_agent_type
    @verfy_data_type
    def items_create(self, *args, **kwargs):
        """
        create items on host
        :param kwargs:
            name : items monitor name
            key_ : items key name
            hostid : host id
            type : datay of type,defualt=numeric,choice=self.data_type.keys()
            value_type : agent monitor type,default=Zabbix_agent,chice=self.zabbix_agent.keys()
            interfaceid : host interface id,default=1
            history : data save of day,default = 60day
            update : get client data of time,defualt=60s
            trends : change data save of day,defualt = 60day
            units : monitor unit,default=''
            formula : return day,default =1
        :return:
        """
        Type = kwargs.get('type', 'numeric')
        AgentType = kwargs.get('agent_type', 'Zabbix_agent')
        self.base['method'] = "item.create"
        self.base['params'] = {
            "name": kwargs['name'],
            "key_": kwargs['key_'],
            "hostid": kwargs['hostid'],
            "type": self.zabbix_agent.get(AgentType),
            "value_type": self.data_type.get(Type),
            "interfaceid": kwargs['interfaceid'],
            "delay": kwargs.get('update',30),
            "history":kwargs.get('history', 60)*60*60,
            "trends":kwargs.get('trends', 90)*60*60,
            "units":kwargs.get('units', ''),
            "formula":kwargs.get('formula', 1),
        }
        return self._req(data=self.base)

    @verfylogin
    @verfy_data_type
    def history_get(self, *args, **kwargs):
        """
        get items history data
        :param kwargs:
            :itemids: items id
            :limit: data count,defualt is 10
            :type:  history data type,default is numeric
        """
        self.base['method'] = "history.get"
        self.base['params'] = {
                "output": "extend",
                "history": self.data_type[kwargs['type']],
                "itemids": kwargs.get('itemsid', 1),
                "limit": kwargs.get('limit', 10)
        }
        return self._req(data=self.base)

    @verfylogin
    def interface_get(self,*args,**kwargs):
        """
        with hostid get host interfaceid
        :param kwargs:
            hostid: host id
        """
        self.base['method'] = "hostinterface.get"
        self.base['params'] = {"output": "extend", "hostids": kwargs['hostid']}
        return self._req(data=self.base)

    @verfylogin
    def interface_create(self, *args, **kwargs):
        InterfaceType = {'agent':1,'SNMP':2,'IPMI':3,"JMX":4}
        Interface = kwargs.get('type', 'agent')
        if Interface not in InterfaceType.keys():
            raise ValueError("monitor type must in is:%s" % '/'.join(InterfaceType.keys()))
        self.base['method'] = "hostinterface.create"
        self.base['params'] = {
            "hostid": kwargs['hostid'],
            "dns": "",
            "ip": kwargs['ip'],
            "main": 0,
            "port": kwargs.get('port','10050'),
            "type": InterfaceType[Interface],
            "useip": 1
        }
        return self._req(data=self.base)

    @verfylogin
    def interface_exists(self,*args,**kwargs):
        """
        check host interface id exists
        :param kwargs:
            hostids: host id
        :return:
        """
        self.base['method'] = "hostinterface.get"
        self.base['params'] = {"output": "interfaceid", "hostids": kwargs['hostid']}
        return self._req(data=self.base)

    @verfylogin
    def screen_get(self, *args, **kwargs):
        """
        show screen list
        :param kwargs:
            screenid: screen id
        :return:
        """
        if kwargs.get('info', True) is True:
            self.base['params'] = {"output": "extend","selectScreenItems": "extend"}
        else:
            self.base['params'] = {"output": ["name","hsize","vsize"]}
        self.base['method'] = "screen.get"
        if kwargs.get('screenid',False):
            self.base['params']['screenids'] = kwargs['screenid']
        return self._req(data=self.base)

    @verfylogin
    def screen_create(self, *args, **kwargs):
        Dict = []
        data = kwargs.get('data',[])
        hsize = int(kwargs.get('hsize',2))
        vsize = int(kwargs.get('vsize',20))
        x = y = 0
        for info in data:
            Dict.append({
                    "resourcetype": 0,
                    "resourceid":info,
                    "rowspan": 1,
                    "colspan": 1,
                    "x": x,
                    "y": y, #图标在screen中的坐标
                    "width":500,
                    "height":100,#图表宽,高
            })
            x += 1
            if x == hsize:y+=1
            if x >= hsize:x=0
        Vsizey = (vsize / hsize) + (vsize % hsize)
        if Vsizey < y:vsize=y+1
        self.base['method'] = "screen.create"
        self.base['params'] = {
            "name": kwargs['name'],
            "hsize": hsize,
            "vsize": vsize,
            "screenitems": Dict
        }
        # import public_lib
        # print public_lib.json_data(Dict)
        return self._req(data=self.base)

    @verfylogin
    def screen_create_host(self, *args, **kwargs):
        """
        select host all grapg create screen
        :param kwargs:
            hostid: host id
            name: screen name
        """
        hostid = kwargs['hostid']
        if self.host_id_exists(hostid=hostid).get('result',False):
            return self.screen_create(
                name=kwargs.get('name'), hsize=2,  vsize=1,
                data=[int(i['graphid']) for i in sorted(self.graph_get(hostid=hostid)['result'],key=lambda x:x['name'])]
            )
        else:
            raise RaiseVlues('invalid hostid:%s' % hostid)

    @verfylogin
    def graph_get(self, *args, **kwargs):
        """
        with hostid get graph info
        :param kwargs:
            hostid: host id
            info : if info is Ture,reutrn all info,defualt=False
        :return:
        """
        self.base['method'] = "graph.get"
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["name"]
        self.base['params'] = {"output": output,"hostids": kwargs['hostid']}
        return self._req(data=self.base)

    @verfylogin
    def screen_delete_id(self, *args, **kwargs):
        """
        with screenid delete screen
        :param kwargs:
            screenid: [screenid,screenid]
        :return:
        """
        self.base['method'] = "screen.delete"
        self.base['params'] = kwargs['screenid_list']
        return self._req(data=self.base)

    @verfylogin
    def screen_delete_name(self, *args, **kwargs):
        """
        with screen name delete screen
        :param kwargs:
            screenid: [screenid,screenid]
        :return:
        """
        screen_name = kwargs.get('name')
        screen_id = False
        for i in self.screen_get(info=False)['result']:
            if i['name'] == screen_name:
                screen_id = i['screenid']
                break
        if screen_id is False:
            raise RaiseVlues("screen name %s not exists" % screen_name)
        else:
            self.base['method'] = "screen.delete"
            self.base['params'] = [screen_id]
            return self._req(data=self.base)

    @verfylogin
    def group_create(self, *args, **kwargs):
        """
        create monitor group
        :param kwargs:
          :name :host group name
        :return:[]
        """
        self.base['params'] = {"name": kwargs['name']}
        self.base['method'] = "hostgroup.create"
        return self._req(data=self.base)

    @verfylogin
    def group_exists(self, *args, **kwargs):
        """
        show  monitor group is exists
        :param kwargs:
          :name :host group name
        :return:[]
        """
        self.base['params'] = {"output": ["name"], "filter": {"name":kwargs["name"]}}
        self.base['method'] = "hostgroup.get"
        return self._req(data=self.base)

    @verfylogin
    def group_delete(self, *args, **kwargs):
        """
        delete host group
        :param kwargs:
          :groupid_list:host group id
        :return:[]
        """
        self.base['params'] = kwargs['groupid_list']
        self.base['method'] = "hostgroup.delete"
        return self._req(data=self.base)

    @verfylogin
    def group_host_add(self, *args, **kwargs):
        """
        add host to group
        :param kwargs:
          :host_id: [host_id1,host_id2]
          :group_id: host group id
        :return:[]
        """
        self.base['params'] = {
            "groups": [{"groupid": kwargs['group_id']}],
            "hosts": self.list_to_list(data=kwargs.get('host_id',[]),key="hostid")
        }
        self.base['method'] = "hostgroup.massadd"
        return self._req(data=self.base)

    @verfylogin
    def group_host_remove(self, *args, **kwargs):
        """
        remove host to group
        :param kwargs:
          :host_id: [host_id1,host_id2]
          :group_id: host group id
        :return:[]
        """
        self.base['params'] = {"groupids": [kwargs['group_id']],"hostids": kwargs['host_id']}
        self.base['method'] = "hostgroup.massremove"
        return self._req(data=self.base)

    @verfylogin
    def group_get(self, *args, **kwargs):
        """
        get group list
        :param kwargs:
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
    def group_get_name(self, *args, **kwargs):
        """
        with group name show group info
        :param kwargs:
          :name ： host group name
        :return:[]
        """
        self.base['params'] = {"output": "extend","filter": {"name": [kwargs['name']]}}
        self.base['method'] = "hostgroup.get"
        return self._req(data=self.base)

    @verfy_graph_type
    @verfylogin
    def graph_create(self, *args, **kwargs):
        """
        create graph photo
        :param kwargs:
            :name : graph photo name
            :gitems : monitor items id and items color
            :graphtype : graph photo type
        :return:
        """
        graphtype = self.graph_type[kwargs.get('graphtype', 'default')]
        self.base['params'] = {
                "name": kwargs['name'],
                "width": 900,
                "height": 200,
                "gitems":kwargs.get('gitems',[]),
                "graphtype":graphtype,
            }
        self.base['method'] = "graph.create"
        return self._req(data=self.base)

    @verfylogin
    def graph_delete(self, *args, **kwargs):
        """
        delete graph photo
        :param kwargs:
          :graphid_list:graph photo id
        :return:[]
        """
        self.base['params'] = kwargs['graphid_list']
        self.base['method'] = "graph.delete"
        return self._req(data=self.base)

    @verfylogin
    def graph_hostid_exists(self, *args, **kwargs):
        """
        with hostid,grpah name verfy photo is true ir false
        :param kwargs:
            :name: graph photo name
            :hostid: monitor host id
        """
        self.base['method'] = "graph.get"
        self.base['params'] = {"name": kwargs['name'],"hostids": kwargs['hostid'],"output":["graphid","name"]}
        return self._req(data=self.base)

    @verfylogin
    def graph_hostname_exists(self, *args, **kwargs):
        """
        with host name,grpah name verfy photo is true ir false
        :param kwargs:
            :name: graph photo name
            :host_name: monitor host name
        """
        self.base['method'] = "graph.get"
        self.base['params'] = {"name": kwargs['name'],"host": kwargs['host_name'],"output":["graphid","name"]}
        return self._req(data=self.base)

    @verfylogin
    def trigger_create(self, *args, **kwargs):
        """
        create monitor itmes of trigger
        :param kwargs:
            :name: tirger name
            :expression: means of expression
        :return:
        """
        self.base['method'] = "trigger.create"
        self.base['params'] = {
            "description": kwargs['name'],
            "priority": 5,
            "expression":kwargs['expression'],
            "type":1
        }
        return self._req(data=self.base)

    @verfylogin
    def trigger_itemsid_get(self, *args, **kwargs):
        """
        with items id get trigger info
        :param kwargs:
            :itemids: items id
            :altogether_express: hide means of expression,default=False
        :return:
        """
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["name","status","expression","description"]
        self.base['method'] = "trigger.get"
        self.base['params'] = {"output": output,"itemids": kwargs['itemids']}
        if kwargs.get('altogether_express') is True:
            self.base['params']['expandExpression'] = 'extend'
        return self._req(data=self.base)

    @verfylogin
    def trigger_hostsid_get(self, *args, **kwargs):
        """
        with hostid get all trigger info
        :param kwargs:
            :hostids: hostd id
            :items_info: print itemsid to end,default='',chico=['extend','']
        :return:
        """
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["name","status","expression","description","functions"]
        self.base['method'] = "trigger.get"
        self.base['params'] = {"output": output,"hostids": kwargs['hostid'],"selectFunctions": kwargs.get('items_info','')}
        return self._req(data=self.base)

    @verfylogin
    def trigger_delete(self, *args, **kwargs):
        """
        delete items of trigger
        :param kwargs:
          :triggerid_list:[trigger_id1,trigger_id2]
        :return:[]
        """
        self.base['params'] = kwargs['triggerid_list']
        self.base['method'] = "trigger.delete"
        return self._req(data=self.base)

    @verfylogin
    def template_get(self, *args, **kwargs):
        """
        get template list
        :param kwargs:
            :info: show all template,defualt=False
            :name: template name,default=False
        :return:[]
        """
        if kwargs.get('info', False) is True:
            output = ["name","templateid","error"]
        else:
            output = 'extend'
        self.base['params'] = {"output": output}
        if kwargs.get('name',False):
            self.base['params']['filter'] = {"host":[kwargs['name']]}
        self.base['method'] = "template.get"
        return self._req(data=self.base)

    @verfylogin
    def template_name_exists(self, *args, **kwargs):
        """
        with template name verfy template is true ir false
        :param kwargs:
            :name: template name
        """
        self.base['method'] = "template.get"
        self.base['params'] = {"output": ["name","templateid"],"filter":{"name":kwargs["name"]}}
        return self._req(data=self.base)

    @verfylogin
    def template_create(self, *args, **kwargs):
        """
        create template
        :param kwargs:
            :name: template name
            :group_id: group id
            :hostid_list: host id
            :expression: means of expression
        :return:
        """
        self.base['method'] = "template.create"
        self.base['params'] = {
            "host": kwargs['name'],
            "groups":{"groupid":kwargs['group_id']},
            "hosts":self.list_to_list(data=kwargs.get('hostid_list',[]),key="hostid"),
        }
        return self._req(data=self.base)

    @verfylogin
    def template_delete(self, *args, **kwargs):
        """
        delete items of trigger
        :param kwargs:
          :templateid_list:[template_id1,template_id2]
        :return:[]
        """
        self.base['params'] = kwargs['templateid_list']
        self.base['method'] = "template.delete"
        return self._req(data=self.base)

    @verfylogin
    def host_link_template(self, *args, **kwargs):
        """
        host link template
        :param kwargs:
          :templateid_list:[template_id,template_id]
          :host_id: host id
        :return:[]
        """
        self.base['method'] = "template.massadd"
        self.base['params'] = {
            "templates": self.list_to_list(data=kwargs['templateid_list'],key="templateid"),
            "hosts": [kwargs['host_id']]
        }
        return self._req(data=self.base)

    @verfylogin
    def httptest_create(self, *args, **kwargs):
        """
        create monitor of web
        :param kwargs:
            :hostid: host id
            :name: monitor name
            :url: monitor http url
            :agent: http agent
            :status_codes: access of url,return http code
            :auth_basic: enable basic HTTP authentication,default=False
            :user: basic HTTP authentication of login user
            :password: basic HTTP authentication of login password
            :timeout: access url of timeout,default=15
        :return:
        """
        self.base['method'] = "httptest.create"
        self.base['params'] = {
            "name": kwargs['name'],
            "hostid": kwargs['hostid'],
            "agent": kwargs.get('agent','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko, monitor httptest of zabbix'),
            "steps": [
                {
                    "name": kwargs['name'],
                    "url": kwargs['url'],
                    "timeout": kwargs.get('timeout',10),
                    "status_codes": kwargs.get('status_codes',200),
                    "no": 1
                }
            ]
        }
        if kwargs.get('auth_basic') is True:
            self.base['params']['authentication'] = 1
            self.base['params']['http_user'] = kwargs.get('user','user')
            self.base['params']['http_password'] = kwargs.get('password','')
        return self._req(data=self.base)

    @verfylogin
    def httptest_get(self, *args, **kwargs):
        """
        get httptest list
        :param kwargs:
            :hostid: show all httptest in host id
        :return:[]
        """
        if kwargs.get('info', None) is True:
            output = 'extend'
        else:
            output = ["httptestid","name","status","agent"]
        self.base['params'] = {
            "output": output,
            "selectSteps": "extend",
            "hostid":kwargs.get("hostid","")
        }
        self.base['method'] = "httptest.get"
        return self._req(data=self.base)

    @verfylogin
    def httptest_id_get(self, *args, **kwargs):
        """
        with httptest_id get info
        :param kwargs:
            :httptest_id: httptest id
        :return:[]
        """
        self.base['params'] = {
            "output": 'extend',
            "selectSteps": "extend",
            "httptestids":kwargs['httptest_id']
        }
        self.base['method'] = "httptest.get"
        return self._req(data=self.base)

    @verfylogin
    def httptest_delete(self, *args, **kwargs):
        """
        delete httptest monitor
        :param kwargs:
          :httptestid_list:[httptest_id1,httptest_id2]
        :return:[]
        """
        self.base['params'] = kwargs['httptestid_list']
        self.base['method'] = "httptest.delete"
        return self._req(data=self.base)

    @verfylogin
    def host_unlink_template(self, *args, **kwargs):
        """
        host unlink template
        :param kwargs:
          :templateid_list:[template_id,template_id]
          :host_id: host id
        :return:[]
        """
        self.base['method'] = "template.massremove"
        self.base['params'] = {"templateids": kwargs['templateid_list'],"hostids": kwargs['host_id']}
        return self._req(data=self.base)

    def _host_info_thread(self,**kwargs):
        f = _zabbix()
        f.host = self.host
        f.base = self.base
        f.LoginVerfy = self.LoginVerfy
        return f.trigger_itemsid_get(itemids=kwargs['itemid'], altogether_express=True)

    def host_info(self,**kwargs):
        """
        get host montor info,inclued:items,graph,triger
        :param kwargs:
            :host_name: host name
            :debug: return json data,default=False
        :return:
        """

        data_list = []
        host_info = self.host_get(host=kwargs.get('host_name',''))
        if not host_info['result']:
            raise  ValueError("%s not find" % kwargs['host_name'])
        else:
            for host in host_info['result']:
                data_dict = {}
                items_data = []
                items_info = self.items_search(hostid=host['hostid'])
                for items in items_info['result']:
                    triger_info = self.trigger_itemsid_get(itemids=items['itemid'],altogether_express=True)
                    # triger_info = self._host_info_thread(itemid=items['itemid'])
                    if triger_info['result']:
                        triger_data = []
                        for triger_nei in triger_info['result']:
                            triger_data.append({
                                "triggerid":triger_nei['triggerid'],
                                "expression":triger_nei['expression'],
                                "name":triger_nei['description'],
                            })
                        items['trigger'] = triger_data
                    items_data.append(items)
                data_dict["host_name"] = host['host']
                data_dict["host_id"] = host['hostid']
                data_dict["items"] = items_data
                data_list.append(data_dict)
        if kwargs.get('debug') is True:
            import public_lib
            return json.dumps(data_list, indent=4, ensure_ascii=False)
        return data_list



if __name__ == "__main__":
    F = _zabbix(host='http://zabbix.migang.com',timeout=15)
    F.login(user='admin',passwd='4c7c0022cb1d20')
    F.timeout = 30                      #请求超时时间

    # print F.httptest_get()                            #查看所有监控,info=Trure
    # print F.httptest_get(hostid=10270)                #根据hostid查看所有监控,info=Trure
    # print F.httptest_id_get(httptest_id=1)            #根据httptestid查看某个监控,info=Trure
    # print F.httptest_delete(httptestid_list=[15,16])  #根据httptestid删除httptest监控
    # print F.httptest_create(                          #创建web监控
    #     name='gaolin10',              #监控名称
    #     hostid=10270,                 #host id
    #     url='http://172.16.1.6',      #监控地址,url
    #     status_codes='200',           #返回正常的http状态码,多个状态码用逗号间隔
    # )


    # print F.template_get()                            #获取所有template,info=Ture
    # print F.template_get(name='gaolin1')              #查询某个template,info=Ture
    # print F.template_name_exists(name='gaolin')       #根据模板名称判断模板是否存在
    # print F.template_delete(templateid_list=[10271])  #根据模板id删除模板
    # print F.template_create(                          #创建模板
    #     name='gaolin1',                #模板名词
    #     group_id=14,                  #所属主机组
    #     hostid_list=[10270]           #那些主机增加该模板，非必须项
    # )


    # print F.trigger_itemsid_get(itemids=31001)                #根据itemsid获取监控报警阀值
    # print F.trigger_hostsid_get(hostid='10270')               #根据监控hostid获取所有主机中的监控报警阀值
    # print F.trigger_delete(triggerid_list=[16256])            #根据griggerid删除trigger
    # print F.trigger_create(                                   # 创建trigger
    #     name='gaolin_test2',  # trigger 名称
    #     expression='{zabbix_test:system.cpu.util[,user].last()}>2',  # 触发条件表达式子,最后取值大于n
    # )

    # print F.graph_get(hostid=10270)                           #获取主机下的所有监控图表,info=Ture,返回详细信息
    # print F.graph_delete(graphid_list=[1463])                 #根据主机id和图表名词删除监控图表
    # print F.graph_hostid_exists(name='a6',hostid='10270')     #根据主机id和图表名词，查询图表是否存在
    # print F.graph_hostname_exists(name='a5',host_name='zabbix_test')  #根据主机id和图表名词，查询图表是否存在
    # print F.graph_create(                                     #创建监控图表
    #         name='a6',                    #监控图表名称
    #         graphtype='default',          #图表类型 graphtype=[default/stacked/pie/exploded]
    #         gitems=[
    #             {                         #tiems 可以写多个,也可以写1个
    #                 'itemid':'31002',     #items id
    #                 'color':'C80000',     #图标颜色
    #             },{
    #                 'itemid': '31001',
    #                 'color': '00DD00',
    #             }
    #         ]
    # )

    # print F.host_info(host_name='Dns1',debug=True)        # 获取所有主机监控详情,debug=True
    # print F.host_get()                                    #获取所有hosts,info=False
    # print F.host_get(host='Dns1',info=True)               #获取某个host详细信息
    # print F.host_id_exists(hostid=10254)                  #根据hostid查询hostsid是否存在
    # print F.host_link_template(host_id=10269,templateid_list=['10001',10047])     #根据模板id,host添加模板
    # print F.host_unlink_template(host_id=10269,templateid_list=['10001',10047])     #根据模板id,host删除模板
    # print F.host_delete(hostid_list=[10119,10120])        #根据hostid删除监控主机
    # print F.host_create(                              #    创建监控主机
    #     name='zabbix_test',       # 监控主机名,默认为监控主机ip
    #     ip='172.16.1.42',         # 监控主机ip
    #     groupid=8                 # 创建主机所在的组,默认为8
    # )


    # print F.group_get(info=True)                              #获取所有主机组ID
    # print F.group_get_name(name='Discovered hosts')           #根据主机组名称获取主机组信息
    # print F.group_create(name='ggg')                          #创建主机组
    # print F.group_exists(name='ggg')                          #判断主机组是否存在
    # print F.group_delete(groupid_list=[15,16])                #删除主机组
    # print F.group_host_add(group_id=16,host_id=[10105,10106]) #添加主机到主机组
    # print F.group_host_remove(group_id=16,host_id=[10105,10107])   #从主机组中删除主机


    # print F.screen_get()                                  #查询所有screen
    # print F.screen_get(screenid=33)                       #根据screenid查询screen
    # print F.screen_delete_id(screenid_list=[22,23])       #根据screenid删除screen
    # print F.screen_delete_name(name='log_server')         #根据screen 名称删除screen
    # print F.screen_create_host(hostid=10254,name='t21')   #根据hostid建立screen
    # print F.screen_create(    # 创建screen
    #     name='test2',         # screen 名称
    #     hsize=2,              # 宽
    #     vsize=1,              # 高
    #     data=[792, 793, 794, 796, 795]  # graph,图像id
    # )


    # print F.interface_get(hostid=10270)                   #根基host_id获取主机接口信息
    # print F.interface_exists(hostid=10270)                #根据ip,主机id判断主机接口是否存在
    # print F.interface_create(                             #创建主机监控接口
    #     hostid='10270',       #对应的主机id
    #     ip='172.16.1.42',    #监控机ip
    #     port='10050',         #监控机port
    #     type='agent',         #type=[agent/SNMP/IPMI/JMX]
    # )


    # print F.items_get(itemsid=30998)                  #获取items详情,包括:lastvalue,units
    # print F.items_get(itemsid=30998,info=True)        #获取items全部详情
    # print F.items_search(hostid='10270')              #查询所有tiesm
    # print F.items_search(hostid='10270',key="system") #模糊过滤items

    # print F.items_exists(hostid=10270, key_='gaolin') #判断主机监控项是否存在
    # print F.items_delete(itemslist=[30997,30998])     #删除监控项目,传递参数list
    # print F.items_create(                             #创建主机监控项
    #     name='gaolin1',        #监控项名称
    #     key_='system.cpu.util[,user]', #监控项key
    #     hostid='10270',       #对应的主机id
    #     update=30,            #数据获取频率,默认30s
    #     interfaceid=11,       #主机interfaceid 接口id
    #     history=90,           #数据保存多少天
    #     trends=90,            #趋势数据保存多少天
    #     units='',             #单位
    #     type='float',       # type = float/character/numeric/text[default=numeric]
    #     agent_type='Zabbix_agent' # Zabbix_agent/SNMPv1_agent/Zabbix_trapper/simple_check/SNMPv2_agent/Zabbix_internal/SNMPv3_agent/Zabbix_agent_(active)/Zabbix_aggregate/web_item/external_check/database_monitor/IPMI_agent/SSH_agent/TELNET_agent/calculated/JMX_agent/SNMP_trap
    # )

    # print F.history_get(      #获取items历史数据
    #     itemsid=31001,# 监控项目id
    #     limit=2,      # limit 获取监控的最后n个值
    #     type='float'  #监控数据类型,数据类型必须正确，否则返回空
    # )

    #https://www.zabbix.com/documentation/3.4/manual/api/reference/screen/object#screen