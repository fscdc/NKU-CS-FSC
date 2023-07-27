import re
import csv
import jieba
import math
import random
from pypinyin import lazy_pinyin

# 全部疾病名文件
filepath_all_illness_name = "./medical/data/all_illness_name.csv"


class FuzzyGuess:
    """对用户输入的病名采取模糊匹配，猜测可能的准确病名"""

    def __init__(self) -> None:
        self.all_illness = []
        # 导入全部疾病名
        with open(file=filepath_all_illness_name, encoding="utf-8") as fp:
            illness_rows = csv.DictReader(fp)
            for illness_row in illness_rows:
                self.all_illness.append(illness_row["name"])

    def get_mini_edit_dist(self, src: str, des: str):
        """利用动态规划算法求源串(用户输入串)到目标串(准确病名串)的最小编辑代价"""
        # 若源串与目标串完全匹配，则无需编辑，且返回极小值用于平衡其他代价
        if src == des:
            return -100
        # 若源串为目标串子串，则无需编辑
        if src in des:
            return 0

        # 补空代价：使用空字符填充当前位置的编辑代价
        space_cost = 1
        # 字形失配代价：两个字符不相同的编辑代价
        unmatch_char_cost = 1
        # 拼音失配代价：在字形不同的基础上，拼音也不相同的编辑代价
        unmatch_pinyin_cost = 2
        # 长度差距代价：当源串和目标串不等长时，实际的总代价放缩比例
        srclen, deslen = len(src), len(des)
        len_cost_rate = max(srclen / deslen, 1)

        # 源串和目标串的拼音表示
        src_pinyin = "".join(lazy_pinyin("#".join(src))).split("#")
        des_pinyin = "".join(lazy_pinyin("#".join(des))).split("#")

        # 初始化边界条件，直接空字符填充
        mini_edit_dist = [[0 for i in range(deslen + 1)] for j in range(srclen + 1)]
        for i in range(srclen):
            mini_edit_dist[i + 1][0] = space_cost * (i + 1)
        for i in range(deslen):
            mini_edit_dist[0][i + 1] = space_cost * (i + 1)
        # 动态规划求解最小编辑代价
        for i in range(srclen):
            for j in range(deslen):
                # 直接从相邻状态采用空字符填充转移的代价
                mini_edit_dist[i + 1][j + 1] = space_cost + min(
                    mini_edit_dist[i][j + 1], mini_edit_dist[i + 1][j]
                )
                # 将当前两串对应位置字符比较，添加字形失配和拼音失配的代价
                mini_edit_dist[i + 1][j + 1] = min(
                    mini_edit_dist[i + 1][j + 1],
                    mini_edit_dist[i][j]
                    + (src[i] != des[j]) * unmatch_char_cost
                    + (src_pinyin[i] != des_pinyin[j]) * unmatch_pinyin_cost,
                )
        # 根据源串在目标串的相对长度占比，放缩总编辑代价得到实际编辑代价
        return mini_edit_dist[srclen][deslen] * len_cost_rate

    def get_score(self, src: str, des: str):
        """
        利用朴素子串包含比较计算源串到目标串的相关程度，
        为与动态规划最小编辑代价的排序方式一致，设定为分值越低，相关程度越高
        """
        # 源串是目标串的子串，则认为相关程度极大，设置系数较大为3.5
        # 若源串的长度越大，其成为目标串子串的概率越小，相关程度越大，
        # 故设定分值与源串长度线性相关
        if src in des:
            return -3.5 * len(src)
        # 源串和目标串的拼音形式
        src_pinyin_list, des_pinyin_list = lazy_pinyin(src), lazy_pinyin(des)
        all_src_pinyin, all_des_pinyin = "", ""
        for des_pinyin in des_pinyin_list:
            all_des_pinyin += des_pinyin
        # 当源串从字形上不属于目标串子串时，考虑其拼音形式是否存在子串包含关系
        score = 0
        for src_pinyin in src_pinyin_list:
            all_src_pinyin += src_pinyin
            # 每存在一个字符的拼音包含于目标串则累计分值
            if src_pinyin in des_pinyin_list:
                score -= 1
        # 源串拼音是目标串拼音的子串，则认为相关程度较大，设置系数中等为1.5
        if all_src_pinyin in all_des_pinyin:
            return -1.5 * len(src)
        # 源串可能存在部分字符与目标串相同，可能具有一定相关程度，
        # 若相同字符数越多，认为相关程度越大，返回上文累计值
        return score

    def get_guess_list(self, input_str: str, use_jieba: bool, limit: int = 10) -> list:
        """
        input_str为用户输入的待匹配模糊病名串,可使用非单词字符作为描述的分隔符,可以容忍少量的同音错字,如:"感燃 蛋白,综合症"；
        use_jieba选择是否采用jieba分词进而使用不同字串匹配算法估计编辑代价/相关程度；
        limit限制返回的预测用户可能想查询的准确疾病名称的数量；
        返回对用户可能想查询的准确疾病名称的预测列表(已按照编辑代价/相关程度分值升序排序)
        """
        # 初始化所有准确病名和用户输入模糊病名的编辑代价的列表,
        # 内嵌二元列表第一个元素表示疾病在all_illness_name.csv文件中的id,第二个元素表示编辑代价,初始化为极大值
        print(input_str)
        score_list = [[i, 10000] for i in range(len(self.all_illness))]
        # 不使用jieba分词时则采用动态规划求编辑代价的方法
        if not use_jieba:
            print("No")
            # 为充分利用用户输入的所有字段，每次匹配会合并为单个长串匹配
            # 为避免间隔字段的顺序对于编辑代价计算的影响，会随机若干组(至多10组)字段的不同排列顺序

            # 所有字段的列表，每次会随机重排
            token_list = list(set(re.split(r"\W", input_str)))
            # 不同随机重排次数
            max_shuffle_count = (
                10 if len(token_list) > 3 else math.factorial(len(token_list))
            )
            # 记录不同排列顺序避免重复
            shuffle_set = set()
            while len(shuffle_set) < max_shuffle_count:
                while "".join(token_list) in shuffle_set:
                    random.shuffle(token_list)
                shuffle_set.add("".join(token_list))
            # 对每个重排执行动态规划求解编辑代价并取所有重排代价的最小值
            for shuffled_tokens in shuffle_set:
                id = 0
                for illness_name in self.all_illness:
                    score_list[id][1] = min(
                        score_list[id][0],
                        self.get_mini_edit_dist(shuffled_tokens, illness_name),
                    )
                    id += 1
        # 使用jieba分词时则采用朴素子串包含比较求相关程度方法
        else:
            # 正则筛出所有非文本字符并使用jieba分词
            input_str = re.sub(r"\W", "", input_str)
            token_list = jieba.lcut_for_search(input_str)
            # 对每个分词段计算相关程度累加
            for token in token_list:
                id = 0
                for illness_name in self.all_illness:
                    score_list[id][1] += self.get_score(token, illness_name)
                    id += 1
        # 将所有疾病按照上述编辑代价/相关程度分值升序排序
        score_list.sort(key=lambda illness_item: illness_item[1])
        # 筛选编辑代价/相关程度分值最小的前limit个疾病作为返回结果
        count, result_list = 0, []
        for illness_item in score_list:
            if count == limit:
                break
            result_list.append(self.all_illness[illness_item[0]])
            count += 1
        return result_list


# 病名模糊匹配器全局实例
fuzzy_guess = FuzzyGuess()

if __name__ == "__main__":
    fg = FuzzyGuess()
    # '大楼α病,综-合 征β' '蛋白 新冠 冠状'
    print("Jieba")
    print(fg.get_guess_list("干冒 可搜", True))
    print("Split")
    print(fg.get_guess_list("干冒 可搜", False))
    pass
