#!/usr/bin/env python
#encoding=utf-8
#Created by gaolin on 2017-10-11 10:17
import public_lib
import traceback
import  pandas  as pd
from error_msg import RaiseVlues

class ImportPands:
    def __init__(self,**kwargs):
        """
        read excel data
        :param kwargs:
            :primary_key:clumn data primary
            :menu: menu name,format is [[field name,menu name],[field name,menu name]]
        """
        self.data_excel = []
        self.primary_key = kwargs.get('primary_key',[])     #判断字段是否唯一,某个菜单中的数据不能重复
        self.menu_list = kwargs['menu']   #excel的菜单栏[菜单名称fidld1,菜单名称fidld2,菜单名称fidld3]
        self.x = 1      #设置从第几列开始读取数据
        self.y = 1      #设置从第几行开始读取数据
        self.msg = {"status": False, "msg": "", "data": []}
        self.file_path = ""

    def lock(Fn):
        def Test(self, *args, **kwargs):
            if len(set(self.menu_list)) == len(self.menu_list):
                data = Fn(self, *args, **kwargs)
                if self.primary_key:
                    for primary_name in self.primary_key:
                        temp_data = []
                        for info in data:
                            try:
                                temp_data.append(info[primary_name])
                            except KeyError,e:
                                raise RaiseVlues("非法菜单: %s" % primary_name)
                        if len(temp_data) != len(set(temp_data)):
                            for i in set(temp_data):
                                if temp_data.count(i) > 1:
                                    raise RaiseVlues("%s，重复数据:%s" % (primary_name,i))
                return data
            raise RaiseVlues("Field重复")
        return Test


    @lock
    def load_data(self, **kwargs):
        df = pd.read_excel(self.file_path,sheet_name=kwargs.get("table_number",0))
        all_data = []
        for i in df.index.values:
            if i > self.x:
                raw_data = df.ix[i].values
                raw_dict = {}
                for raw_num,raw_name in enumerate(self.menu_list):
                    try:
                        raw_dict[self.menu_list[raw_num]] = raw_data[raw_num+self.y]
                    except IndexError,e:
                        raw_dict[self.menu_list[raw_num]] = ""
                all_data.append(raw_dict)
        return all_data

    def table_list(self):
        f = pd.ExcelFile(self.file_path)
        return f.sheet_names

    def file(self,**kwargs):
        try:
            self.file_path = kwargs["file_path"]
            data = self.load_data(**kwargs)
        except IOError,e:
            self.msg['msg'] = '%s,文件不存在' % self.file_path
            return self.msg
        except RaiseVlues,e:
            self.msg['msg'] = e.message
            return self.msg
        except Exception,e:
            print traceback.format_exc()
            self.msg['msg'] = '读取数据失败,ERROR:%s' % traceback.format_exc()
            return self.msg
        self.msg["status"] = True
        self.msg["data"] = data
        return self.msg


if __name__ == "__main__":
    import_meni = ['ID','sn','name']
    d = ImportPands(menu=import_meni,primary_key=[])
    d.x = 1
    d.y = 1
    print public_lib.json_data(d.file(file_path='/Users/gaolin/Downloads/网络设备-模板.xlsx'))




