import os
# import ahocorasick
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
# Create your views here.
from py2neo import Graph, Node
import pandas as pd
from .models import Rel, alldata
from collections import Counter
table = pd.read_excel("data/终 地点2.xlsx")
Node2 = {}
columns = table.columns.values.tolist()
for i,row in table.iterrows():
    Node2[row[columns[0]]] = {}
    for j in columns[1:]:
        # print(j)
        if row[j]!="无":
            Node2[row[columns[0]]][j] = str(row[j]).replace("\n","").strip()
# print(Node2)

# g = Graph(
#     "http://127.0.0.1:7474", auth=("neo4j", "12345678"), name="neo4j")


def index(request):
    return render(request, "index.html")


def getalldata(request):
    data = django_to_table()
    # data2 = json.load(open("E:/project/dj_vue/vue-d3-graph-main/src/data/records.json", "r", encoding="utf-8"))
    # data2 = json.load(open("E:/project/dj_vue/1.json", "r", encoding="utf-8"))

    # data2 = make_json(data.sample(frac=1).iloc[:200])
    data2 = make_json(data)
    print(data2)
    return HttpResponse(json.dumps(data2), content_type='application/json')


def getdata(request):
    data = django_to_table()

    key_word = request.GET['name']
    query_type = '1'
    print(key_word, query_type)
    if query_type == '1':
        data2, _ = find(data, key_word)
        data2 = make_json(data2)
    elif query_type == '2':
        data2, layel2node = find(data, key_word)
        t = [data2]
        for key_word2 in layel2node:
            data3, layel3node = find(data, key_word2)
            t.append(data3)
        t = pd.concat(t)
        data2 = t.drop_duplicates()
        data2 = make_json(data2)

    return HttpResponse(json.dumps(data2), content_type='application/json')


def init_py2neo(request):
    t1 = django_to_table()

    g.delete_all()
    is_create = []
    for index, i in t1[['sub_type', 'sub_name']].iterrows():
        if i['sub_name'] not in is_create:
            is_create.append(i['sub_name'])
            node = Node(i['sub_type'], name=i['sub_name'])
            g.create(node)
    for index, i in t1[['obj_type', 'obj_name']].iterrows():
        if i['obj_name'] not in is_create:
            is_create.append(i['obj_name'])
            node = Node(i['obj_type'], name=i['obj_name'])
            g.create(node)

    for index, i in t1.iterrows():
        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            i['sub_type'], i['obj_type'], i['sub_name'], i['obj_name'], i['rel_type'], i['rel_name'])
        print(query)
        try:
            g.run(query)
        except Exception as e:
            print(e)


def init_models():
    t1 = pd.read_excel("data/rel3.xlsx")
    table_ = t1.drop_duplicates().dropna()
    Rel.objects.all().delete()
    r = []
    for index, row in table_.iterrows():
        r.append(Rel(obj_name=row['obj_name'], obj_type=row['obj_type'],
                     rel_name=row['rel_name'], rel_type=row['rel_type'],
                     sub_name=row['sub_name'], sub_type=row['sub_type']))
    Rel.objects.bulk_create(r)
    print("success")

    table.drop_duplicates().dropna()
    alldata.objects.all().delete()
    r2 = []
    for index, row in table.iterrows():
        r2.append(alldata(k1=row['地点'], k2=row['createtime'],
                     k3=row['createcd'], k4=row['address'],
                     k5=row['size'], k6=row['desc']))

    alldata.objects.bulk_create(r2)
    print("success")

def django_to_table():
    t = pd.DataFrame(Rel.objects.values()).drop_duplicates(subset=['sub_name','obj_name'])
    print(t)
    return t
def find(table, node, type="all"):
    """
    根据结点获取与之相邻的邻居
    """

    t1 = table[table['sub_name'] == node]
    t1_child_node = t1['obj_name'].values.tolist()
    t2 = table[table['obj_name'] == node]
    t2_parent_node = t2['sub_name'].values.tolist()
    if type == "all":
        t = pd.concat((t1, t2))
        t_node = list(set(t1_child_node + t2_parent_node))
    if type == "child":
        t = t1
        t_node = t1_child_node
    if type == "parent":
        t = t2
        t_node = t2_parent_node

    return t, t_node


