from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship

'''
将多对多的关系表进行转化
这里将多对多关系转化成两个有向边
文件提供了转换成四个关系的函数
'''

graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))


# belong关系的构建
def create_belong(infos):
    for info in infos:
        aid = info[0]
        cid = info[1]
        # 匹配节点
        matcher = NodeMatcher(graph)
        app_node = matcher.match("application", Aid=aid).first()
        category_node = matcher.match("category", Cid=cid).first()
        # 创建关系
        relation_belong = Relationship(app_node, "Belong", category_node)
        relation_belonged = Relationship(category_node, "BeBelonged", app_node)
        graph.create(relation_belong)
        graph.create(relation_belonged)


# useof关系
def create_useof(infos):
    for info in infos:
        uid = info[0]
        aid = info[1]
        # 匹配节点
        matcher = NodeMatcher(graph)
        app_node = matcher.match("application", Aid=aid).first()
        user_node = matcher.match("user", Uid=uid).first()
        # 创建关系
        relation_useof = Relationship(user_node, "UseOf", app_node)
        relation_usedof = Relationship(app_node, "BeUsedOf", user_node)
        graph.create(relation_useof)
        graph.create(relation_usedof)


# runon关系
def create_runon(infos):
    for info in infos:
        aid = info[0]
        vmid = info[1]
        # 匹配节点
        matcher = NodeMatcher(graph)
        app_node = matcher.match("application", Aid=aid).first()
        vm_node = matcher.match('virtualmachine', VMid=vmid).first()
        # 创建关系
        relation_runon = Relationship(app_node, "RunOn", vm_node)
        relation_ranon = Relationship(vm_node, "BeRanOn", app_node)
        graph.create(relation_runon)
        graph.create(relation_ranon)


# replicia关系
def create_replicia(infos):
    for info in infos:
        dbsid1 = info[0]
        dbsid2 = info[1]
        # 匹配节点
        matcher = NodeMatcher(graph)
        dbs_node1 = matcher.match("databaseserver", DBSid=dbsid1).first()
        dbs_node2 = matcher.match("databaseserver", DBSid=dbsid2).first()
        # 创建关系
        relation_replicia = Relationship(dbs_node2, "Replicia", dbs_node1)
        relation_bereplicia = Relationship(dbs_node1, "BeReplicia", dbs_node2)
        graph.create(relation_replicia)
        graph.create(relation_bereplicia)
