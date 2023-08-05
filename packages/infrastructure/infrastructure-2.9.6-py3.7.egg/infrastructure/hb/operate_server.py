# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 17:10:22
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-11-19 20:03:16
import time
import os
from infrastructure.variables.hb_conf import JAVA_COV

def checkServerStatus(remoteServer,service_name,status,coverageLog=""):
	command = "cd /workspace/carkey/{service_name}/latest;./init.script status".format(service_name=service_name)
	result = remoteServer.exec_command(command=command)
	print(result)
	if status in result[0]:
		if coverageLog:
			record = coverageLog(data=
					{
						"operationType": "检查服务器状态是否符合预期",
						"message": str(result),
						"remark": status,
						"typeInfo": "覆盖率桥接",
						"status":1
					})					
			record.is_valid(raise_exception=True)
			record.save()
		return True
	else:
		return False

class OperateServer(object):
	def __init__(self,remoteServer):
		"""
			操作远程服务器
		"""
		self.remoteServer = remoteServer

	def restartServer(self,service_name,coverageLog=""):
		stopCommandList = ["sudo su - deploy\n",
		"sudo su\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"sudo ./init.script stop\n"]

		stopResult = self.remoteServer.exec_command(command=stopCommandList,
			func=checkServerStatus,remoteServer=self.remoteServer,
			service_name=service_name,status="stopped",coverageLog=coverageLog)
		if coverageLog:
			record = coverageLog(data=
					{
						"operationType": "统计静态代码停止服务器结果",
						"message": stopResult,
						"typeInfo": "覆盖率桥接",
						"status":1
					})					
			record.is_valid(raise_exception=True)
			record.save()

		
		# time.sleep(5)
		startCommandList = ["sudo su - deploy\n",
		"sudo su\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"sudo ./init.script start\n"]

		restartResult = self.remoteServer.exec_command(command=startCommandList,
			func=checkServerStatus,remoteServer=self.remoteServer,
		service_name=service_name,status="running",coverageLog=coverageLog)		
		return restartResult

	def checkStaus(self,service_name):
		command = "cd /workspace/carkey/{service_name}/latest;./init.script status".format(service_name=service_name)
		result = self.remoteServer.exec_command(command=command)

		if "stopped" in result[0]:
			return "stopped"
		elif "running" in result[0]:
			return "running"
		else:
			return "unkown"

	def addJacocoArg(self,service_name,port):
		commandList = ["sudo su - deploy\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"""sudo sed -i '/START_OPTS=/a\START_OPTS="$START_OPTS -javaagent:\/workspace\/carkey\/jarlibs\/jacoco\/jacocoagent.jar=includes=*,output=tcpserver,address=*,port={port},append=true"' init.script\n""".format(
			port=port)]
		result = self.remoteServer.exec_command(command=commandList)
		return result

	def filter_jar(self,service_name,jarName,islib=True):
		"""
			根据pom上jar包名在运程服务器上过滤出实际的jar包
		"""
		tempJar=[]
		if islib:
			command = "cd /workspace/carkey/{service_name}/latest/lib;ls|grep {jarName}".format(
				service_name=service_name,
				jarName=jarName)
		else:
			command = "cd /workspace/carkey/{service_name}/latest;ls|grep {jarName}".format(
				service_name=service_name,
				jarName=jarName)
		result = self.remoteServer.exec_command(command=command)
		if result:
			for loop in result:
				tempJar.append(loop.strip())

		return tempJar


	def download(self,service_name,jar,islib=True,isServerEnv=True):
		if islib:
			remote_path = "/workspace/carkey/{service_name}/latest/lib/{jar}".format(
				service_name=service_name,jar=jar)
		else:
			remote_path = "/workspace/carkey/{service_name}/latest/{jar}".format(
				service_name=service_name,jar=jar)

		if isServerEnv:			
			local_dir = JAVA_COV["jarDir"].format(
				week=getWeek(onlyWeek=True),service_name=service_name)
			os.makedirs(local_dir) if not os.path.exists(local_dir) else True
			local_path = local_dir + "/" + jar
		else:
			local_path = "/Users/yongfanmao/哈啰mycode/jc/data/{service_name}/{jar}".format(
				service_name=service_name,jar=jar)

		self.remoteServer.download(remote_path,local_path)

		return local_path




	def __del__(self):
		self.remoteServer.close()


