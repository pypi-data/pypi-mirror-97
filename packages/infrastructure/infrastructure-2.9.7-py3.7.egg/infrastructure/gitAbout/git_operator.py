# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2021-01-18 12:52:11
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-01-18 15:04:42
from infrastructure.parse.parse_xml import ParseXml
from infrastructure.variables.hb_conf import JAVA_COV
from infrastructure.base.dealTime import getNowFirstDayAndLastDay
from infrastructure.base.dealTime import getWeekFirstDayAndLastDay
import platform
import datetime
import os

class GitOperator(object):
	"""
	"""

	def __init__(self):
		pass

	def get_master_last_week_commit(self,service_name,Mon=None,master_week_num=None):
		"""
		获取上周master分支最后一次提交记录
		"""
		if not Mon:
			if master_week_num:
				week = datetime.datetime.now().isocalendar()
				Mon = getWeekFirstDayAndLastDay(str(week[0])+'.'+str(master_week_num))[0]
			else:
				Mon = getNowFirstDayAndLastDay()[0]
		command = 'cd /home/mario/jc/repo/{service_name};git rev-list -n 1 --before="{Mon}" master'.format(
			service_name=service_name,Mon=Mon)

		with os.popen(command) as mon_time:
			out = mon_time.read()

		return out.strip()