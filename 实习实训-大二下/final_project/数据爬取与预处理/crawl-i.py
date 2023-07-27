import urllib.request
import urllib.parse
from lxml import etree
import re
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

random_useragent = UserAgent().random
headers = {"User-Agent": random_useragent}


# 获取检查项目名称函数
def get_inspect_name(page):
    try:
        url = "http://jck.xywy.com/jc_%s.html" % page
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("gbk")
        selector = etree.HTML(html)
        name = selector.xpath('//div[@class="baby-weeks"]/div/strong/text()')[0]
        print(page, url)
        return name
    except Exception as e:
        print(e, page, "该界面丢失(网站问题)")
        return None


with open("inspect.txt", "w", encoding="utf-8") as file:
    with ThreadPoolExecutor(max_workers=16) as executor:
        pages = range(1, 3782)
        inspect_names = executor.map(get_inspect_name, pages)

        for name in inspect_names:
            if name:
                file.write(name + "\n")
