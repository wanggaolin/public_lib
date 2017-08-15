###python ???????,????
####install    
    cd /usr/local/src && git clone https://github.com/wanggaolin/public_lib.git && \
    cd public_lib && python setup.py install || cd public_lib/ && git pull && python setup.py  install

##1????    
####1.0.1 ???
        import time
        F = public_lib.proging_rate(screen_max=1000,screen_name='1000M',rate_symbol='#')
        for i in range(1000):
            time.sleep(0.1)
            F.update("%sM" % i)
        F.end()
    

####1.0.2 ???json    

    In [4]: print public_lib.json_data({'a':'??'},indent=8)
    {
            "a": "??"
    }
    
    In [5]: print public_lib.json_data({'a':'??'})
    {
        "a": "??"
    }
    
    In [6]: 


####1.0.3 ???time??

    In [10]: public_lib.CurrTime()
    Out[10]: '2017-07-31 11:04:01'
    
    In [11]: public_lib.CurrDay()
    Out[11]: '2017-07-31'


####1.0.4 ???????

    In [17]: public_lib.all_file('.')
    Out[17]: ['./+~JF1688623560254782582.tmp']

    In [7]: public_lib.dir_name('/a/b')
    Out[7]: '/a/b'
        
####1.0.5 ???????
    In [6]: public_lib.telnet(ip='1.1.1.1',port=22,timeout=10)
    Out[6]: (False, socket.timeout('timed out'))
           

####1.0.6 ???????
    In [3]: print public_lib.color('x')
    x
    
    In [4]: print public_lib.color('x',name='green')
    x
    
    In [5]: print public_lib.color('x',number=35)
    x
    
####1.0.7 ?????????*
    In [2]: public_lib.hide_str('nihaoma',start=2,end=4) #????
    Out[2]: 'ni**oma'
    
    
####1.0.8????
    In [2]: public_lib.bank_check('6228480402564890018')
    Out[2]: True

    In [2]: public_lib.card_check(530826198410209673)
    Out[2]: True

    #rule????
    number:True     ?????[???/??/??]
    number_str:True ?????????
    time_day:true	????????????ISO?????2009-06-23/1998/01/22??????????????
    minlength:10	??????? 10 ??????????????
    maxlength:5	    ??????? 5 ??????????????
    rangelength:[5,10]	???????? 5 ? 10 ????????????????
	max:5	        ????????? 5?
	min:10	        ????????? 10?

    #??
    print public_lib.json_data(public_lib.req_check(data={"number":'a'}).rule(rule=
        {
            "number":{
                "alias": "???",     #??
                "number": True        #??
                }
        }
    ))
    rule:????
    data:????,???????

    #??
        {'status':False,'data':self.data,'msg':''}
            #status:??????,[true/false]
            #data:??????
            #msg:????

####1.0.??????use-agent
    In [8]: public_lib.user_agent()
    Out[8]: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'

####1.0.????????hashid????????????id
    In [5]: public_lib.hash_id()
    Out[5]: '7580a0faf2b11cf149b6f74067a30a974c1eee71'
    
    In [6]: public_lib.hash_id('hello word')
    Out[6]: 'e0738b87e67bbfc9c5b77556665064446430e81c'

####1.1.0???????hashid????????????id
    In [8]: public_lib.md5_id()
    Out[8]: '9aba2e0c5be39d89842f0cf6ff12a7f5'
    
    In [9]: public_lib.md5_id('hello word')
    Out[9]: '13574ef0d58b50fab38ec841efe39df4'

####1.1.1?????use-agent
    In [10]: public_lib.user_agent()
    Out[10]: 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'

##2????
####2.0.1???????,??????
    print public_lib.send_file(
        smtp='smtp.xxxxx.com',
        user='alert@xxxxx.com',
        passwd='xxxxx',
        subject="test file",
        to_list=['brach@lssin.com'],
        file_list=['/tmp/123','/tmp/456']
    )
####2.0.2?????
    print public_lib.send_mail(
        smtp='smtp.xxxxx.com',
        user='alert@xxxxx.com',
        passwd='xxxxx',
        subject="test mail",
        to_list=['brach@lssin.com'],
        text="hello word",
    )    

##3????            
####3.0.1??????????????pid????????
    In [2]: public_lib.pid('java')
    Out[2]: pid(memory=1056864, pid=['6168'])
    
    
    
##4????
####4.0.1 ??????????[/var/log/message]
    public_lib.syslog.error("test log")  