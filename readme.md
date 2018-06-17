### python 公共方法库,方便使用
#### install
    #centos:
        yum install rrdtool-devel
    #ubuntu:
        apt-get install librrd-dev
    cd /usr/local/src && git clone https://github.com/wanggaolin/public_lib.git && \
    cd public_lib && python setup.py install || cd public_lib/ && git pull && python setup.py  install

## 1系统模块    
#### 1.0.1 进度条
    import time
    F = public_lib.proging_rate(screen_max=1000,screen_name='1000M',rate_symbol='#')
    for i in range(1000):
        time.sleep(0.1)
        F.update("%sM" % i)
    F.end()
    
#### 1.0.2 漂亮的json        
    In [5]: print public_lib.json_data({'a':'你好'})
    {
        "a": "你好"
    }

#### 1.0.3 方便的time模块
    In [10]: public_lib.CurrTime()
    Out[10]: '2017-07-31 11:04:01'
    
    In [11]: public_lib.CurrDay()
    Out[11]: '2017-07-31'

#### 1.0.4 文件模块
    In [17]: public_lib.all_file('.')
    Out[17]: ['./+~JF1688623560254782582.tmp']

    In [7]: public_lib.dir_name('/a/b/')
    Out[7]: '/a/b'
        
#### 1.0.5 方便的网络模块
    In [6]: public_lib.telnet(ip='1.1.1.1',port=22,timeout=10)
    Out[6]: (False, socket.timeout('timed out'))
           
#### 1.0.6 输出带颜色字体
    In [3]: print public_lib.color('x')
    In [4]: print public_lib.color('x',name='green')    
    In [5]: print public_lib.color('x',number=35)
    
#### 1.0.7 隐藏文本字符替换为*
    In [2]: public_lib.hide_str('nihaoma',start=2,end=4) #隐藏字符
    Out[2]: 'ni**oma'
    
#### 1.0.8参数校验
    In [2]: public_lib.check_bank('6228480402564890018') #银行卡号检查
    Out[2]: True

    In [2]: public_lib.check_card(530826198410209673)   #身份证号检查
    Out[2]: True

    #rule规则列表
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
	
    #用法
        #rule:检查规则
        #data:检查对象,必须是字典    
    print public_lib.json_data(public_lib.check_req(data={"number":'a'}).rule(rule=
        {
            "number":{                #字典中对应key  
                "alias": "手机号",     #别名
                "number": True,       #规则
                "minlength":5,        #规则可以写多个
                "error":{
                        "number":"手机号格式错误"  #自定义错误内容,非必须
                }                  
            }
        }
    ))

    #返回
        {'status':False,'data':self.data,'msg':''}
            #status:验证成功失败,[true/false]
            #data:原验证的数据
            #msg:失败原因


#### 1.0.9　网络ping
    In [3]: public_lib.ping(ip='www.lssin.com')
    Out[3]: ping(status=True, min='3.407', avg='3.581', max='3.726', mdev='0.131', lost='0%', text='')
    
