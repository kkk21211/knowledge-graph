# _*_ coding:utf-8 _*_
"""
@File     : 扩展地区.py
@Project  : k
@Time     : 2024/5/4 14:56
@Author   : KUN
@Software : PyCharm
@License  : (C)Copyright 2018-2028, Taogroup-NLPR-CASIA
@Last Modify Time      @Version     @Desciption
--------------------       --------        -----------
2024/5/4 14:56        1.0             None
"""
import pandas as pd
if __name__ == '__main__':
    t1 = pd.read_excel("rel2.xlsx")
name = "常州，无锡，嘉兴，苏州，湖州，安吉".split("，")
rel2 = []
for i,row in t1.iterrows():
    for k in name:
        if k in row['obj_name']:
            rel2.append(["地区",k,row['obj_name'],row['obj_type'],"所在地区","所在地区"])

rel2 = pd.DataFrame(rel2,columns=['sub_name','sub_type','obj_name','obj_type','rel_name','rel_type']).drop_duplicates()
pd.concat([t1,rel2]).drop_duplicates().to_excel("rel3.xlsx",index=None)