def make_json(table):
    data = []
    links = []
    legends = []
    l1 = table['sub_type'].values.tolist()
    l2 = table['obj_type'].values.tolist()
    l3 = table['sub_name'].values.tolist()
    l4 = table['obj_name'].values.tolist()

    category = {v: k for k, v in enumerate(sorted(list(set(l1 + l2))))}
    nodes = {v: k for k, v in enumerate(sorted(list(set(l3 + l4))))}
    legends = [k for k, v in category.items()]
    categories = [{'name': k} for k, v in category.items()]
    types = {}
    for i, row in table.iterrows():
        types[row['sub_name']] = row['sub_type']
        types[row['obj_name']] = row['obj_type']

    # print(categories)
    for i, j in nodes.items():
        data.append({'name': i, 'category': category[types[i]]})
    for i, row in table.iterrows():
        links.append({'source': nodes[row['sub_name']], "target": nodes[row['obj_name']], "value": row['rel_name']})

    return {"data": data, "links": links, "name": legends, "categories": categories}


# init_models()
#
#
# init_py2neo(1)


def regist(request):
    if request.method == 'GET':
        return render(request, "regist.html")
    else:
        try:
            userid = request.POST['id']
            userpw = request.POST['pw']
            useremail = request.POST['email']
            username = request.POST['name']
            usersex = request.POST['sex']
            usersr = request.POST['sr']
            userage = request.POST['age']
            userpn = request.POST['phonenum']
        except Exception as e:
            raise e
            render(request, "regist.html")
        try:
            G_user = Group.objects.get(name="一般用户")
            user = User.objects.create_user(username=userid,
                                            password=userpw,
                                            email=useremail, is_staff=True)
            user.groups.add(G_user)
            user.save()
            try:
                Users.objects.create(user=user,
                                     userName=username,
                                     userSex=usersex,
                                     userAge=userage,
                                     usersr=usersr,
                                     userPhoneNum=userpn).save()

                return HttpResponseRedirect('/admin/')
            except Exception as e:
                raise e
                print(e)
                return HttpResponse("regist fail")
            return render(request, "regist.html")
        except Exception as e:
            print(e)
            return render(request, "regist.html")


def networks(request):
    return render(request, template_name="index2.html")


def plot_scores(request):
    t =django_to_table()
    print(t)
    t1 = t[t['sub_type'] != '类型']
    ys = {row['obj_name']:row['sub_name'] for i,row in t1.iterrows()}
    t2 = t[t['sub_type'] != '类型']
    t3 = t[t['sub_type'] == '类型']
    t2['地区'] = t2['obj_name'].apply(lambda x:ys[x])
    print(t2)
    print(t3)
    m = t2.groupby("sub_name",as_index=False)['obj_name'].count()
    m3 = t2.groupby("地区", as_index=False)['obj_name'].count()
    m2 = t3.groupby("sub_name",as_index=False)['obj_name'].count()
    student_scores2 = []
    table4 = pd.read_excel("data/终 地点2.xlsx")
    t4 = table4.groupby("createcd",as_index=False)['地点'].count().sort_values("地点").tail(30)

    for i, j in t4.iterrows():
        if j['createcd'] != "不详":
            student_scores2.append({"name": j['createcd'], "value": j['地点']})
    print(student_scores2)
    student_scores = []
    for i, j in m.iterrows():
        student_scores.append({"name": str(j['sub_name']), "score": j['obj_name']})
    student_scores3 = []
    for i, j in m2.iterrows():
        student_scores3.append({"name": str(j['sub_name']), "score": j['obj_name']})

    t_2 = t2[['sub_name','obj_name']]
    t_3 = t3[['sub_name','obj_name']]
    t_3.columns = ['类型','名地']
    t_2.columns = ['地区','名地']
    t4 = pd.merge(left=t_2,right=t_3,left_on='名地',right_on='名地')
    t4 = t4.groupby(['类型','地区'],as_index=False).count()
    x1 = {j:i for i,j in enumerate(t4['类型'].unique())}
    y1 = {j:i for i,j in enumerate(t4['地区'].unique())}
    data4 = [[x1[row['类型']],y1[row['地区']],row['名地']]for i,row in t4.iterrows()]
    print(t4)

    return render(request, template_name="tonji.html",context={"data1":student_scores,"data2":student_scores2,"data3":student_scores3,
                                                                'data4':data4,'x1':list(x1.keys()),'y1':list(y1.keys())})#
def plot_map(request):
    table = pd.read_csv("data/address.csv",names=['地址','经度','维度'])
    data = []
    geoCoordMap = {}
    for i,row in table.iterrows():
        data.append({"name":row['地址'],"value":100})
        geoCoordMap[row['地址']] = [row['经度'],row['维度']]

    return render(request, template_name="map.html",context={"data":data,"geoCoordMap":geoCoordMap})
