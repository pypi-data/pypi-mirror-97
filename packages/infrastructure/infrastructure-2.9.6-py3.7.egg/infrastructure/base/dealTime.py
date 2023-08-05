# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-09-09 15:05:51
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-01-28 15:20:50

import datetime
import time

def getWeek(onlyWeek=False):
	"""
		获取当前是第几周
		返回： float 年份.第几周 如 2020.3

		计算指定时间是当年第几周：

		1 import datetime
		2 datetime.date(2020, 10, 1).isocalendar()
		3 # (2020, 40, 4)：2020年10月1号是2020年第40周周4
	"""
	week = datetime.datetime.now().isocalendar() ## (2020, 37, 5)：当前时间是2002年第37周周五
	if not onlyWeek:
		rweek = str(week[0])+'.'+str(week[1]) # 2020.3
	else:
		rweek = week[1]
	return rweek 

def getWeekFirstDayAndLastDay(floatWeek):
	"""
		floatWeek 2020.3
		获取已知第几周的第一天和最后一天
	"""
	tempWeek = str(floatWeek).split('.')
	lastDay = (datetime.datetime.strptime(tempWeek[0]+'-'+tempWeek[1]+'-0', '%Y-%U-%w')+datetime.timedelta(days=7)).__format__("%Y-%m-%d") + ' 23:59:59'
	startDay = (datetime.datetime.strptime(tempWeek[0]+'-'+tempWeek[1]+'-0', '%Y-%U-%w')+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
	return startDay,lastDay

def getNowFirstDayAndLastDay():
	"""
		得到当周 第一天和最后一天 ('2020-09-07 00:00:00', '2020-09-13 23:59:59')
	"""
	return getWeekFirstDayAndLastDay(getWeek())


if __name__ == '__main__':
	print(getWeekFirstDayAndLastDay(getWeek()))
	print(getWeek())

