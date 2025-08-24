# _*_ coding:utf-8 _*_

import pandas as pd
table = pd.read_excel("rel.xlsx",sheet_name="Sheet2",names=["文化","文本"])
table = table.applymap(lambda x:x.strip())
rel = []
for i,row in table.iterrows():
    sf = row['文本'].split("：")[0][:3]
    dq = row['文本'].split("：")[0][3:]
    jlyz = row['文本'].split("：")[1].split("、")
    rel.append([sf,"省份",dq,"地区","省份_地区","省份_地区"])
    for j in jlyz:
        rel.append([dq, "地区",j,f'{row["文化"]}_聚落遗址',"位置", "位置"])
        rel.append([row['文化'], "文化",j,f'{row["文化"]}_聚落遗址',"对应文化", "对应文化"])
    for j in range(len(jlyz)-1):
        rel.append([jlyz[j], f'{row["文化"]}_聚落遗址', jlyz[j+1], f'{row["文化"]}_聚落遗址', "相关文化", "相关文化"])
pd.DataFrame(rel,columns=['sub_name','sub_type','obj_name','obj_type','rel_name','rel_type']).drop_duplicates().to_excel("rel2.xlsx",index=None)