#### 1.1.0　随机获取use-agent
    In [8]: public_lib.user_agent()
    Out[8]: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (...'

#### 1.1.1　获取随机一个hashid或根据指定字符串返回一个id
    In [5]: public_lib.hash_id()
    Out[5]: '7580a0faf2b11cf149b6f74067a30a974c1eee71'
    
    In [6]: public_lib.hash_id('hello word')
    Out[6]: 'e0738b87e67bbfc9c5b77556665064446430e81c'

#### 1.1.2　获取随机一个hashid或根据指定字符串返回一个id
    In [8]: public_lib.md5_id()
    Out[8]: '9aba2e0c5be39d89842f0cf6ff12a7f5'
    
    In [9]: public_lib.md5_id('hello word')
    Out[9]: '13574ef0d58b50fab38ec841efe39df4'

#### 1.1.3　获取文件md5
    In [2]: public_lib.file_md5('/tmp/12')
    Out[2]: False
    
#### 1.1.4　将list切割成n等份
    In [2]: public_lib.list_cut(range(10),4)
    Out[2]: [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
       
#### 1.1.5　检查ip地址是否合法       
    In [5]: public_lib.check_ip('1.1.1.1222')
    Out[5]: False

#### 1.1.6　检查ip地址是私有地址
    In [6]: public_lib.check_ip_private('172.16.5.5')
    Out[6]: True

#### 1.1.７　获取系统版本
    In [5]: public_lib.uname()
    Out[5]: 'Ubuntu 14.04.3 LTS'

#### 1.1.8　检查文本是否包含特殊符号
    In [2]: public_lib.check_symbols('..')
    Out[2]: symbols(status=False, symbols='..')

#### 1.1.9　检查2个文件内容是否一致
    In [2]: public_lib.file_diff('/tmp/1','/tmp/2')
    Out[2]: False

#### 1.2.0　获取系统主机名
    In [2]: public_lib.host_name()
    Out[2]: 'GaoLin'

#### 1.2.1　获取系统所有ip
    In [2]: public_lib.host_ip()
    Out[2]:[{'eth0': '172.16.1.255'}, {'wlan0'

#### 1.2.1　获取list重复元素
    In [2]: public_lib.set_list([1,2,2,2])
    Out[2]: [2]

#### 1.2.2　获取网卡mac地址
    In [2]: network_mac('eth0')
    Out[2]: b8:70:f4:1d:fc:61

#### 1.2.3　字典根据key去重
    In [2]: set_dict(data={'a':1,'b':2},key=['b'])
    Out[2]: {'a': 1}

#### 1.2.4　缓冲数据到文件
    In [2]: @cache_file(time=5,file='/tmp/.zabbix.cpu.every.cache')

#### 1.2.5　弹出自定义error
    In [2]: raise RaiseVlues('xxx')

#### 1.2.6　html转text
    In [2]: public_lib.html_to_text("<p>没有分寸<br/>感</p>")
    Out[2]: HtmlToText(status=True, text=u'\u6ca1\u6709\u5206\u5bf8 \u611f ', error='')

#### 1.2.7　text转html
    In [2]: public_lib.text_to_html("""12 4""")
    Out[2]: TextToHtml(status=True, text="<!DO...../html>", error='')



## 2邮箱模块
#### 2.0.1　发送邮箱附件,支持多个文件
    print public_lib.send_file(
        smtp='smtp.xxxxx.com',
        user='alert@xxxxx.com',
        passwd='xxxxx',
        subject="test file",
        to_list=['brach@lssin.com'],
        file_list=['/tmp/123','/tmp/456']
    )
    
#### 2.0.2　发送邮箱
    print public_lib.send_mail(
        smtp='smtp.xxxxx.com',
        user='alert@xxxxx.com',
        passwd='xxxxx',
        subject="test mail",
        to_list=['brach@lssin.com'],
        text="hello word",
    )    

#### 2.0.3　解析邮件文本[/var/spool/mail/root]
    In [2]: a="""
       ...: From MAILER-DAEMON  Mon Aug 28 17:49:35 2017
       ...: ....
       ...: Message-Id: <20170828094935.B018E143019@source.localdomain>
       ...: Status: O
       ...: 
       ...: This is test mail.
       ...: """
    In [3]: print public_lib.mail_text(a.strip())
    Out[3]:{'Date': 'Mon, 28 Aug 2017 17:49:35 +0800 (CST)', 'text': 'This is a MIE....

## 3监控模块            
#### 3.0.1　根据某个进程名称获取对应的pid和使用的内存大小
    In [2]: public_lib.pid('java')
    Out[2]: pid(memory=1056864, pid=['6168'])
    
## 4日志模块
#### 4.0.1 记录日志到系统日志中[/var/log/message]
    public_lib.syslog.error("test log")  

## 5 excel模块
#### 5.0.1 将数据写入exlce中
    f = {
        'menu': [['name', '姓名', {'msg': '姓名', 'w': 16}],['number', '电话', {'msg': '电话', 'w': 6}]],
        'data': [
            {"name":"王高林","number":"1"},
            {"name":"王高林1"},
        ],
        'title': '学生登记表'
    }
    print public_lib.excel_write(**f).save('/tmp/1.xlsx')

#### 5.0.1 读取exlce数据
    menu = [['name','姓名'],['number','电话'],['id','班级']]
    d 6 public_lib.excel_read(menu=menu)
    d.x = 3
    d.y = 7
    print public_lib.json_data(d.file(file_path='/data/temp/download/资产主机.xlsx'))

## 6xmind 模块
#### 6.0.1 将xmind txt 数据导入到excel中
    F = public_lib.xmind(file='/home/gaolin/Desktop/安全防护.txt')
    print F.save_excel('/tmp/1.xlsx')

## 7rrdtool 模块
#### 7.0.1 根据传递的参数绘制图表
    F = public_lib.rrd()
    F.interval = 5
    F.units = 'G'
    F.y_desc = 'xxxxx'
    F.title = '测试图表'
    F.img = '1.png'
    l = {
        'time': ['1529206065', '1529206070', '1529206075', '1529206080', '1529206085'],
        'lable': [{'type': 'AREA', 'name': 'w1'}, {'name': 'w2'}],
        'w2': [81, 79, 60, 80, 78],
        'w1': [3, 24, 59, 11, 11]
    }
    print F.load(l)
![demo images](https://raw.githubusercontent.com/wanggaolin/public_lib/master/public_lib/img/1.png)
<div align=center><img width="650" height="300" src="https://raw.githubusercontent.com/wanggaolin/public_lib/master/public_lib/img/1.png"/></div>