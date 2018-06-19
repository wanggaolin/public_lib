### zabbix api document,support 2.x 3.x
#### 1.hosts
    print F.host_info(host_name='Dns2',debug=True)  # 获取所有主机监控详情,debug=True
    print F.host_get()                                    #获取所有hosts,info=False
    print F.host_get(host='172.16.1.7',info=True)         #获取某个host详细信息
    print F.host_id_exists(hostid=10105)                  #根据hostid查询hostsid是否存在
    print F.host_link_template(host_id=10122,templateid_list=['10001',10047])     #根据模板id,host添加模板
    print F.host_unlink_template(host_id=10122,templateid_list=['10001',10047])     #根据模板id,host删除模板
    print F.host_delete(hostid_list=[10119,10120])        #根据hostid删除监控主机
    print F.host_create(                              # 创建监控主机
        name='zabbix_test',       # 监控主机名,默认为监控主机ip
        ip='172.16.1.221',        # 监控主机ip
        groupid=8                 # 创建主机所在的组,默认为8
    )

#### 2.hosts interface
    print F.interface_get(hostid=10105)                       #根基host_id获取主机接口信息
    print F.interface_exists(hostid=10105,ip='172.16.1.6')    #根据ip,主机id判断主机接口是否存在
    print F.interface_create(                                 #创建主机监控接口
        hostid='10131',       #对应的主机id
        ip='172.16.1.221',    #监控机ip
        port='10050',         #监控机port
        type='agent',         #type=[agent/SNMP/IPMI/JMX]
    )

#### 3.hosts items
    print F.items_get(itemsid=24598)                  #获取items详情,包括:lastvalue,units
    print F.items_get(itemsid=24598,info=True)        #获取items全部详情
    print F.items_search(hostid='10122')              #查询所有tiesm
    print F.items_search(hostid='10105',key="gaolin") #模糊过滤items
    print F.items_exists(hostid=10105, key_='gaolin') #判断主机监控项是否存在
    print F.items_delete(itemslist=[24597,24591])     #删除监控项目,传递参数list
    print F.items_create(                             #创建主机监控项
        name='gaolin2',        #监控项名称
        key_='net.if.in[eth1]', #监控项key
        hostid='10131',       #对应的主机id
        update=60,            #数据获取频率,默认60s
        interfaceid=20,       #主机interfaceid 接口id
        history=60,           #数据保存多少天
        trends=90,            #趋势数据保存多少天
        units='',             #单位
        type='numeric',       # type = float/character/numeric/text[default=numeric]
        agent_type='Zabbix_agent' # Zabbix_agent/SNMPv1_agent/Zabbix_trapper/simple_check/SNMPv2_agent/Zabbix_internal/SNMPv3_agent/Zabbix_agent_(active)/Zabbix_aggregate/web_item/external_check/database_monitor/IPMI_agent/SSH_agent/TELNET_agent/calculated/JMX_agent/SNMP_trap
    )

#### 4.template
    print F.template_get()                            #获取所有template,info=Ture
    print F.template_get(name='t2')                   #查询某个template,info=Ture
    print F.template_name_exists(name='Template OS Linux')                #根据模板名称判断模板是否存在
    print F.template_delete(templateid_list=[10125,10127])                #根据模板id删除模板
    print F.template_create(                          #创建模板
        name='gaolin',                #模板名词
        groupid_list=[15,14],         #所属主机组
        hostid_list=[10122]           #那些主机增加该模板，非必须项
    )

#### 5.trigger
    print F.trigger_itemsid_get(itemids=24598)                #根据itemsid获取监控报警阀值
    print F.trigger_hostsid_get(hostid='10122')               #根据监控hostid获取所有主机中的监控报警阀值
    print F.trigger_delete(triggerid_list=[10010])            #根据griggerid删除trigger
    print F.trigger_create(                                   # 创建trigger
        name='gaolin_test2',  # trigger 名称
        expression='{zabbix_test:vm.memory.size[available].last()}<2',  # 触发条件表达式子,最后取值大于n
    )

#### 6.graph
    print F.graph_get(graphid_list=[848,849])                 #获取主机下的所有监控图表,info=Ture,返回详细信息
    print F.graph_delete(graphid_list=10105)                  #根据主机id和图表名词删除监控图表
    print F.graph_hostid_exists(name='a51',hostid='10105')    #根据主机id和图表名词，查询图表是否存在
    print F.graph_hostname_exists(name='a5',host_name='zabbix_test')  #根据主机id和图表名词，查询图表是否存在
    print F.graph_create(                                     #创建监控图表
            name='a6',                    #监控图表名称
            graphtype='default',          #图表类型 graphtype=[default/stacked/pie/exploded]
            gitems=[
                {                         #tiems 可以写多个,也可以写1个
                    'itemid':'24733',     #items id
                    'color':'C80000',     #图标颜色
                },{
                    'itemid': '24732',
                    'color': '00DD00',
                }
            ]
    )


#### 7.group
    print F.group_get(info=True)                              #获取所有主机组ID
    print F.group_get_name(name='Discovered hosts')           #根据主机组名称获取主机组信息
    print F.group_create(name='ggg')                          #创建主机组
    print F.group_exists(name='t1')                           #判断主机组是否存在
    print F.group_delete(groupid_list=['12','13'])            #删除主机组
    print F.group_host_add(group_id=14,host_id=[10105,10106]) #添加主机到主机组
    print F.group_host_remove(group_id=14,host_id=[10105,10107])   #从主机组中删除主机

#### 8.screen
    print F.screen_get()                                  #查询所有screen
    print F.screen_get(screenid=20)                       #根据screenid查询screen
    print F.screen_delete_id(screenid_list=[41,44])       #根据screenid删除screen
    print F.screen_delete_name(name='t2')                 #根据screen 名称删除screen
    print F.screen_create_host(hostid=10105,name='t21')   #根据hostid建立screen
    print F.screen_create(    # 创建screen
        name='test1',         # screen 名称
        hsize=2,              # 宽
        vsize=1,              # 高
        data=[772, 591, 594, 694, 697, 626]  # graph,图像id
    )



#### 9.hosts history
    print F.history_get(    #获取items历史数据
        itemsid=23754,  # 监控项目id
        limit=2,  # limit 获取监控的最后n个值
        type='numeric'  #监控数据类型
    )

#### 10.httptest
    print F.httptest_get()                            #查看所有监控,info=Trure
    print F.httptest_get(hostid=10122)                #根据hostid查看所有监控,info=Trure
    print F.httptest_id_get(httptest_id=21)           #根据httptestid查看某个监控,info=Trure
    print F.httptest_delete(httptestid_list=[15,16])  #根据httptestid删除httptest监控
    print F.httptest_create(                          #创建web监控
        name='gaolin10',              #监控名称
        hostid=10122,                 #host id
        url='http://172.16.1.221',    #监控地址,url
        status_codes='200,201',       #返回正常的http状态码,多个状态码用逗号间隔
    )
    