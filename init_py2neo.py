# _*_ coding:utf-8 _*_

from py2neo import Graph, Node
import pandas as pd


def init_py2neo():
    t1 = pd.read_excel('rel2.xlsx')
    g = Graph(
        "http://127.0.0.1:7474", auth=("neo4j", "12345678"),name="neo4j")
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


init_py2neo()
