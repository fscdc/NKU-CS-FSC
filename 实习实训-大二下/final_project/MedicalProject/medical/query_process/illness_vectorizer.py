import os
import csv
import joblib
import random
from py2neo import Graph
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

# 全部疾病名(导入数据库的原始数据)
filepath_illness_name = "./medical/data/all_illness_name.csv"
# 疑难杂症名录(全部疾病名的子集)
filepath_rare_illness_name = "./medical/data/rare_illness_name.csv"

# 请保证以下4个文件同时存在且数据匹配，否则将4者删除运行
# 疑难杂症对应关联的症状
filepath_rare_illness_symp = "./medical/data/rare_illness_symp.txt"
# TFIDF模型存储数据
filepath_tfidf_model = "./medical/data/tfidf_model.joblib"
# PCA模型存储数据
filepath_pca_model = "./medical/data/pca_model.joblib"
# 疑难杂症特征向量矩阵
filepath_rare_illness_matrix = "./medical/data/rare_illness_matrix.joblib"


class IllnessVectorizer:
    """将疾病根据关联的症状向量化"""

    def __init__(self, vec_dim_limit: int) -> None:
        if vec_dim_limit <= 0:
            raise ValueError("向量维数应为正数")
        self.graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))
        # 读取疑难杂症
        self.rare_illness = []
        with open(file=filepath_rare_illness_name, encoding="utf-8") as fp:
            rare_illness_rows = csv.DictReader(fp)
            for rare_illness_row in rare_illness_rows:
                self.rare_illness.append(rare_illness_row["name"])
        if len(self.rare_illness) == 0:
            # 读取为空则创建疑难杂症数据文件并重新读取
            self.select_difficult_illness()
            with open(file=filepath_rare_illness_name, encoding="utf-8") as fp:
                rare_illness_rows = csv.DictReader(fp)
                for rare_illness_row in rare_illness_rows:
                    self.rare_illness.append(rare_illness_row["name"])
        # 读取/计算疾病向量化模型&疾病向量矩阵
        self.symp_doc = []
        self.tfidf_model = TfidfVectorizer()
        self.pca_model = PCA(n_components=vec_dim_limit)
        self.rare_illness_matrix = []
        finish_read_flag = False
        if os.path.isfile(filepath_rare_illness_symp):
            self.rare_illness_matrix = joblib.load(filepath_rare_illness_matrix)
            # 若已存在的疾病特征矩阵的特征数与当前指定特征数一致则读取先前计算结果，否则不读取并在后文重新计算
            if len(self.rare_illness_matrix[0]) == vec_dim_limit:
                with open(filepath_rare_illness_symp, "r", encoding="utf-8") as fp:
                    while True:
                        symps_row = fp.readline()
                        if not symps_row:
                            break
                        self.symp_doc.append(symps_row.replace("\n", ""))
                self.tfidf_model = joblib.load(filepath_tfidf_model)
                self.pca_model = joblib.load(filepath_pca_model)
                finish_read_flag = True
        if not finish_read_flag:
            self.symp_doc = [
                " ".join(self.get_illness_symp(rare)) for rare in self.rare_illness
            ]
            with open(filepath_rare_illness_symp, "w", encoding="utf-8") as fp:
                for symps_row in self.symp_doc:
                    fp.write(symps_row)
                    fp.write("\n")
            self.rare_illness_matrix = self.tfidf_model.fit_transform(self.symp_doc)
            joblib.dump(self.tfidf_model, filepath_tfidf_model)
            # 判断制定特征数的合法性，不合法则修正为合法的最大值
            max_vec_dim = min(self.rare_illness_matrix.shape[1], len(self.rare_illness))
            if max_vec_dim < vec_dim_limit:
                print(
                    "设定的向量维数{}超出合法维数上限{}，已自动修正为合法维数上限".format(
                        vec_dim_limit, max_vec_dim
                    )
                )
                vec_dim_limit = max_vec_dim
                self.pca_model = PCA(vec_dim_limit)
            self.rare_illness_matrix = self.rare_illness_matrix.toarray()
            self.rare_illness_matrix = self.pca_model.fit_transform(
                self.rare_illness_matrix
            )
            joblib.dump(self.pca_model, filepath_pca_model)
            joblib.dump(self.rare_illness_matrix, filepath_rare_illness_matrix)

    def select_difficult_illness(self, num=8000) -> None:
        """
        从全部疾病中挑选疑难杂症,num为挑选的疑难杂症数量
        """
        # 挑选出的疑难杂症编号列表
        L = random.sample(range(0, 8800), num)
        f_illness = open(filepath_illness_name, "r", encoding="UTF-8-sig")
        illness_rows = csv.DictReader(f_illness)
        # 疑难杂症在疑难杂症中的编号与在所有疾病中的编号
        cur, id = 0, 0
        header = ["curid", "id", "name"]
        output_list = []
        for info in illness_rows:
            if cur == num:
                break
            if id in L:
                ill_dict = {"curid": cur, "id": id, "name": info["name"]}
                output_list.append(ill_dict)
                cur += 1
                id += 1
            else:
                id += 1
        # 导出疑难杂症病名文件
        with open(
            filepath_rare_illness_name, "w", newline="", encoding="utf_8_sig"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for i in output_list:
                writer.writerow(i)

    def get_illness_symp(self, name: str) -> list:
        """查询与指定症状相关联的疾病并返回其列表"""
        symptom_query = "match (n:疾病)-[r:病症]->(m:症状) where n.name='{}' return m".format(
            name
        )
        symptom_list = []
        for symptom_item in list(self.graph.run(symptom_query)):
            symptom_node = symptom_item.get("m")
            symptom_list.append(symptom_node["name"])
        return symptom_list

    def calculate_illness_vector(self, symp_list: list):
        """根据已训练的tfidf和pca模型将用户描述的症状列表转化为特征向量"""
        return self.pca_model.transform(
            self.tfidf_model.transform([" ".join(symp_list)]).toarray()
        )


# 疾病向量化工具全局实例
illness_vectorizer = IllnessVectorizer(80)

if __name__ == "__main__":
    iv = IllnessVectorizer(8)
    print(iv.calculate_illness_vector(["咳嗽", "乏力", "焦虑"]))
    for i in range(3):
        print(f"Document {i+1}:")
        print(iv.symp_doc[i])
        print(iv.rare_illness_matrix[i])
    pass
