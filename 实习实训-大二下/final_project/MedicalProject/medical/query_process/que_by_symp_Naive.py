from py2neo import Graph
from medical.query_process.keyword_selector import keyword_selector

"""
通过症状列表返回可能病名
"""


class QueBySympNaive:
    """通过对疾病与描述症状相连的次数统计,选取计数值高的疾病作为预测"""

    def __init__(self) -> None:
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))

    def get_prob_illness(self, symp_list: list, limit: int = -1) -> list:
        illness_count, illness_symp = {}, {}
        for symp in symp_list:
            # 构建查询语句，查找对应症状的病
            illness_query = (
                "match (n:疾病)-[r:病症]->(m:症状) where m.name='{}' return n".format(symp)
            )
            # 根据查找到的病，每次筛选到这个病，这个病的得分加一
            for illness_item in list(self.graph.run(illness_query)):
                illness_name = illness_item.get("n")["name"]
                # 判断字典里面是否有这个病，有的话该病score+1
                # 没有的话，在字典里面构建，然后设置score为1
                if illness_count.get(illness_name) is None:
                    illness_count[illness_name] = 1
                    illness_symp[illness_name] = {symp}
                else:
                    illness_count[illness_name] += 1
                    if symp not in illness_symp[illness_name]:
                        illness_symp[illness_name].add(symp)
        # 通过列表对score进行排序
        illness_sorted_list = list(illness_count.keys())
        illness_sorted_list.sort(
            reverse=True, key=lambda illness_name: illness_count[illness_name]
        )
        # 通过参数limit的限制来控制返回结果个数
        if (limit > 0) & (limit < len(illness_sorted_list)):
            illness_sorted_list = illness_sorted_list[:limit]
        # 返回一个列表，每个元素为tuple，tuple分别为病名和所含症状
        return [
            (illness_name, illness_symp[illness_name])
            for illness_name in illness_sorted_list
        ]

    def que_by_symp(self, input_str: str, limit: int = -1) -> list:
        # input_str 为输入的一段症状文本
        # limit为限制最后结果的个数
        # 通过调用get_prob_illness来实现返回结果
        # 而对于输入input_str的处理则是调用keyword_selector中的db_symp_select来完成：文本->症状列表->数据库中症状的列表 转换
        return self.get_prob_illness(keyword_selector.db_symp_select(input_str), limit)


# 朴素对症问疾全局实例
solver_naive = QueBySympNaive()

if __name__ == "__main__":
    str1 = "我最近身体不太舒服，总是觉得耳聋耳鸣腹痛腹泻头晕冒汗。这是怎么回事?"
    print(solver_naive.que_by_symp(str1, 5))
