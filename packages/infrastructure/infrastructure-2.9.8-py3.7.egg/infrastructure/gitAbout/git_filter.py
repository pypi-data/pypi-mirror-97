# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 16:43:44
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-11-02 19:49:19

from infrastructure.parse.parse_xml import ParseXml
from infrastructure.variables.hb_conf import JAVA_COV
# import sys
# sys.path.append("/Users/yongfanmao/哈啰mycode/jc/library/infrastructure")
# from parse.parse_xml import ParseXml
import platform
import os

class GitFilter(object):
	"""
		git项目过滤
	"""
	def __init__(self,serviceRepoDir="",service_name=""):
		if serviceRepoDir:
			self.serviceRepoDir = serviceRepoDir
		else:
			self.repoDir = JAVA_COV.get("repoDir")
			os.makedirs(self.repoDir) if not os.path.exists(self.repoDir) else True
			self.serviceRepoDir = JAVA_COV["serviceRepoDir"].format(
				service_name=service_name)


	def get_backslash(self):
		sysstr = platform.system()
		if sysstr =="Windows":
			return "\\"
		else:
			return '/'

	def filter_jarName(self,coverageLog="",alreadyRecord="",assignation_name=[]):
		"""
			功能: 给出git项目中 打成jar包的包名及该jar包对应git的路径
				 支持获取指定目录下的jar包的包名
			返回
				(打成jar包的包名,jar包对应git的路径)
		"""
		jarList = []
		sourcePathList = []
		for name in os.listdir(self.serviceRepoDir):
			if assignation_name:
				if name not in assignation_name:
					continue
			name_path = self.serviceRepoDir + self.get_backslash() + name
			if name == '.git':
				continue
			elif 'iface' in name.lower():
				continue
			elif os.path.isdir(name_path):
				for file in os.listdir(name_path):
					file_path = name_path + self.get_backslash() + file
					if os.path.isfile(file_path) and file == "pom.xml":
						px = ParseXml(file_path)
						name = px.get_designation_node("artifactId","project")
						if name:
							jarList.append(name)
							sourcePathList.append(name_path)
					if os.path.isdir(file_path):
						# dspservice 第二层判断
						for sub_file in os.listdir(file_path):
							sub_file_path = file_path + self.get_backslash() + sub_file
							if os.path.isfile(sub_file_path) and sub_file == "pom.xml":
								px = ParseXml(sub_file_path)
								sub_name = px.get_designation_node("artifactId","project")
								if sub_name:
									if coverageLog:
										record = coverageLog(data=
										{
											"operationType": "发现第二层jar包",
											"message": sub_name,
											"remark": "{recordId}次覆盖率统计{service_name}".format(recordId=alreadyRecord.id,
							service_name=alreadyRecord.service_name),
											"typeInfo": "gitlab_jar包过滤",
											"status":1
										})					
										record.is_valid(raise_exception=True)
										record.save()
									jarList.append(sub_name)
									sourcePathList.append(file_path)

		return jarList,sourcePathList


	def gitPullCode(self,team,service_name,branch_or_commit):
		content = ""
		if not os.path.exists(self.serviceRepoDir):
			# 拉新取项目代码 git@gitlab-inner.hellobike.cn:10022
			command = 'cd '+ self.repoDir + ';\
					git clone ssh://git@gitlab.hellobike.cn:10022/{team}/{service_name}.git;\
					cd {service_name};\
					git pull&&git checkout {branch_or_commit}'.format(
						service_name=service_name,
						team=team,branch_or_commit=branch_or_commit)
		else:
			command = 'cd '+self.serviceRepoDir + ';\
			git checkout master&&git pull&&git checkout {branch_or_commit}'.format(
				branch_or_commit=branch_or_commit)

		print(command)
		with os.popen(command) as gitClone:
			content = gitClone.read() # content 可能会没有

		return content,command

if __name__ == '__main__':
	a=GitFilter(serviceRepoDir='/Users/yongfanmao/哈啰mycode/jc/AppHelloAnunnakiDSPService')
	print(a.filter_jarName())
