# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-12-03 15:42:51
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-02-05 20:03:07

from robot.api import logger
import os
import json
import base64
try:
	import pymysql
except:
	os.popen("pip install pymysql -i https://mirrors.ustc.edu.cn/pypi/web/simple/").read()
import threading

class UseMysql(object):
	_instance_lock = threading.Lock()


	def __new__(cls, *args, **kwargs):
		# print(dir(cls))
		if not hasattr(cls, '_instance'):
			# print(dir(UseMysql))
			with UseMysql._instance_lock:
				if not hasattr(cls, '_instance'):
					UseMysql._instance = super().__new__(cls)

		return UseMysql._instance

	def __init__(self):
		self.db = pymysql.connect("10.69.12.184","maoyongfan",base64.b64decode('bTEyMzQ1Ng==').decode(),"helloBikeDB")
		self.cursor = self.db.cursor()


	def getTokenInfos(self):
		sql = "select helloBikeToken,user_agent from helloBikeDB.helloBikeUserInfo where id=1" 
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			# print(results)
			return results[0],results[1]
		except Exception as e:
			raise Exception("获取token信息失败")

	def getWeekNum(self,rd_id):
		sql = "select week_num from helloBikeDB.helloBikeJavaCoverage_record where id={id}".format(id=rd_id) 
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			print(results)
			return results[0]
		except Exception as e:
			raise Exception("获取week_num信息失败")

	def getJavaCoverageToEmail(self):
		sql = "select email from helloBikeDB.helloBikeJavaCoverage_toEmail"

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall() #(('maoyongfan10020@hellobike.com',), ('maoyongfan@163.com',))
			return results
		except Exception as e:
			raise Exception("Failed get to email")

	def getJavaCoverageCcEmail(self):
		sql = "select email from helloBikeDB.helloBikeJavaCoverage_ccEmail"

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall() #(('maoyongfan10020@hellobike.com',), ('maoyongfan@163.com',))
			return results
		except Exception as e:
			raise Exception("Failed get cc email")

	def getWeekReportResult(self,week_num,needIter=True):
		sql = 'select business,team,service_name,service_desc,branch,totalCoverage,incrementCoverage,total_lines,total_coverage_lines,increment_lines,increment_coverage_lines FROM helloBikeDB.helloBikeJavaCoverage_mergeRecord where week_num={week_num} and merge_mode=1 and increment_lines IS NOT NULL  and incrementCoverage!="0%" order by business,incrementCoverage desc'.format(week_num=week_num)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall() #(('maoyongfan10020@hellobike.com',), ('maoyongfan@163.com',))
			if needIter:
				for loop in results:
					yield loop
			else:
				return results
		except Exception as e:
			raise Exception("Failed get week_report_result")

	def __del__(self):
		self.cursor.close()  # 5. 关闭链接
		self.db.close()

if __name__ == '__main__':
	us = UseMysql()
	a=us.getWeekReportResult(5)
	print(dir(a))
	for loop in a:
		print(loop)



	