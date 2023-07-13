from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship
import Create_neo4j  # 导入读取data文加夹中读取csv文件的方法,在Create中导入创建节点和关系的py文件
import CRUD

"""
test进行测试
测试结果是否正确
"""


graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))

if __name__ == "__main__":
    Create_neo4j.read_create_node()
    Create_neo4j.read_create_relation()

    # 测试：增
    print("---------测试增-------")
    CRUD.create_node("user", "Uid", "User100")
    CRUD.create_node("user", "Uid", "User101")
    # 查找对应节点
    print("--------增加两个节点---------")
    matcher = NodeMatcher(graph)
    new_node1 = matcher.match("user", Uid="User100").first()
    new_node2 = matcher.match("user", Uid="User101").first()
    # 打印两个节点看看是否添加
    print(new_node1, "\n", new_node2)
    print("----------增加关系----------")
    CRUD.create_relation(new_node1, "同事", new_node2)
    query = "match (n) -[r:同事]->(m) return r"
    result = CRUD.run_Cypher(query)
    # 打印关系看看关系是否添加
    print(result)
    print("---------测试增结束-------")

    # 测试改
    print("---------测试改-------")
    CRUD.update_node("user", "Uid", "User100", "gender", "男")
    new_node1 = matcher.match("user", Uid="User100").first()
    print(new_node1)
    CRUD.update_node("user", "Uid", "User100", "gender", "女")
    new_node1 = matcher.match("user", Uid="User100").first()
    print(new_node1)
    print("---------测试改结束-------")

    # 测试查
    print("---------测试查-------")
    # 测试传入的为空
    result1 = CRUD.retrieve()
    print("测试传入参数为空:", result1)
    # 测试第一个参数不为空，其它为空
    result2 = CRUD.retrieve("user")
    print("第一个参数不为空,返回结果个数:", len(result2))
    # 测试前两个参数不为空，其它为空
    result3 = CRUD.retrieve("user", "同事")
    print("前两个参数不为空:", result3)
    # 测试三个参数都不为空
    result4 = CRUD.retrieve("user", "UseOf", "application")
    print("三个参数都不为空,返回结果个数", len(result4))
    print("---------测试查结束-------")

    # 测试删除
    # 删除User100 以及其对应关系,最后打印结果应为空
    print("---------测试删-------")
    CRUD.delete_node("user", "Uid", "User100")
    new_node1 = matcher.match("user", Uid="User100").first()
    print(new_node1)
    # 删除节点User101 (孤立节点删除),最后打印结果应为空
    CRUD.delete_node("user", "Uid", "User101")
    new_node2 = matcher.match("user", Uid="User101").first()
    print(new_node2)
    print("---------测试删结束-------")

    # 复杂查询实现
    # 利用run_Cypher 提供的借口，实现该操作
    # 复杂查询,只提供路径长度的查询，其他查询输入query语句完成
    print("---------测试复杂查询-------")
    # 测试大于和任意路径由于建立的图数据库节点和关系较多，较为复杂，时间较长，这里不做测试
    # 测试小于
    node_list2 = CRUD.len_retrieve("user", "Uid", "User001", 2, operation="小于")
    print(len(node_list2))
    # 测试位于len1，len2之间
    node_list3 = CRUD.len_retrieve("user", "Uid", "User001", 2, 4)
    print(len(node_list3))
    print("---------测试复杂查询结束-------")
