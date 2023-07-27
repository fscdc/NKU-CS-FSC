import urllib.request
import urllib.parse
from lxml import etree
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

random_useragent = UserAgent().random
headers = {"User-Agent": random_useragent}


# 获取疾病名称
def get_disease_name(page):
    try:
        url = "https://jib.xywy.com/il_sii/gaishu/%s.htm" % page
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("gbk")
        selector = etree.HTML(html)
        name = selector.xpath("//title/text()")[0].split("的简介")[0]
        print(page, url)
        return name
    except Exception as e:
        print(e, page, "该界面丢失(网站问题)")
        return None


with open("disease.txt", "w", encoding="utf-8") as file:
    with ThreadPoolExecutor(max_workers=16) as executor:
        pages = range(1, 11000)
        symptom_names = executor.map(get_disease_name, pages)

        for name in symptom_names:
            if name:
                file.write(name + "\n")
