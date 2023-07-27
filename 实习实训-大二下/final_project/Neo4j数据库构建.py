from py2neo import Graph
from py2neo import Node
from py2neo import NodeMatcher
from py2neo import Relationship
from py2neo import RelationshipMatcher
import csv


class Csv2Neo4j:
    def __init__(self):
        self.graph = Graph("bolt: // localhost:7474", auth=("neo4j", "12345678"))

    def create_node(self, infos):
        """
        创建除了疾病以外的节点
        去重通过判断节点或者关系是否在当前图中
        :param infos: csv文件读取结果
        """
        for info in infos:
            if info["label"] == "食物":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("食物", name=info["name"])
                    self.graph.create(node)
                continue
            if info["label"] == "治疗方式":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("治疗方式", name=info["name"])
                    self.graph.create(node)
                continue
            if info["label"] == "药物":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("药物", name=info["name"])
                    self.graph.create(node)
                continue
            if info["label"] == "症状":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("症状", name=info["name"])
                    self.graph.create(node)
                continue
            if info["label"] == "检查":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("检查", name=info["name"])
                    self.graph.create(node)
                continue
            if info["label"] == "科室":
                if self.not_have("Node", label=info["label"], name=info["name"]):
                    node = Node("科室", name=info["name"])
                    self.graph.create(node)
                continue

    def create_relation(self, infos):
        # 创建关系的节点
        # 去重通过判断节点或者关系是否在当前图中
        matcher = NodeMatcher(self.graph)
        for info in infos:
            start_name = info["start"]
            end_name = info["end"]
            if info["label"] == "检查项目":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("检查", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "检查项目", end_node)
                    self.graph.create(relation)
                continue

            if info["label"] == "并发症":
                # 有的并发症可能只在关系的end节点中出现，所以这里需要考虑end节点是不是空，以防报错
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("疾病", name=end_name).first()
                if end_node is None:
                    end_node = Node("疾病", name=end_name)
                    self.graph.create(end_node)
                    end_node = matcher.match("疾病", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "并发症", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "治疗":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("治疗方式", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "治疗", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "就诊科室":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("科室", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "就诊科室", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "科室从属":
                start_node = matcher.match("科室", name=start_name).first()
                end_node = matcher.match("科室", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "科室从属", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "推荐药物":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("药物", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "推荐药物", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "常见药物":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("药物", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "常见药物", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "病症":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("症状", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "病症", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "推荐吃":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("食物", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "推荐吃", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "宜吃":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("食物", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "宜吃", end_node)
                    self.graph.create(relation)
                continue
            if info["label"] == "忌吃":
                start_node = matcher.match("疾病", name=start_name).first()
                end_node = matcher.match("食物", name=end_name).first()
                if self.not_have(
                    n_r="Relation", label=info["label"], start=start_node, end=end_node
                ):
                    relation = Relationship(start_node, "忌吃", end_node)
                    self.graph.create(relation)
                continue

    def create_illness(self, infos):
        # 创建疾病节点
        for info in infos:
            matcher = NodeMatcher(self.graph)
            node = matcher.match("疾病", name=info["name"]).first()
            if node is None:
                node = Node(
                    "疾病",
                    name=info["name"],
                    insurance=info["insurance"],
                    easy_get=info["easy_get"],
                    get_way=info["get_way"],
                    cure_time=info["cure_time"],
                    cured_prob=info["cured_prob"],
                    cost_money=info["cost_money"],
                    cause=info["cause"],
                    prevent=info["prevent"],
                    desc=info["desc"],
                    get_prob=info["get_prob"],
                )
                self.graph.create(node)
                continue
            if node["cause"] is None:
                self.graph.delete(node)
                node = Node(
                    "疾病",
                    name=info["name"],
                    insurance=info["insurance"],
                    easy_get=info["easy_get"],
                    get_way=info["get_way"],
                    cure_time=info["cure_time"],
                    cured_prob=info["cured_prob"],
                    cost_money=info["cost_money"],
                    cause=info["cause"],
                    prevent=info["prevent"],
                    desc=info["desc"],
                    get_prob=info["get_prob"],
                )
                self.graph.create(node)
                continue

    def not_have(self, n_r, label=None, name=None, start=None, end=None):
        # 判断构建的Neo4j是否含有某个节点或者关系，来防止重复构建节点和关系
        if n_r == "Node":
            matcher = NodeMatcher(self.graph)
            node = matcher.match(label, name=name).first()
            if node is None:
                return True
            else:
                return False
        if n_r == "Relation":
            matcher = RelationshipMatcher(self.graph)
            relation = matcher.match({start, end}, label).first()
            if relation is None:
                return True
            else:
                return False
        return None

    def read_create(self, node_path, relation_path, illness_path):
        # 读取node文件
        f_node = open(node_path, "r", encoding="UTF-8-sig")
        node_rows = csv.DictReader(f_node)
        # 读取relation文件
        f_relation = open(relation_path, "r", encoding="UTF-8-sig")
        relation_rows = csv.DictReader(f_relation)
        # 读取疾病文件
        f_illness = open(illness_path, "r", encoding="UTF-8-sig")
        illness_rows = csv.DictReader(f_illness)
        # 创建neo4j
        # 这里创建顺序需要注意，为疾病，其他节点，关系创建
        self.create_illness(illness_rows)
        self.create_node(node_rows)
        self.create_relation(relation_rows)


handler = Csv2Neo4j()
handler.read_create("./data/node.csv", "./data/relation.csv", "./data/illness.csv")
