import urllib.request
import urllib.parse
from lxml import etree
import re
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

random_useragent = UserAgent().random
headers = {"User-Agent": random_useragent}


# 获取症状名称函数
def get_symptom_name(page):
    try:
        url = "https://zzk.xywy.com/%s_gaishu.html" % page
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("gbk")
        selector = etree.HTML(html)
        name = selector.xpath('//div[@class="jb-name fYaHei gre"]/text()')[0]
        print(page, url)
        return name
    except Exception as e:
        print(e, page, "该界面丢失(网站问题)")
        return None


with open("symptom.txt", "w", encoding="utf-8") as file:
    with ThreadPoolExecutor(max_workers=16) as executor:
        pages = range(1, 6912)
        symptom_names = executor.map(get_symptom_name, pages)

        for name in symptom_names:
            if name:
                file.write(name + "\n")
