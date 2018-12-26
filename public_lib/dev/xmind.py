#!/usr/bin/env python
#encoding=utf-8

#1.将xmind转换成txt
#2.将txt转换成excel

from textwrap import wrap
from microst_xlsx import ExportHander

class xmind:
    def __init__(self, *args, **kwargs):
        self.file = kwargs['file']

    def _count(self,**kwargs):
        source_data = kwargs['source_data']
        line_number = kwargs['line_number']
        k = []
        for t in source_data:
            try:
                t = t[line_number].encode('utf-8')
                k.append(len(t))
            except IndexError,e:
                pass
        max_size = max(k)
        if max_size < 15:
            return {"w":10}
        elif 30 > max_size > 14:
            return {"w": 20}
        elif 51 > max_size > 29:
            return {"w": 30}
        elif max_size > 100:
            return {"w": 70,"style":"left"}
        elif max_size > 50:
            return {"w": 40,"style":"left"}
        return {"w":max(k)*0.5}

    def _load(self):
        l  = []
        with open(self.file) as P:
            for i in P.read().strip().split('\n'):
                l.append(i.encode("utf-8").split('\t'))
        max_len = max([ len(j) for j in l ])
        data_txt = []
        menu_data = [ [str(m),str(m),self._count(line_number=m,source_data=l)] for m in range(max_len)]

        # 将不足的list元素置为空
        for r1 in range(max_len-1):
            for r_number in range(len(l)):
                r_h = l[r_number]
                if (max_len - len(r_h))!=0:
                    for ah in range(max_len - len(r_h)):
                        r_h.append('')
                    l[r_number] = r_h
                for r_num in range(len(r_h)):
                    try: #判断后一个，下一个是否为空，如果为真，则将内容移动到下一个
                        if r_h[r_num+1] == l[r_number+1][r_num] == "" and r_h[r_num] !="":
                            l[r_number + 1][r_num] = r_h[r_num]
                            l[r_number][r_num] = ""
                    except IndexError,e:
                        pass

        # 删除多余的空行
        for r2 in range(max_len-1):
            for r1_number in range(len(l)):
                try:
                    if set(l[r1_number]) == set([""]) == set(l[r1_number+1]):
                        del l[r1_number]
                except IndexError,e:
                    pass

        if set(l[0]) == set([""]):
            del l[0]

        # 计算需要合并的单元格
        merge_list = []
        for m_number in range(len(l)):
            for m_line_number in range(len(l[m_number][:-1])):
                try:
                    if l[m_number+1][m_line_number] == l[m_number+2][m_line_number] == "" :
                        merge_list.append([m_line_number+1,m_number+2,m_line_number+1,m_number+3])
                except IndexError,e:
                    pass
                merge_list = sorted(merge_list, key=lambda x: x[0], reverse=False)

        for t_set in range(len(merge_list)):
            for t_number in range(len(merge_list)):
                try:
                    if merge_list[t_number][0] == merge_list[t_number+1][0]:
                        if merge_list[t_number][3] == merge_list[t_number+1][1]:
                            merge_list[t_number][3] = merge_list[t_number][3]+1
                            del merge_list[t_number+1]
                            break
                except IndexError,e:
                    pass

        for number in range(len(l)):
            h = l[number]
            dict_temp = {}
            for h_num in range(len(h)):
                conntext = h[h_num].encode('utf-8').strip()
                if len(unicode(conntext,"utf-8"))>50:
                    dict_temp[menu_data[h_num][0]] = '\n'.join(wrap(unicode(conntext,"utf-8"),45))
                else:
                    dict_temp[menu_data[h_num][0]]=conntext
            data_txt.append(dict_temp)
        return {"data":data_txt,"menu":menu_data,"title":l[0][0],"merge":merge_list}

    def save_excel(self,file_path):
        data = self._load()
        return ExportHander(**data).save(file_path)

if __name__ == "__main__":
    F = xmind(file='/home/gaolin/Desktop/安全防护.txt')
    print F.save_excel('/data/temp/migang/yunwei/document/security/安全评测/安全防护.xlsx')
    print F.save_excel('/tmp/1.xlsx')

