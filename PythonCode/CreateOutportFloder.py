#该代码实现功能为:自动创建从今天以后的所有日期的文件夹

import os
import datetime

curPath = os.path.abspath(os.path.dirname(__file__))
today = datetime.date.today()
trDateNow = str(today)
print(curPath)  

import arrow
date_list = []
date_least = []
for year in [2022]:  # 年份
    start_date = '%s-1-1' % year
    a = 0
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_sum = 366
    else:
        days_sum = 365
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        date_list.append(b)

dateIndex = 0
for date in date_list:
    if trDateNow == str(date):    
        break
    dateIndex = dateIndex + 1    

for date in date_list[dateIndex:]:
    floderPath = curPath + os.sep + str(date)
    date_least.append(floderPath)
  
for floder in date_least:
    os.mkdir(floder)
    




