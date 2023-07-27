import urllib.request
import urllib.parse
from lxml import etree
import pymongo
from fake_useragent import UserAgent
from max_cut import *

"""基于寻医问药的犯罪案件采集"""


class MedicalSpider:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn["medical"]
        self.col = self.db["data"]
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
            "药品推荐": "recommend_drug",
            "推荐": "recommend_eat",
            "忌食": "not_eat",
            "宜食": "do_eat",
            "症状": "symptom",
            "检查": "check",
            "成因": "cause",
            "预防措施": "prevent",
            "所属类别": "category",
            "简介": "desc",
            "名称": "name",
            "常用药品": "common_drug",
            "治疗费用": "cost_money",
            "并发症": "acompany",
        }
        self.dcuter = diseaseCutWords()
        self.icuter = inspectCutWords()
        self.scuter = symptomCutWords()

    """根据url，请求html"""

    def get_html(self, url):
        random_useragent = UserAgent().random
        headers = {"User-Agent": random_useragent}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("gbk")
        return html

    """测试"""

    def spider_main(self):
        for page in range(1, 20):
            try:
                basic_url = "http://jib.xywy.com/il_sii/gaishu/%s.htm" % page
                cause_url = "http://jib.xywy.com/il_sii/cause/%s.htm" % page
                prevent_url = "http://jib.xywy.com/il_sii/prevent/%s.htm" % page
                symptom_url = "http://jib.xywy.com/il_sii/symptom/%s.htm" % page
                inspect_url = "http://jib.xywy.com/il_sii/inspect/%s.htm" % page
                food_url = "http://jib.xywy.com/il_sii/food/%s.htm" % page
                drug_url = "http://jib.xywy.com/il_sii/drug/%s.htm" % page
                data = {}
                # 处理疾病节点和疾病的属性
                basic_info = self.basicinfo_spider(basic_url)
                data["category"], data["name"], data["desc"], attributes = (
                    basic_info["category"],
                    basic_info["name"],
                    basic_info["desc"],
                    basic_info["attributes"],
                )

                for attr in attributes:
                    attr_pair = attr.split("：")
                    if len(attr_pair) == 2:
                        key = attr_pair[0]
                        value = attr_pair[1]
                        if key in self.key_dict:
                            # 中文转英文
                            if key != "常用药品":
                                data[self.key_dict[key]] = value
                acompany = [
                    i
                    for i in self.dcuter.max_forward_cut(str(data["acompany"]))
                    if len(i) > 1
                ]
                data["acompany"] = acompany
                common_drugs = attributes[9].split("：")[1]
                data["common_drug"] = [i for i in common_drugs.split(" ") if i]
                # 处理原因和预防（简单）
                data["cause"] = self.common_spider(cause_url)
                data["prevent"] = self.common_spider(prevent_url)

                # 处理食物
                food_info = self.food_spider(food_url)
                if food_info:
                    data["do_eat"], data["not_eat"], data["recommend_eat"] = (
                        food_info["good"],
                        food_info["bad"],
                        food_info["recommend"],
                    )
                # 处理检查信息，可能有重复
                inspect_info = self.inspect_spider(inspect_url)
                inspectstring = "b".join(inspect_info)
                inspects = [
                    i for i in self.icuter.max_forward_cut(inspectstring) if len(i) > 1
                ]
                data["check"] = inspects

                # 处理症状信息，可能有重复
                symptom_info = self.symptom_spider(symptom_url)
                symptomstring = "b".join(symptom_info)
                symptoms = [
                    i for i in self.scuter.max_forward_cut(symptomstring) if len(i) > 1
                ]
                data["symptom"] = symptoms

                # 处理药品
                drug_info = self.drug_spider(drug_url)
                data["recommend_drug"] = list(
                    set([i.split("(")[-1].replace(")", "") for i in drug_info])
                )  # 推荐药品是括号中的名字
                data["drug_detail"] = drug_info

                self.col.insert_one(data)
                print(page, "成功爬取")
            except Exception as e:
                print(e, page, "爬取失败")
        return

    """基本信息解析"""

    def basicinfo_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath("//title/text()")[0]
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
        basic_data["name"] = title.split("的简介")[0]
        basic_data["desc"] = (
            "\n".join(desc)
            .replace("\r\n\t", "")
            .replace("\r\n\n\n", "")
            .replace(" ", "")
            .replace("\r\n", "\n")
        )
        basic_data["attributes"] = infobox
        return basic_data

    """drug解析"""

    def drug_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        drugs = [
            i.replace("\n", "").replace("\t", "").replace(" ", "")
            for i in selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')
        ]
        return drugs

    """food治疗解析"""

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
        symptoms_data["symptoms_detail"] = detail
        return detail

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
handler.spider_main()
