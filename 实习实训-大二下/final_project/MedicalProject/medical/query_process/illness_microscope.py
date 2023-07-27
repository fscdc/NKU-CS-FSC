from py2neo import Graph
from py2neo import NodeMatcher

"""
查询疾病名称
返回结果的字典
"""

class IllnessMicroscope:
    def __init__(self) -> None:
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))

    def query_info(self, name: str) -> dict:
        illness_info = {"病名": name}

        # 疾病属性
        matcher = NodeMatcher(self.graph)
        illness = matcher.match("疾病", name=name).first()
        illness_info["简介"] = illness["desc"]
        illness_info["患病比例"] = illness["get_prob"]
        illness_info["成因"] = illness["cause"]
        illness_info["预防措施"] = illness["prevent"]
        illness_info["传染方式"] = illness["get_way"]
        illness_info["易感人群"] = illness["easy_get"]
        illness_info["医保疾病"] = illness["insurance"]
        illness_info["治愈率"] = illness["cured_prob"]
        illness_info["治疗周期"] = illness["cure_time"]
        illness_info["治疗费用"] = illness["cost_money"]

        # 治疗方式
        cure_method_query = (
            "match (n:疾病)-[r:治疗]->(m:治疗方式) where n.name='{}' return m".format(name)
        )
        cure_method_list = []
        for cure_method_item in list(self.graph.run(cure_method_query)):
            cure_method_node = cure_method_item.get("m")
            cure_method_list.append(cure_method_node["name"])
        illness_info["治疗方式"] = cure_method_list

        # 检查项目
        check_query = "match (n:疾病)-[r:检查项目]->(m:检查) where n.name='{}' return m".format(
            name
        )
        check_list = []
        for check_item in list(self.graph.run(check_query)):
            check_node = check_item.get("m")
            check_list.append(check_node["name"])
        illness_info["检查项目"] = check_list

        # 并发症
        complication_query = (
            "match (n:疾病)-[r:并发症]->(m:疾病) where n.name='{}' return m".format(name)
        )
        complication_list = []
        for complication_item in list(self.graph.run(complication_query)):
            complication_node = complication_item.get("m")
            complication_list.append(complication_node["name"])
        illness_info["并发症"] = complication_list

        # 症状
        symptom_query = "match (n:疾病)-[r:病症]->(m:症状) where n.name='{}' return m".format(
            name
        )
        symptom_list = []
        for symptom_item in list(self.graph.run(symptom_query)):
            symptom_node = symptom_item.get("m")
            symptom_list.append(symptom_node["name"])
        illness_info["症状"] = symptom_list

        # 常见药物&治疗药物
        common_med_query = (
            "match (n:疾病)-[r:常见药物]->(m) where n.name='{}' return m".format(name)
        )
        common_med_list = []
        for common_med in list(self.graph.run(common_med_query)):
            common_med_list.append(common_med.get("m")["name"])
        illness_info["常见药物"] = common_med_list

        cure_med_query = "match (n:疾病)-[r:治疗药物]->(m) where n.name='{}' return m".format(
            name
        )
        cure_med_list = []
        for cure_med in list(self.graph.run(cure_med_query)):
            cure_med_list.append(cure_med.get("m")["name"])
        illness_info["治疗药物"] = cure_med_list

        # 推荐吃
        recommend_food_query = (
            "match (n:疾病)-[r:推荐吃]->(m) where n.name='{}' return m".format(name)
        )
        recommend_food_list = []
        for recommend_food in list(self.graph.run(recommend_food_query)):
            recommend_food_list.append(recommend_food.get("m")["name"])
        illness_info["推荐吃"] = recommend_food_list

        # 忌吃
        forbid_food_query = (
            "match (n:疾病)-[r:忌吃]->(m) where n.name='{}' return m".format(name)
        )
        forbid_food_list = []
        for forbid_food in list(self.graph.run(forbid_food_query)):
            forbid_food_list.append(forbid_food.get("m")["name"])
        illness_info["忌吃"] = forbid_food_list

        # 宜吃
        suitable_food_query = (
            "match (n:疾病)-[r:宜吃]->(m) where n.name='{}' return m".format(name)
        )
        suitable_food_list = []
        for suitable_food in list(self.graph.run(suitable_food_query)):
            suitable_food_list.append(suitable_food.get("m")["name"])
        illness_info["宜吃"] = suitable_food_list

        # 科室
        depart_query = "match (n:疾病)-[r:就诊科室]->(m) where n.name='{}' return m".format(
            name
        )
        depart_list = []
        for depart in list(self.graph.run(depart_query)):
            depart_list.append(depart.get("m")["name"])
        illness_info["就诊科室"] = depart_list

        return illness_info

# 病痛显微镜全局实例
illness_microscope = IllnessMicroscope()

if __name__ == "__main__":
    pass