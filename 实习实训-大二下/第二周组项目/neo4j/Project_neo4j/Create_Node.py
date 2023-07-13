from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship

'''
创建节点
文件提供了创建节点的八个的函数
'''

graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))


# 创建user的函数
def create_user(infos):
    for info in infos:
        # Uid，性别，年龄，邮箱
        user_node = Node('user', Uid=info[0], gender=info[1], age=info[2], email=info[3])
        graph.create(user_node)


# 创建application的函数
def create_application(infos):
    for info in infos:
        # Aid,名称，版本，开发者，简述，占用空间大小
        # 外键 databaseserver.DBSid
        application_node = Node('application', Aid=info[0], name=info[1], version=info[2], dev=info[3], profile=info[4],
                                size=info[5])
        graph.create(application_node)

        # 外键处理
        matcher = NodeMatcher(graph)
        databaseserver_node = matcher.match("databaseserver", DBSid=info[-1])
        if len(databaseserver_node) == 0:
            continue
        App_DBS = Relationship(application_node, 'App_DBS', databaseserver_node.first())
        graph.create(App_DBS)


# 创建category的函数
def create_category(infos):
    for info in infos:
        # Cid,名称,说明
        category_node = Node('category', Cid=info[0], name=info[1], profile=info[2])
        graph.create(category_node)


# 创建databaseserver的函数
def create_databaseserver(infos):
    for info in infos:
        # DBSid,名称,IP地址,DBMS类型,版本,处理器类型,内存容量
        databaseserver_node = Node('databaseserver', DBSid=info[0], name=info[1], IP=info[2], DB_class=info[3],
                                   version=info[4], pro_class=info[5], size=info[6])
        graph.create(databaseserver_node)


# 创建loadbalancer的函数
def create_loadbalancer(infos):
    for info in infos:
        # LBid,名称,IP地址,端口,负载分发算法,SSL加速,会话保持
        # 外键rack.Rid
        loadbalancer_node = Node('loadbalancer', LBid=info[0], name=info[1], IP=info[2], port=info[3], load=info[4],
                                 SSL=info[5], session=info[6])
        graph.create(loadbalancer_node)

        # 外键处理
        matcher = NodeMatcher(graph)
        rack_node = matcher.match("rack", Rid=info[-1])
        if len(rack_node) == 0:
            continue
        LdB_Rack = Relationship(loadbalancer_node, 'LdB_Rack', rack_node.first())
        graph.create(LdB_Rack)


# 创建virtualmachine的函数
def create_virtualmachine(infos):
    for info in infos:
        # VMid，名称，版本，访问控制，认证配置、容错设置
        virtualmachine_node = Node('virtualmachine', VMid=info[0], name=info[1], version=info[2], visitcontrol=info[3],
                                   auth=info[4], allowerror=info[5])
        graph.create(virtualmachine_node)

        # 外键处理
        matcher = NodeMatcher(graph)
        server_node = matcher.match("server", Sid=info[-1])
        if len(server_node) == 0:
            continue
        VM_Srv = Relationship(virtualmachine_node, 'VM_Srv', server_node.first())
        graph.create(VM_Srv)


# 创建rack的函数
def create_rack(infos):
    for info in infos:
        # Rid，名称，位置，容量
        rack_node = Node('rack', Rid=info[0], name=info[1], address=info[2], capacity=info[3])
        graph.create(rack_node)


# 创建server的函数
def create_server(infos):
    for info in infos:
        # Sid，名称，IP地址，操作系统，处理器类型、内存容量
        # rack.Rid
        server_node = Node('server', Sid=info[0], name=info[1], IP=info[2], operationsystem=info[3], processor=info[4],
                           memoryspace=info[5])
        graph.create(server_node)

        # 外键处理
        matcher = NodeMatcher(graph)
        rack_node = matcher.match("rack", Rid=info[-1])
        if len(rack_node) == 0:
            continue
        server_Rack = Relationship(server_node, 'server_Rack', rack_node.first())
        graph.create(server_Rack)
