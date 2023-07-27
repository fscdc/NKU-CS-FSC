import jieba

from medical.query_process.que_by_IpSpM import QueByIpSpM

"""
根据疾病(Illness)、症状(Symptom)、药名(Medicine)三个模块的输入返回最可能得疾病列表
"""

# 停用词
filepath_stop_words = "./medical/data/stop_words.csv"


class QueByIpSpMPlus(QueByIpSpM):
    """在朴素三项联检的基础上,增加jieba分词,允许用户输入3组对应的描述性文本"""

    def __init__(self) -> None:
        super().__init__()
        # 读取停用词用于提升分词效果
        self.stop_words = self.read_csv_file(filepath_stop_words)

    def cut_word(self, input_str: str) -> list:
        """先用jieba分词，然后剔除单字和处于停用词表中的词"""
        words_after_cut = [
            token
            for token in jieba.lcut(input_str, cut_all=False)
            if (len(token) > 1) & (token not in self.stop_words)
        ]
        # print(words_after_cut)
        return words_after_cut

    def select_by_all_info(
        self,
        input_illness: str,
        input_symptom: str,
        input_medicine: str,
        limit: int = 10,
    ) -> list:
        """返回所有疾病按照用户给定疾病、症状、药品列表的匹配度值的加权降序排序的列表"""
        # jieba分词用户输入
        input_illness_list = self.cut_word(input_illness)
        input_symptom_list = self.cut_word(input_symptom)
        input_medicine_list = self.cut_word(input_medicine)
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

    pass


# Plus三项联检全局实例
solver_IpSpMPlus = QueByIpSpMPlus()

if __name__ == "__main__":
    # input_illness = "我曾怀孕，新冠阳性一次"
    # input_symptom = "我最近失眠，时常伴随恶心、呕吐"
    # input_medicine = "近期服用安眠药，吃连花清瘟胶囊"
    input_illness = "我曾患过感冒，非典流行的时候也感染过"
    input_symptom = "我最近嗜睡并且发烧，时常咳嗽"
    input_medicine = "感冒灵胶囊"
    print(
        solver_IpSpMPlus.select_by_all_info(
            input_illness, input_symptom, input_medicine, 10
        )
    )
