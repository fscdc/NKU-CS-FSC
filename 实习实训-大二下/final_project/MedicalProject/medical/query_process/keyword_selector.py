import re
import csv
import jieba

"""
筛选出症状关键词
"""

# 存在Neo4j数据库中的所有症状名
filepath_db_symp_name = "./medical/data/db_symp_name.csv"
# 爬取到的所有症状名(未分词)
filepath_extended_symp_name = "./medical/data/extended_symp_name.csv"
# 停用词表
filepath_stop_words = "./medical/data/stop_words.csv"


class KeywordSelector:
    def __init__(self) -> None:
        # 读取全部症状和数据库中的症状
        self.db_symp = []
        with open(file=filepath_db_symp_name, encoding="utf-8") as fp:
            symp_rows = csv.DictReader(fp)
            for symp_row in symp_rows:
                self.db_symp.append(symp_row["name"])

        self.extended_symp = set()
        with open(file=filepath_extended_symp_name, encoding="utf-8") as fp:
            while True:
                symp_row = fp.readline()
                if not symp_row:
                    break
                self.extended_symp.add(symp_row)

        # 加载停用词
        self.stop_words = set()
        with open(file=filepath_stop_words, encoding="utf-8") as fp:
            while True:
                stop_word_row = fp.readline()
                if not stop_word_row:
                    break
                self.stop_words.add(stop_word_row)

    def extended_symp_select(self, input_str: str) -> list:
        # 通过症状比较完善的文件完成筛查
        # 这个筛查的首先筛查出较为模糊的症状
        # 筛查规则为如果是某个症状的字串就被筛选出来
        input_str_list = re.split(r"\W", input_str)
        # 筛查的时候，如果是在停用词里面或者长度为一，那么不进行选取
        token_list = [
            token
            for single_input_str in input_str_list
            for token in jieba.lcut(single_input_str, cut_all=False)
            if (len(token) > 1) & (token not in self.stop_words)
        ]
        # 按照匹配规则构建结果
        desc_symp_list = []
        for token in token_list:
            for ext_symp in self.extended_symp:
                if token in ext_symp:
                    desc_symp_list.append(token)
                    break
        return desc_symp_list

    def get_score(self, src: str, des: str):
        # 得分函数，这里的得分规则为按照顺序匹配，匹配度越高得分越低
        # 需要明确的是，这里如果只有一个字匹配，而没有一个以上长度的词匹配，那么返回得分为0
        score = 0
        one = True
        for i in range(len(src)):
            for j in range(i + 1, len(src) + 1):
                if src[i:j] in des:
                    score += (j - i) * 1.0 * len(src[i:j]) / len(des)
                    if j - i > 1:
                        one = False
        if one:
            return 0
        return -score

    def db_symp_select(self, input_str) -> list:
        symp_list = []
        # print(self.extended_symp_select(input_str))
        # 根据extended_symp_select来获取要进行模糊匹配症状的列表
        for symp in self.extended_symp_select(input_str):
            # 判断长度是否为1，长度为1的字符不进行匹配
            if len(symp) == 1:
                continue
            # 设置分数的列表，根据get_score来获取score
            score_list = [0 for i in range(len(self.db_symp))]
            for i in range(len(self.db_symp)):
                if len(symp) < len(self.db_symp[i]):
                    score_list[i] = self.get_score(symp, self.db_symp[i])
                else:
                    score_list[i] = self.get_score(self.db_symp[i], symp)
            # 由于匹配效果越好，分数越低（为了与之前编辑距离的分数规则一样而采用分数越低匹配越好）
            # 查找分数最低的索引，为当前需要匹配症状的结果
            id = score_list.index(min(score_list))
            if score_list[id] < 0:
                symp_list.append(self.db_symp[id])
        return symp_list


keyword_selector = KeywordSelector()

if __name__ == "__main__":
    # test_fuzzy_guess('大楼病综合征')
    # str = "后背痛两天，深呼吸都疼"  # ['背痛', '呼吸衰竭']
    # str = "我最近身体不太舒服，总是觉得耳聋耳鸣腹痛腹泻头晕冒汗。这是怎么回事?"  # ['体癣', '水土不服', '耳聋', '耳鸣', '腹痛', '腹泻', '头晕']
    # str = "鼻窦炎鼻涕由黄转清，是好转还是严重了？"
    ks = KeywordSelector()
    print(ks.db_symp_select(str))
    pass
