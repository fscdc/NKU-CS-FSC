#!/usr/bin/env python3
# coding: utf-8


import csv
import urllib.request
import urllib.parse
from lxml import etree
import thulac
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from max_cut import *
import os


"""使用清华大学分词库 Thulac 对症状进行分词

输入几段描述症状的文字 data（列表），分词得到其中的症状
"""


def symptom_text_segmenter(data: list) -> list:
    # 使用现有症状语料
    keywords_file = "./symptom.txt"

    keywords_dict = []
    with open(keywords_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                keyword = line.split("\t")
                keywords_dict += keyword

    segmenter = thulac.thulac(seg_only=True)

    symptoms = []

    for text in data:
        seg_result = segmenter.cut(text, text=True)
        words = seg_result.split()
        for word in words:
            if word in keywords_dict:
                symptoms.append(word)
    return list(set(symptoms))


# 以字典形式输出至 csv 文件，确保只在文件创建时输出一次表头
def write_data_to_csv(file_path, data, fieldnames):
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf_8_sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


"""基于寻医问药网的医学资料采集"""


class MedicalSpider:
    def __init__(self):
        self.node_csv_file = "./data/node.csv"
        self.relation_csv_file = "./data/relation.csv"
        self.illness_csv_file = "./data/illness.csv"
        self.key_dict = {
            "医保疾病": "yibao_status",
            "患病比例": "get_prob",
            "易感人群": "easy_get",
            "传染方式": "get_way",
            "就诊科室": "cure_department",
            "治疗方式": "cure_way",
            "治疗周期": "cure_lasttime",
            "治愈率": "cured_prob",
            "药品明细": "drug_detail",
            "药品推荐": "recommand_drug",
            "推荐": "recommand_eat",
            "忌食": "not_eat",
            "宜食": "do_eat",
            "症状": "symptom",
            "检查": "check",
            "成因": "cause",
            "预防措施": "prevent",
            "所属类别": "category",
            "简介": "desc",
            "名称": "name",
            " 常用药品": "common_drug",  # 这里爬取的时候有个空格，太坑了
            "治疗费用": "cost_money",
            "并发症": "acompany",
        }
        # 对检查项目进行分词
        self.inspect_cuter = CutWords("./inspect.txt")
        self.disease_cuter = CutWords("./disease.txt")

    """根据 url，请求 html"""

    def get_html(self, url):
        # 随机 UA，反反爬虫
        # random_useragent = random.choice(search_engine_UA)
        random_useragent = UserAgent().random
        headers = {"User-Agent": random_useragent}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("gbk")
        return html

    """线程函数，并行执行单元"""

    def process_page(self, page):
        # 使用 data 作为字典参数，向 csv 文件中添加数据
        data = {}

        # 记录当前页是否爬取失败
        failed = False

        # 记录错误的来源
        error = []

        # 由于可能出现部分网页不规范的情况，需要放在 try 环境中，以防爬虫终止
        basic_url = "http://jib.xywy.com/il_sii/gaishu/%s.htm" % page
        cause_url = "http://jib.xywy.com/il_sii/cause/%s.htm" % page
        prevent_url = "http://jib.xywy.com/il_sii/prevent/%s.htm" % page
        symptom_url = "http://jib.xywy.com/il_sii/symptom/%s.htm" % page
        inspect_url = "http://jib.xywy.com/il_sii/inspect/%s.htm" % page
        food_url = "http://jib.xywy.com/il_sii/food/%s.htm" % page
        drug_url = "http://jib.xywy.com/il_sii/drug/%s.htm" % page

        """基本信息：疾病的种类、名称、描述等"""
        try:
            basic_info = self.basicinfo_spider(basic_url)
            data["category"], data["name"], data["desc"], attributes = (
                basic_info["category"],
                basic_info["name"],
                basic_info["desc"],
                basic_info["attributes"],
            )
        except:
            print("第 {} 页爬取失败".format(page))
            return

        """属性信息的提取"""
        try:
            # 使用冒号进行分词，将各个属性分出来
            # 这里已经把 treat 板块下的属性提取了，所以我们不需要爬取 treat 板块下的数据
            for attr in attributes:
                attr_pair = attr.split("：", 1)  # ! 太坑了，这里只能分一个冒号
                # print(attr_pair)
                if len(attr_pair) == 2:
                    key = attr_pair[0]
                    value = attr_pair[1]
                    # 中文转英文
                    if key in self.key_dict:
                        data[self.key_dict[key]] = value
                        # 去除空格、回车
                        if self.key_dict[key] in [
                            "yibao_status",
                            "get_prob",
                            "easy_get",
                            "get_way",
                            "cure_lasttime",
                            "cured_prob",
                        ]:
                            data[self.key_dict[key]] = (
                                value.replace(" ", "")
                                .replace("\t", "")
                                .replace("\r", "")
                                .replace("\n", "")
                                .replace("\xa0", "")
                            )
                        # 按空格、顿号分词
                        if self.key_dict[key] in [
                            "cure_department",
                            "cure_way",
                            "common_drug",
                        ]:
                            split_by_space = value.split(" ")  # 按空格分词
                            data[self.key_dict[key]] = [
                                sub_item.strip()
                                for item in split_by_space
                                for sub_item in item.split("、")
                                if sub_item.strip()
                            ]

            """我们现在还需要对并发症进行分词"""
            if data["acompany"]:
                data["acompany"] = [
                    i
                    for i in self.disease_cuter.max_forward_cut(str(data["acompany"]))
                    if len(i) > 1
                ]
        except:
            error += ["疾病的部分属性不存在"]
            failed = True

        """发病原因"""
        try:
            data["cause"] = self.common_spider(cause_url)
        except:
            error += ["发病原因不存在"]
            failed = True

        """预防措施"""
        try:
            data["prevent"] = self.common_spider(prevent_url)
        except:
            error += ["预防措施不存在"]
            failed = True

        """症状以及具体描述"""
        try:
            data["symptoms"], data["symptoms_detail"] = self.symptom_spider(symptom_url)

            # 症状关键词需要进行 NLP 分词提取
            data["symptoms"] = symptom_text_segmenter(data["symptoms_detail"])
        except:
            error += ["症状以及具体描述不存在"]
            failed = True

        """检查项目"""
        try:
            inspect_info = self.inspect_spider(inspect_url)
            inspectstring = "b".join(inspect_info)
            inspects = [
                i
                for i in self.inspect_cuter.max_forward_cut(inspectstring)
                if len(i) > 1
            ]
            data["check"] = inspects
        except:
            error += ["检查项目不存在"]
            failed = True

        """食物"""
        try:
            food_info = self.food_spider(food_url)
            if food_info:
                data["do_eat"], data["not_eat"], data["recommend_eat"] = (
                    food_info["good"],
                    food_info["bad"],
                    food_info["recommend"],
                )
        except:
            error += ["食物信息不存在"]
            failed = True

        """药品"""
        try:
            drug_info = self.drug_spider(drug_url)
            data["recommend_drug"] = list(
                set([i.split("(")[-1].replace(")", "") for i in drug_info])
            )
            data["drug_detail"] = drug_info
        except:
            error += ["药品信息不存在"]
            failed = True

        # 删除 data 中的 symptoms_detail，因为我们并不需要提取这一属性
        # 这里的 try 只是防止 data 中没有 symptoms_detail，并不需要更新错误信息 error
        try:
            del data["symptoms_detail"]
        except:
            pass

        if failed:
            if data:
                print("第 {} 页爬取部分失败，原因有：".format(page), str("，".join(error)))
            else:
                print("第 {} 页爬取失败".format(page))
        else:
            print("第 {} 页爬取成功".format(page))

        return data

    """清除掉现有的 csv 文件，方便之后重新以追加形式写入新 csv 文件中"""

    def clear_file(self, file_path):
        try:
            os.remove(file_path)
        except:
            pass

    """主要函数"""

    def parallelize_processing(self, num_pages, max_workers=None):
        # 清除掉现有的 csv 文件
        self.clear_file(self.node_csv_file)
        self.clear_file(self.relation_csv_file)
        self.clear_file(self.illness_csv_file)

        header_node = [
            "label",
            "name",
        ]
        header_relation = [
            "label",
            "start",
            "end",
        ]
        header_illness = [
            "label",
            "name",
            "insurance",
            "easy_get",
            "get_way",
            "cure_time",
            "cured_prob",
            "cost_money",
            "cause",
            "prevent",
            "desc",
            "get_prob",
        ]

        """采用 ThreadPoolExecutor 进行多线程加速"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交每个页面的处理任务到线程池
            results = executor.map(self.process_page, range(1, num_pages + 1))

            # 将结果写入到 csv 文件中，results 是这一组线程得到的所有结果
            for data in results:
                node_list = []
                relation_list = []
                illness_list = []

                """疾病"""
                try:
                    illness_node = {
                        "label": "疾病",
                        "name": data["name"],
                        "insurance": data["yibao_status"],
                        "easy_get": data["easy_get"],
                        "get_way": data["get_way"],
                        "cure_time": data["cure_lasttime"],
                        "cured_prob": data["cured_prob"],
                        "cost_money": data["cost_money"],
                        "cause": data["cause"],
                        "prevent": data["prevent"],
                        "desc": data["desc"],
                        "get_prob": data["get_prob"],
                    }
                    illness_list.append(illness_node)
                except:
                    pass

                """节点及关系"""
                # 治疗方式
                try:
                    for name in data["cure_way"]:
                        cure_way_node = {"label": "治疗方式", "name": name}
                        node_list.append(cure_way_node)
                        cure_way_relation = {
                            "label": "治疗",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(cure_way_relation)
                except:
                    pass

                # 推荐吃的食物
                try:
                    for name in data["recommend_eat"]:
                        food_node = {"label": "食物", "name": name}
                        node_list.append(food_node)
                        food_relation = {
                            "label": "推荐吃",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(food_relation)
                except:
                    pass

                # 忌吃的食物
                try:
                    for name in data["not_eat"]:
                        food_node = {"label": "食物", "name": name}
                        node_list.append(food_node)
                        food_relation = {
                            "label": "忌吃",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(food_relation)
                except:
                    pass

                # 宜吃的食物
                try:
                    for name in data["do_eat"]:
                        food_node = {"label": "食物", "name": name}
                        node_list.append(food_node)
                        food_relation = {
                            "label": "宜吃",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(food_relation)
                except:
                    pass

                # 推荐药物
                try:
                    for name in data["recommend_drug"]:
                        drug_node = {"label": "药物", "name": name}
                        node_list.append(drug_node)
                        drug_relation = {
                            "label": "推荐药物",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(drug_relation)
                except:
                    pass

                # 常见药物
                try:
                    for name in data["common_drug"]:
                        drug_node = {"label": "药物", "name": name}
                        node_list.append(drug_node)
                        drug_relation = {
                            "label": "常见药物",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(drug_relation)
                except:
                    pass

                # 并发症
                try:
                    for name in data["acompany"]:
                        illness_relation = {
                            "label": "并发症",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(illness_relation)
                except:
                    pass

                # 症状
                try:
                    for name in data["symptoms"]:
                        symptoms_node = {"label": "症状", "name": name}
                        node_list.append(symptoms_node)
                        symptoms_relation = {
                            "label": "病症",
                            "start": data["name"],
                            "end": name,
                        }
                        relation_list.append(symptoms_relation)
                except:
                    pass

                # 科室，包括细分的科室
                try:
                    depart_name = data["cure_department"]
                    # 添加直连的科室（如果有多个科室，取最细粒度的），office 是细粒度的
                    cure_office_node = {"label": "科室"}
                    # 最多只可能有两个科室
                    if len(depart_name) > 1:
                        cure_office_node["name"] = depart_name[1]
                    else:
                        cure_office_node["name"] = depart_name[0]

                    node_list.append(cure_office_node)

                    # 如果有两个科室，那么添加从属关系
                    if len(depart_name) > 1:
                        # 先添加节点，department 表示较为粗粒度的科室
                        cure_department_node = {
                            "label": "科室",
                            "name": depart_name[0],
                        }
                        node_list.append(cure_department_node)

                        # 添加科室从属关系：细粒度的科室 -[从属]-> 粗粒度的科室
                        belong_relation = {
                            "label": "科室从属",
                            "start": cure_office_node["name"],
                            "end": cure_department_node["name"],
                        }
                        relation_list.append(belong_relation)

                    # 添加就诊科室关系：疾病名称 -[就诊]-> 细粒度的科室
                    office_go_for_relation = {
                        "label": "就诊科室",
                        "start": data["name"],
                        "end": cure_office_node["name"],
                    }
                    relation_list.append(office_go_for_relation)
                except:
                    pass

                # 检查项目
                try:
                    for check_item in data["check"]:
                        check_item_node = {
                            "label": "检查",
                            "name": check_item,
                        }
                        node_list.append(check_item_node)
                        check_method_relation = {
                            "label": "检查项目",
                            "start": data["name"],
                            "end": check_item,
                        }
                        relation_list.append(check_method_relation)
                except:
                    pass

                """以追加形式写入文件"""
                # 写入节点
                for data in node_list:
                    write_data_to_csv(self.node_csv_file, data, header_node)

                # 写入关系
                for data in relation_list:
                    write_data_to_csv(self.relation_csv_file, data, header_relation)

                # 写入疾病
                for data in illness_list:
                    write_data_to_csv(self.illness_csv_file, data, header_illness)

    """基本信息解析"""

    def basicinfo_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath("//div[@class='jb-name fYaHei gre']/text()")[0]
        category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
        infobox = []
        for p in ps:
            info = (
                p.xpath("string(.)")
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
            infobox.append(info)
        basic_data = {}
        basic_data["category"] = category
        basic_data["name"] = title
        basic_data["desc"] = (
            "\n".join(desc)
            .replace("\r\n\t", "")
            .replace("\r\n\n\n", "")
            .replace(" ", "")
            .replace("\r\n", "\n")
        )
        basic_data["attributes"] = infobox
        return basic_data

    """drug 药物治疗解析"""

    def drug_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        drugs = [
            i.replace("\n", "").replace("\t", "").replace(" ", "")
            for i in selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')
        ]
        return drugs

    """food 食物解析"""

    def food_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
        try:
            food_data = {}
            food_data["good"] = divs[0].xpath("./div/p/text()")
            food_data["bad"] = divs[1].xpath("./div/p/text()")
            food_data["recommend"] = divs[2].xpath("./div/p/text()")
        except:
            return {}

        return food_data

    """症状信息解析"""

    def symptom_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        symptoms = selector.xpath('//a[@class="gre" ]/text()')
        ps = selector.xpath("//p")
        detail = []
        for p in ps:
            info = (
                p.xpath("string(.)")
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
            detail.append(info)
        symptoms_data = {}
        symptoms_data["symptoms"] = symptoms
        symptoms_data["symptoms_detail"] = detail
        return symptoms, detail

    """检查信息解析"""

    def inspect_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        inspects = selector.xpath(
            '//div[@class="jib-articl fr f14 jib-lh-articl"]/p/text()'
        )
        return inspects

    """通用解析模块"""

    def common_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath("//p")
        infobox = []
        for p in ps:
            info = (
                p.xpath("string(.)")
                .replace("\r", "")
                .replace("\n", "")
                .replace("\xa0", "")
                .replace("   ", "")
                .replace("\t", "")
            )
            if info:
                infobox.append(info)
        return "\n".join(infobox)


handler = MedicalSpider()
handler.parallelize_processing(20)
