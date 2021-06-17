# -*- coding = utf-8 -*-
# @Time : 2020/7/22 14:19
# @Author : Zrr
# @File : test1.py
# @Software : PyCharm

from bs4 import BeautifulSoup

response = open("test1.html","rb")
html = response.read().decode("utf-8")
bs = BeautifulSoup(html,"html.parser")

t = bs.select(".item .title")
for link in t:
    print(link.text.strip())




