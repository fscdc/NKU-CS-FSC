import numpy as np

from medical.query_process.illness_vectorizer import illness_vectorizer
from medical.query_process.keyword_selector import keyword_selector


class QueBySympVecSim:
    """利用向量相似度预测用户想查询的疾病"""

    def get_similarity_cos(self, desc_vec: np.array) -> np.array:
        """余弦相似度"""
        # 矩阵向量内积
        similarity_vec = np.matmul(illness_vectorizer.rare_illness_matrix, desc_vec.T)
        # 除以模长单位化
        similarity_vec /= np.sqrt(
            np.sum(np.square(illness_vectorizer.rare_illness_matrix), axis=1)
        ).reshape(similarity_vec.shape[0], -1)
        similarity_vec /= np.sqrt(np.sum(np.square(desc_vec)))
        return similarity_vec

    def get_similarity_euc(self, desc_vec: np.array) -> np.array:
        """欧几里得相似度"""
        # 计算欧氏距离
        similarity_vec = np.sum(
            np.square(illness_vectorizer.rare_illness_matrix - desc_vec), axis=1
        )
        # 为与余弦相似度的比较方式统一(值越大相似度越高),规约到(0,1]范围
        similarity_vec = 1.0 / (1.0 + np.sqrt(similarity_vec))
        return similarity_vec

    def get_prob_illness(self, symp_list: list, limit: int = -1) -> list:
        desc_vec = illness_vectorizer.calculate_illness_vector(symp_list)
        # 余弦相似度
        simvec_cos = self.get_similarity_cos(desc_vec)
        # 欧几里得相似度
        simvec_euc = self.get_similarity_euc(desc_vec)
        # 合并两种相似度结果
        similarity_list = [
            (idx, simvec_cos[idx] * simvec_euc[idx])
            for idx in range(simvec_cos.shape[0])
        ]
        # 根据相似度降序排列
        similarity_list.sort(key=lambda item: item[1], reverse=True)
        rare_illness_list = [
            illness_vectorizer.rare_illness[similarity_list[idx][0]]
            for idx in range(len(similarity_list))
        ]
        # 筛选相似度最高的limit个疾病并返回
        if (limit > 0) & (len(similarity_list) > limit):
            rare_illness_list = rare_illness_list[:limit]
        rare_illness_list = [
            (
                rare_illness_name,
                set(
                    [
                        symp
                        for symp in illness_vectorizer.symp_doc[
                            illness_vectorizer.rare_illness.index(rare_illness_name)
                        ].split(" ")
                        if symp in symp_list
                    ]
                ),
            )
            for rare_illness_name in rare_illness_list
        ]
        return rare_illness_list

    def que_by_symp(self, input_str: str, limit: int = 10) -> list:
        """根据用户描述返回至多limit个相似度最高的疾病"""
        return self.get_prob_illness(keyword_selector.db_symp_select(input_str), limit)


# 向量相似度对症问疾全局实例
solver_vecsim = QueBySympVecSim()

if __name__ == "__main__":
    # input_str = "我想睡觉，嗜睡，咳嗽"
    input_str = "我最近发热畏寒、头痛"
    print(solver_vecsim.que_by_symp(input_str, 20))
    pass
