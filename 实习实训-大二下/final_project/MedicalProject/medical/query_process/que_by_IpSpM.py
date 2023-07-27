import os
import re
import csv
from pypinyin import lazy_pinyin
from py2neo import Graph

"""
根据疾病(Illness)、症状(Symptom)、药名(Medicine)三个模块的输入返回最可能得疾病列表
"""

# 所有疾病名
filepath_all_illness_name = "./medical/data/all_illness_name.csv"
# 所有症状名
filepath_all_symptom_name = "./medical/data/all_symptom_name.csv"
# 所有药品名
filepath_all_medicine_name = "./medical/data/all_medicine_name.csv"


class QueByIpSpM:
    """根据疾病、症状、药品三组关键词输入预测用户可能想查询的疾病"""

    def __init__(self) -> None:
        """疾病(Illness)、症状(Symptom)、药名(Medicine)3个文件读入"""
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))
        # 读取所有疾病名
        finish_read_flag = False
        self.illness_name = set()
        if os.path.isfile(filepath_all_illness_name):
            self.illness_name = self.read_csv_file(filepath_all_illness_name)
            if self.illness_name:
                finish_read_flag = True
        if not finish_read_flag:
            self.create_illness_file()
            self.illness_name = self.read_csv_file(filepath_all_illness_name)
        # 读取所有症状名
        finish_read_flag = False
        self.symptom_name = set()
        if os.path.isfile(filepath_all_symptom_name):
            self.symptom_name = self.read_csv_file(filepath_all_symptom_name)
            if self.symptom_name:
                finish_read_flag = True
        if not finish_read_flag:
            self.create_symptom_file()
            self.symptom_name = self.read_csv_file(filepath_all_symptom_name)
        # 读取所有药品名
        finish_read_flag = False
        self.medicine_name = set()
        if os.path.isfile(filepath_all_medicine_name):
            self.medicine_name = self.read_csv_file(filepath_all_medicine_name)
            if self.medicine_name:
                finish_read_flag = True
        if not finish_read_flag:
            self.create_medicine_file()
            self.medicine_name = self.read_csv_file(filepath_all_medicine_name)
        print("finish init")

    def read_csv_file(self, filepath: str) -> set:
        """读取对应csv文件并返回集合形式"""
        csv_data = set()
        with open(file=filepath, encoding="utf-8") as fp:
            csv_rows = csv.DictReader(fp)
            for csv_row in csv_rows:
                csv_data.add(csv_row["name"])
        return csv_data

    def create_illness_file(self) -> None:
        """若不存在则创建所有疾病的病名csv文件，会在构造函数中调用"""
        # 查询所有疾病
        query = "match (n:疾病) return n"
        illness_items = self.graph.run(query)
        id = 0
        header = ["id", "name"]
        output_list = []
        # 遍历查询结果，封装成字典放入列表
        for illness_item in list(illness_items):
            name = illness_item.get("n")["name"]
            ill_dict = {"id": id, "name": name}
            output_list.append(ill_dict)
            id += 1

        # 将列表的结果写入文件中
        with open(
            filepath_all_illness_name, "w", newline="", encoding="utf_8_sig"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for i in output_list:
                writer.writerow(i)

    def create_symptom_file(self) -> None:
        """若不存在则创建所有症状名称的csv文件，会在构造函数中调用"""
        # 查询所有症状
        query = "match (n:症状) return n"
        illness_items = self.graph.run(query)
        id = 0
        header = ["id", "name"]
        output_list = []
        # 遍历查询结果，封装成字典放入列表
        for illness_item in list(illness_items):
            name = illness_item.get("n")["name"]
            ill_dict = {"id": id, "name": name}
            output_list.append(ill_dict)
            id += 1

        # 将列表的结果写入文件中
        with open(
            filepath_all_symptom_name, "w", newline="", encoding="utf_8_sig"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for i in output_list:
                writer.writerow(i)

    def create_medicine_file(self) -> None:
        """若不存在则创建所有药品名称的csv文件，会在构造函数中调用"""
        # 查询所有药物
        query = "match (n:药物) return n"
        illness_items = self.graph.run(query)
        id = 0
        header = ["id", "name"]
        output_list = []
        # 遍历查询结果，封装成字典放入列表
        for illness_item in list(illness_items):
            name = illness_item.get("n")["name"]
            ill_dict = {"id": id, "name": name}
            output_list.append(ill_dict)
            id += 1

        # 将列表的结果写入文件中
        with open(
            filepath_all_medicine_name, "w", newline="", encoding="utf_8_sig"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for i in output_list:
                writer.writerow(i)

    def get_score(self, src_str: str, des_str: str):
        # 评分标准为匹配度越高，得分越低
        # 原因是为了与之前文件中写过的编辑距离的分数规则相同
        # 根据两个输入字符长度判断用哪个去匹配哪个
        if len(src_str) < len(des_str):
            src, des = src_str, des_str
        else:
            src, des = des_str, src_str
        # 如果src为des字串，直接返回src长度相关的分
        # 再乘上一个src与des长度的比来实现越靠近全匹配，分数效果越好
        if src in des:
            return -3.5 * len(src) * len(src) / len(des)

        # 如果字匹配不到，匹配音
        src_pinyin_list = lazy_pinyin(src)
        des_pinyin_list = lazy_pinyin(des)

        all_src_pinyin = ""
        all_des_pinyin = ""
        for des_pinyin in des_pinyin_list:
            all_des_pinyin += des_pinyin
        # 根据拼音的结果来反馈，同样也需要一个sec/des来进行调整
        score = 0
        for src_pinyin in src_pinyin_list:
            all_src_pinyin += src_pinyin
            if src_pinyin in des_pinyin_list:
                score += 0.5
        # 如果src连起来的音在des里面，则返回拼音匹配得分
        if all_src_pinyin in all_des_pinyin:
            return -1.0 * len(src) * len(src) / len(des)
        # 如果不满足拼音字串和字符字串，则返回每个音节在其中的得分
        return -score

    def select_by_illness(self, input_illness_list: list) -> dict:
        """返回所有疾病按照用户给定疾病列表的匹配度值的字典"""
        # 建立每个疾病的字典，值为得分
        origin_illness_score = {
            precise_illness: 0 for precise_illness in self.illness_name
        }
        # 对每个疾病进行匹配，通过get_score来计算得分
        for precise_illness in self.illness_name:
            for input_illness in input_illness_list:
                origin_illness_score[precise_illness] += self.get_score(
                    input_illness, precise_illness
                )
        # 通过对列表进行排序，来反馈匹配程度的顺序
        prob_illness_list = list(self.illness_name)
        prob_illness_list.sort(key=lambda ill: origin_illness_score[ill])
        # 限制结果的个数，来提高程序运行效率
        prob_illness_list = prob_illness_list[
            : min(min(30, len(input_illness_list) ** 2 + 5), len(prob_illness_list))
        ]
        # print(prob_illness_list)

        # 设置并发症权重
        complitcation_illness_weight = 0.2
        illness_score = origin_illness_score
        for ill in prob_illness_list:
            # 找到其对应并发症，再给并发症加上一定分数，这里认为患者可能会有某个疾病的并发症
            illness_query = (
                "match (n:疾病)-[r:并发症]->(m:疾病) where n.name='{}' return m".format(ill)
            )
            for illness_item in list(self.graph.run(illness_query)):
                illness_name = illness_item.get("m")["name"]
                illness_score[illness_name] += (
                    origin_illness_score[illness_name] * complitcation_illness_weight
                )
        # 返回结果为疾病以及其分数的字典
        # print("finish illness")
        return illness_score

    def select_by_symptom(self, input_symptom_list: list) -> dict:
        """返回所有疾病按照用户给定症状列表的匹配度值的字典"""
        # 建立每个症状的字典，值为匹配得分
        symptom_score = {precise_symptom: 0 for precise_symptom in self.symptom_name}
        # 对每个症状进行匹配，通过get_score来计算得分
        for precise_symptom in self.symptom_name:
            for input_symptom in input_symptom_list:
                symptom_score[precise_symptom] += self.get_score(
                    input_symptom, precise_symptom
                )
        # 通过对列表进行排序，来反馈症状匹配程度的顺序
        prob_symptom_list = list(self.symptom_name)
        prob_symptom_list.sort(key=lambda symp: symptom_score[symp])
        # 限制结果的个数，来提高程序运行效率
        prob_symptom_list = prob_symptom_list[
            : min(min(30, len(input_symptom_list) ** 2 + 5), len(prob_symptom_list))
        ]
        # print(prob_symptom_list)
        # 通过查找匹配好的症状，来反馈匹配度最高的几个症状所对应的疾病
        illness_score = {precise_illness: 0 for precise_illness in self.illness_name}
        for symp in prob_symptom_list:
            # 根据症状查找疾病，然后对该疾病加上一定的分数
            illness_query = (
                "match (n:症状)-[r:病症]-(m:疾病) where n.name='{}' return m".format(symp)
            )
            for illness_item in list(self.graph.run(illness_query)):
                illness_name = illness_item.get("m")["name"]
                illness_score[illness_name] += symptom_score[symp]
        # 返回结果为疾病所对应分数的字典
        # print("finish symptom")
        return illness_score

    def select_by_medicine(self, input_medicine_list: list) -> dict:
        """返回所有疾病按照用户给定药品列表的匹配度值的字典"""
        # 建立每个药物的字典，值为匹配得分
        medicine_score = {
            precise_medicine: 0 for precise_medicine in self.medicine_name
        }
        # 对每个症状进行匹配，通过get_score来计算得分
        for precise_medicine in self.medicine_name:
            for input_medicine in input_medicine_list:
                medicine_score[precise_medicine] += self.get_score(
                    input_medicine, precise_medicine
                )
        # 通过对列表进行排序，来反馈症状匹配程度的顺序
        prob_medicine_list = list(self.medicine_name)
        prob_medicine_list.sort(key=lambda medi: medicine_score[medi])
        # 限制结果的个数，来提高程序运行效率
        prob_medicine_list = prob_medicine_list[
            : min(min(30, len(input_medicine_list) ** 2 + 5), len(prob_medicine_list))
        ]
        # print(prob_medicine_list)
        # 通过查找匹配好的药物，来反馈匹配度最高的几个症状所对应的疾病
        illness_score = {precise_illness: 0 for precise_illness in self.illness_name}
        for medi in prob_medicine_list:
            # 根据药物查找疾病，然后对该疾病加上一定的分数
            illness_query = "match (n:药物)-[r]-(m:疾病) where n.name='{}' return m".format(
                medi
            )
            for illness_item in list(self.graph.run(illness_query)):
                illness_name = illness_item.get("m")["name"]
                illness_score[illness_name] += medicine_score[medi]
        # 返回结果为疾病所对应分数的字典
        # print("finish medicine")
        return illness_score

    def select_by_all_info(
        self,
        input_illness: str,
        input_symptom: str,
        input_medicine: str,
        limit: int = 10,
    ) -> list:
        """返回所有疾病按照用户给定疾病、症状、药品列表的匹配度值的加权降序排序的列表"""
        # 通过正则匹配对输入信息进行拆分
        delimeter = r"\W"
        input_illness_list = re.split(delimeter, input_illness)
        input_symptom_list = re.split(delimeter, input_symptom)
        input_medicine_list = re.split(delimeter, input_medicine)
        # 设置最后计算结果的权重，三种信息：疾病，症状，药物
        # 这里认为那种信息提供信息越多，占比就越大，权重应该越高
        tot_info_count = (
            len(input_illness_list) + len(input_symptom_list) + len(input_medicine_list)
        )
        illness_weight = len(input_illness_list) / tot_info_count
        symptom_weight = len(input_symptom_list) / tot_info_count
        medicine_weight = len(input_medicine_list) / tot_info_count

        # 获取每种信息的匹配后，返回疾病得分的结果
        score_by_illness = self.select_by_illness(input_illness_list)
        score_by_symptom = self.select_by_symptom(input_symptom_list)
        score_by_medicine = self.select_by_medicine(input_medicine_list)
        # 通过返回的字典和每种信息的权重，来计算三种信息整合后每种疾病的得分
        score_over_all = {
            precise_illness: score_by_illness[precise_illness] * illness_weight
            + score_by_symptom[precise_illness] * symptom_weight
            + score_by_medicine[precise_illness] * medicine_weight
            for precise_illness in self.illness_name
        }
        # 通过列表进行排序
        prob_illness_list = list(self.illness_name)
        prob_illness_list.sort(key=lambda illness: score_over_all[illness])
        # 根据输入参数limit的值来限制最后返回结果
        if (0 < limit) & (limit < len(prob_illness_list)):
            prob_illness_list = prob_illness_list[:limit]
        # 返回一个列表，为可能还有的疾病，可能性越大越靠前
        return [(prob_illness, set()) for prob_illness in prob_illness_list]


# 朴素三项联检全局实例
solver_IpSpM = QueByIpSpM()

if __name__ == "__main__":
    input_illness = "感冒 非典 流行"
    input_symptom = "嗜睡 发烧 咳嗽"
    input_medicine = "感冒灵"
    print(
        solver_IpSpM.select_by_all_info(
            input_illness, input_symptom, input_medicine, 10
        )
    )
