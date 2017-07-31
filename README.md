###python 公共方法方便库,方便调用

#####1 进度条

    import time
    F = public_lib.proging_rate(screen_max=1000,screen_name='1000M',rate_symbol='#')
    for i in range(1000):
        time.sleep(0.1)
        F.update("%sM" % i)
    F.end()
    

#####2 漂亮的json    

    In [4]: print public_lib.json_data({'a':'你好'},indent=8)
    {
            "a": "你好"
    }
    
    In [5]: print public_lib.json_data({'a':'你好'})
    {
        "a": "你好"
    }
    
    In [6]: 


#####3 方便的time模块

    In [10]: public_lib.CurrTime()
    Out[10]: '2017-07-31 11:04:01'
    
    In [11]: public_lib.CurrDay()
    Out[11]: '2017-07-31'


#####4 文件便利

    In [17]: public_lib.all_file('.')
    Out[17]: 
    ['./+~JF1688623560254782582.tmp']

