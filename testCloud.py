# -*- coding = utf-8 -*-
# @Time : 2020/7/23 15:04
# @Author : Zrr
# @File : testCloud.py
# @Software : PyCharm

import jieba

import jieba                           #分词
from matplotlib import pyplot as plt   #绘图，数据可视化
from wordcloud import WordCloud        #词云
from PIL import Image                  #图片处理
import numpy as np                     #矩阵运算
import sqlite3                         #数据库

#准备好分词所需的语句
con = sqlite3.connect("movie.db")
cur = con.cursor()
sql = "select introduction from movie"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
# print(text)
    # print(item[0])
cur.close()
con.close()

cut = jieba.cut(text)
string = ' '.join(cut)
# print(string)
# print(len(string))

#设置遮罩图
img = Image.open(r'.\static\assets\img\girl.png')
img_array = np.array(img)   #将图片转化成数组

wc = WordCloud(
    background_color="white",
    mask=img_array,
    font_path="msyh.ttc"  #字体在 C:\Windows\Fonts\(微软雅黑)
)

wc.generate_from_text(string)  #放入词

plt.figure(1)
plt.imshow(wc)
plt.axis("off")

plt.show()  #显示生成的词云图片
#保存词云图片
plt.savefig(r'.\static\assets\img\wordcloud1.png',dpi=500)


# wc = WordCloud(
#     background_color="white",
#     max_words=200,
#     mask=img_array,
#     contour_width=3,
#     contour_color='steelblue',
#     font_path="msyh.ttc"  #字体在 C:\Windows\Fonts\(微软雅黑)
# )
#
# wc.generate_from_text(string)  #放入词
#
# #绘制图片
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.figure()
# plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
#
# plt.show()  #显示生成的词云图片

