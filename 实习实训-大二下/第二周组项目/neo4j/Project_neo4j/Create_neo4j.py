from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship
import Create_Node  # 导入创建节点的函数，
import Create_Relation  # 导入创建关系的函数

'''
读取csv文件
导入Create_Node和Create_Relation来辅助neo4j图数据库创建
read_create_node提供节点读取与创建
read_create_relation实现关系读取与创建
'''

graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))


# match (n) optional match (n)-[r]-() delete n,r

# 读取节点csv并创建节点
def read_create_node():
    # 读取数据
    entitySet_path = './data/eni/'
    entitySet_list = ['application', 'category', 'databaseserver', 'loadbalancer', 'rack', 'server', 'user',
                      'virtualmachine']
    node_list = []
    for entitySet in entitySet_list:
        headers, rows = [], []
        with open(entitySet_path + entitySet + '.csv', "r", encoding='UTF-8') as fp:
            headers = fp.readline().replace('\"', '').replace('\n', '').split(',')
            while True:
                row_list = fp.readline()
                if not row_list:
                    break
                rows.append(row_list.replace('\"', '').replace('\n', '').split(','))
            node_list.append(rows)

    # 创建节点
    Create_Node.create_category(node_list[1])
    Create_Node.create_databaseserver(node_list[2])
    Create_Node.create_rack(node_list[4])
    Create_Node.create_server(node_list[5])
    Create_Node.create_user(node_list[6])
    # 创建有外键的节点
    Create_Node.create_application(node_list[0])
    Create_Node.create_loadbalancer(node_list[3])
    Create_Node.create_server(node_list[5])
    Create_Node.create_virtualmachine(node_list[7])


# 读取关系csv并创建
def read_create_relation():
    # 读取数据
    Relation_path = './data/rel/'
    Relation_names = ['belong', 'replicia', 'runon', 'useof']
    relation_list = []
    for Relation_name in Relation_names:
        headers, rows = [], []
        with open(Relation_path + Relation_name + '.csv', "r", encoding='UTF-8') as fp:
            headers = fp.readline().replace('\"', '').replace('\n', '').split(',')
            while True:
                row_list = fp.readline()
                if not row_list:
                    break
                rows.append(row_list.replace('\"', '').replace('\n', '').split(','))
            relation_list.append(rows)
    # 创建关系
    Create_Relation.create_belong(relation_list[0])
    Create_Relation.create_replicia(relation_list[1])
    Create_Relation.create_runon(relation_list[2])
    Create_Relation.create_useof(relation_list[3])
