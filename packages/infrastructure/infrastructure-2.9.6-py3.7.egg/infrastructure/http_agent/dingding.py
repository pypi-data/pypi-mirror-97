# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-09-09 16:50:59
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-09-10 16:52:16
import os
from infrastructure.http_agent.http_request import HttpRequest

class DingDingRequest(object):
	def __init__(self,coverageLog=""):
		self.coverageLog = coverageLog

	def logs(self,operationType="",message="",typeInfo="",remark=""):
		record = self.coverageLog(data=
					{
						"operationType": operationType,
						"message": message,
						"typeInfo": typeInfo,
						"remark": remark,
						"status":1
					})					
		record.is_valid(raise_exception=True)
		record.save()

	def sendRobot(self,title,text,
			url="https://oapi.dingtalk.com/robot/send?access_token=3ac128206e2f9a5990e71d31f1846adf6a1c2d872ac2f9e0569535a1773b6954",
			msgtype="markdown",atMobiles=[],isAtAll=False):
		"""
		默认发送给java覆盖率统计平台使用推广群
		"""
		data = {
			"msgtype": msgtype,
			"markdown": {
				"title":title,
				"text": text
			},
			"at": {
				"atMobiles": atMobiles,
				"isAtAll": isAtAll
			}
		}

		headers = {'content-type': "application/json;charset=UTF-8"}

		response = HttpRequest.post(url,headers=headers,data=data)
		if response['status']:

			if self.coverageLog:
				if response['result']['errcode'] == 0:
					self.logs(operationType="发送消息成功",
						message=str(response),
						typeInfo="成功发送钉钉消息",
						remark="")
				else:
					self.logs(operationType="发送消息失败",
						message=str(response),
						typeInfo="发送钉钉消息失败",
						remark=str(data))

		else:
			if self.coverageLog:
				self.logs(operationType="出现异常",
					message=str(response),
					typeInfo="发送钉钉消息给机器人出现异常",
					remark=str(data))

		return response['result']
