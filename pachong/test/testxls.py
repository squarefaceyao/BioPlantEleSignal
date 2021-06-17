# -*- coding = utf-8 -*-
# @Time : 2020/7/22 14:40
# @Author : Zrr
# @File : testxls.py
# @Software : PyCharm

import xlwt

workbook = xlwt.Workbook(encoding="utf-8")  #创建workbook对象
worksheet = workbook.add_sheet('sheet1')  #创建工作表
worksheet.write(0,0,'hello')  #在第一行第一列写入数据hello
workbook.save("test.xls")
