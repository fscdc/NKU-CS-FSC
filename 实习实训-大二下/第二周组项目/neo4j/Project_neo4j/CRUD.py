from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship
import Create_neo4j

graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))

'''
CRUD.py提供了六个函数
实现了CRUD的功能，具体功能每个函数里面有说明
复杂查询实现路径长度的查询
'''


# 测试函数
# 执行Cypher语句，只能先订sentence是一个正确的查询语句，不能有语法错误
def run_Cypher(sentence):
    cursors = graph.run(sentence)
    return list(cursors)


# 简单的增删改查
# 查询，该查询查询的是一类的节点，不是某个节点的关系
# 如果查询某个节点的各个关系，需要直接使用 run_Cypher 构思语句即可（通过py2neo也可，但没有实现函数，与query思路相似）
def retrieve(label1=None, relation=None, label2=None):
    # 如果传进来是空，返回所有
    if label1 == None and relation == None and label2 == None:
        return []
    # 传入第一个参数，查找相应所有标签的节点
    if label1 != None and relation == None and label2 == None:
        query = "MATCH (n:`{}`) RETURN n".format(label1)
        return run_Cypher(query)
    # 传入的label1 和 relation非空,返回关系
    if label1 != None and relation != None and label2 == None:
        query = "MATCH (n:{})-[r:{}]->(m) RETURN r".format(label1, relation)
        return run_Cypher(query)
    # 传入的参数都非空，返回关系
    if label1 != None and relation != None and label2 != None:
        query = "MATCH (n:{})-[r:{}]->(m:{}) RETURN r".format(label1, relation, label2)
        return run_Cypher(query)
    # 对于其它情况也类似，这里不做封装，其他情况返回空列表
    return []


# 增加数据，可以增加节点，需要输入id和name属性
# 也可以增加relation，需要两个节点和关系的名称
def create_node(label, idname, id):
    create_sentence = "CREATE (n:" + label + "{" + idname + ":'" + id + "'})"
    run_Cypher(create_sentence)


def create_relation(node1, relation, node2):
    relation = Relationship(node1, relation, node2)
    graph.create(relation)


# 删除
# 这里只给出删除一个节点的情况
# 对于其他的删除需要构建删除语句，调用run_Cypher
def delete_node(label, idname, id):
    # 首先判断其是否有关系
    query = "match (n:{})-[r]-() where n.{}='{}' return r".format(label, idname, id)
    result = run_Cypher(query)
    if len(result) == 0:
        delete_sentence = "match (n:{}) where n.{}='{}' delete n".format(label, idname, id)
        run_Cypher(delete_sentence)
    else:
        delete_sentence = "match (n:{})-[r]-() where n.{}='{}' delete n,r".format(label, idname, id)
        run_Cypher(delete_sentence)


# 改
# 这里给出修改某个节点的属性
def update_node(label, idname, id, atrname, atr):
    update_sentence = "match (n:{}) where n.{}='{}' set n.{}='{}' return n".format(label, idname, id, atrname, atr)
    run_Cypher(update_sentence)


# 复杂查询，查询对应路径长度的结果节点
def len_retrieve(label1=None, idname=None, id=None, len1=None, len2=None, operation=None):
    # 匹配任意长度路径
    if len1 == '*' and len2 == '*':
        query = "match (n:{})-[*]->(m) where n.{}='{}'return m".format(label1, idname, id)
        return run_Cypher(query)
    # 大于len1长度路径
    if operation == '大于':
        query = "match (n:{})-[*{}..]->(m) where n.{}='{}'return m".format(label1, len1, idname, id)
        return run_Cypher(query)
    # 小于len1长度路径
    if operation == '小于' and len1 > 0:
        query = "match (n:{})-[*..{}]->(m) where n.{}='{}'return m".format(label1, len1, idname, id)
        return run_Cypher(query)
    # len1,len2之间路径
    if len1 != None and len2 != None:
        query = "match (n:{})-[*{}..{}]->(m) where n.{}='{}'return m".format(label1, len1, len2, idname, id)
        return run_Cypher(query)
    return []
