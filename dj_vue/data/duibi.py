# _*_ coding:utf-8 _*_
"""
@File     : duibi.py
@Project  : k
@Time     : 2024/5/4 14:32
@Author   : KUN
@Software : PyCharm
@License  : (C)Copyright 2018-2028, Taogroup-NLPR-CASIA
@Last Modify Time      @Version     @Desciption
--------------------       --------        -----------
2024/5/4 14:32        1.0             None
"""
import pandas as pd
if __name__ == '__main__':
    t1 = pd.read_excel("rel2.xlsx")
    print(len(set(t1['obj_name'].values.tolist())))
    t2 = pd.read_excel("终 地点2.xlsx")
    sy = set(t2['地点'].values.tolist())-set(t1['obj_name'].values.tolist())
    print(len(t2),len(t1),len(sy))
    for i in sy:
        print(i)
