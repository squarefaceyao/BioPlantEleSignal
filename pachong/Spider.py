# -*- coding = utf-8 -*-
# @Time : 2020/7/21 23:50
# @Author : Zrr
# @File : Spider.py
# @Software : PyCharm

from bs4 import BeautifulSoup    #网页解析，获取数据
import re         #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定URL，获取网页数据
import xlwt       #进行excel操作
import sqlite3    #进行SQLite数据操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # #1、爬取网页
    datalist = []
    datalist = getData(baseurl)
    # savepath = ".\\豆瓣电影Top250.xls"  #(r'.\豆瓣电影Top250.xls')
    # #3、保存数据
    # saveData(datalist,savepath)  #保存在当前路径(.\\可以不写)
    # askURL(baseurl)
    dbpath = "movie.db"
    saveDataDB(datalist,dbpath)


#影片链接
findLink = re.compile(r'<a href="(.*?)">')
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?).jpg"',re.S)  #让换行符包含在字符中
#影片片名
# findTitle = re.compile(r'<span class="title">(.*)<span>')
findTitle = re.compile(r'<img alt="(.*?)"')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)  #保存获取到的网页源码

        #2、逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []
            item = str(item)

            link = re.findall(findLink,item)[0]
            data.append(link)  #影片链接

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)  #影片图片

            titles = re.findall(findTitle,item)[0]
            # if(len(titles) == 2):      #中英文名字
            #     ctitle = titles[0]
            data.append(titles)  #影片片名
            #     otitle = titles[1].replace("/","")  #去掉/
            #     data.append(otitle.text)
            # else:
            #     data.append(titles[0].text)
            #     data.append(' ')   #英文名留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)  #影片评分

            judge = re.findall(findJudge,item)[0]
            data.append(judge)  #影片评价人数

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")   #去掉。
                data.append(inq)  #影片概况
            else:
                data.append(" ")  #留空

            bd = re.findall(findBd,item)[0]  #影片相关内容
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉换行
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())  #去掉前后的空格

            datalist.append(data)   #把处理好的一部电影的信息制作成列表放入datalist列表中

    # for i in datalist:
    #     print(i)
    return datalist


#修改header，发送post请求得到解码的网页源码
def askURL(url):
    head = {   #用户代理，模拟浏览器头部信息，伪装用户向豆瓣服务器发送信息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36"
    }

    request = urllib.request.Request(url,headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)  #发送请求
        html = response.read().decode("utf-8")   #读取并解码
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):   #错误编号
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)     #错误理由

    return html    #结果返回解码的网页源码


def init_db(dbpath):
    sql = '''
        create table movie
        (id integer primary key autoincrement,
        info_link text not null,
        pic_link text not null,
        cname text not null,
        score numeric,
        rated numeric,
        introduction text,
        info text
        );
    '''
    conn = sqlite3.connect(dbpath)  #打开或创建数据库文件
    c = conn.cursor()  #获取游标
    c.execute(sql)   #执行sql语句
    conn.commit()    #提交数据库操作
    conn.close()     #关闭数据库连接
    # print("建表成功")


def saveDataDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 3 or index == 4:
                continue
            data[index]= "'"+data[index]+"'"
        sql = '''
            insert into movie(
            info_link,pic_link,cname,score,rated,introduction,info)
             values(%s)
        ''' % ",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()





#保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  #创建工作表 可覆盖内容
    col = ("电影链接","图片链接","影片名","评分","评价数","概况","简介")
    for i in range(0,7):
        sheet.write(0,i,col[i])  #在第一行写入数据
    for i in range(0,250):
        # print("第%d条" % (i+1))
        data = datalist[i]
        for j in range(0,7):
            sheet.write(i+1,j,data[j])

    book.save(savepath)
    # print("save")


#当程序执行时
if __name__ == "__main__":
    main()
    print("爬虫成功")


'''
from bs4 import BeautifulSoup

file = open("https://movie.douban.com/top250?start=0","rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup("html.parser")

# 输出查看:
# for item in t:
#     print(item)

#find_all()
#查找所有的"a"标签
t = bs.find_all("a")
t = bs.find_all("a",limit=3) #限定数量

#正则表达式
#只要包含有"a"
import re
t = bs.find_all(re.compile("a"))

#kwargs参数
t = bs.find_all(id="xxx")
t = bs.find_all(class_="xxx")
t = bs.find_all(text="xxx") #文本

#css选择器
t = bs.select("title")  #标签
t = bs.select(".class")
t = bs.select("#id")
t = bs.select("a[class=xx]") #标签里的属性
t = bs.select("head > title") #子标签

t = bs.select(".class ~ .class1") #兄弟标签
print(t[0].get_text()) #只有一个元素可用[0].获取文本
'''