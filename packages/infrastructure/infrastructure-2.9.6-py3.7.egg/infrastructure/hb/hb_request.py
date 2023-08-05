# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-10 14:43:59
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-03-03 13:52:58
import os
from infrastructure.http_agent.http_request import HttpRequest
from infrastructure.variables.hb_conf import JAVA_COV
from infrastructure.base.dealTime import getWeek
from infrastructure.base.con_mysql import UseMysql

class HBRequest(object):
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

	def ticketGit(self,team,service_name,cookie,user_agent):
		"""
			申请git权限
		"""
		url = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		data = {
			"template":100002740,
			"application_args":{
				"username":"maoyongfan10020",
				"projects":{
					"team":{
						"value":team,
						"label":team
					},
					"name":service_name,
					"access":{
						"value":30,
						"label":"开发"
					}
				}
			}
		}

		headers = {'content-type': "application/json;charset=UTF-8",
			'cookie': cookie,
			'User-Agent': user_agent}

		response = HttpRequest.post(url,headers=headers,data=data)
		if response['code'] == 201:

			if self.coverageLog:
				self.logs(operationType="成功申请权限",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

		else:
			if self.coverageLog:
				self.logs(operationType="申请权限失败",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

			raise Exception("等待git审批")

			

	def openServerAuth(self,server,token,cookie,user_agent):
		"""
		先获取服务器挂载app,再去请求开通权限
		"""
		addECSUserURL = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		appsTemp = ""
		if server.apps:
			appsTemp = server.apps
		else:
			searchDetail = self.searchEcsDetail(server,token,cookie,user_agent)
			if not searchDetail:
				# 获取服务器详细信息失败，无法开通服务访问权限
				raise Exception("获取服务器详细信息失败，无法开通服务访问权限")
			else:			 
				for app in searchDetail['apps']:
					appsTemp += app["app__name"]+","
				if appsTemp[-1] == ",":
					appsTemp = appsTemp[:-1]
				server.apps = appsTemp
				server.save()

		data = {
			"template":100004103,
			"application_args":
				{"ip":"{}".format(server.ip.intranet),
				"team_name":"{}".format(server.team),
				"name":"{}".format(server.name),
				"env":"{}".format(server.env),
				"apps":"{}".format(appsTemp)}
		}

		headers = {'token': token,
			#'cookie': cookie,
			'User-Agent': user_agent}	

		response = HttpRequest.post(addECSUserURL,headers=headers,data=data)
		if response['code'] == 201:
			if self.coverageLog:
				self.logs(operationType="申请服务器权限成功",
					message=str(response),
					typeInfo="申请服务器权限成功",
					remark="")
			return True
		else:
			if self.coverageLog:
				self.logs(operationType="申请服务器权限时失败",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="")
			raise Exception("无法开通服务器访问权限")		

	def searchEcsDetail(self,server,token,cookie,user_agent):
		searchEcsDetailURL = "http://10.111.90.230:20001/api/v1/ecs/{}/".format(server.server_id)
		# print (self.searchEcsDetailURL)
		response = HttpRequest.get(searchEcsDetailURL,headers={'token': token,
			#'cookie': cookie,
			'User-Agent': user_agent})
		if response['code'] == 200:
			detailData = response['result']['data']
			return detailData
		else:
			if self.coverageLog:
				self.logs(operationType="获取服务器挂载app信息失败,请分析",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="获取该{}服务器 {} 挂载app信息,失败"
					.format(server.name,server.env))

			return False

	def getTeamInfo(self,alreadyRecord,helloBikeToken,user_agent):
		"""
			获取服务对应团队名称
		"""
		getTeamUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(
			service_name=alreadyRecord.service_name)

		data = {"action":"tt.application.info.detail"}

		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(getTeamUrl,headers=headers,data=data)
		# print(response)

		if response['status']:
			self.logs(operationType="接口返回结果",
					message=str(response['result']),
					typeInfo="获取团队信息",
					remark="")

			service_desc = response['result'].get("data").get("desc")
			team = response['result'].get("data").get("team").get("code")
			team_desc = response['result'].get("data").get("team").get("name","")

			alreadyRecord.service_desc = service_desc
			alreadyRecord.team = team
			alreadyRecord.team_desc = team_desc
			alreadyRecord.save()
			
			return team
		else:
			raise Exception("获取团队信息异常")



	def getGitTagAndCommit(self,alreadyRecord,helloBikeToken,user_agent):
		"""
		 通过atlas代码版本拦根据commit搜索得出tag和branch
		 以commit查的时候可能会有多个git_tag,git_tag 取的是第一个，而这第一个可能会构建失败,所以commit为不必须传的参数
		"""

		releaseRecordUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(
			service_name=alreadyRecord.service_name)
		if alreadyRecord.git_tag:
			searchValue = alreadyRecord.git_tag
		else:
			searchValue = alreadyRecord.commit
		data = {
				"page":1,
				"page_size":20,
				"search":searchValue,
				"action":"tt.code.deploy.tags.filter"
				}
		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(releaseRecordUrl,headers=headers,data=data)

		if response['status']:
			try:
				git_tag = response['result'].get("data",[])[0].get("name","")
			except:
				raise Exception("传入的是错误的commit！！可能是效能平台")
			commit = response['result'].get("data",[])[0].get('commit').get('id')
			branch = response['result'].get("data",[])[0].get("branch","")
			alreadyRecord.commit = commit
			alreadyRecord.git_tag = git_tag
			alreadyRecord.branch = branch
			alreadyRecord.save()
			self.get_zip_url(alreadyRecord,helloBikeToken,user_agent)
			return git_tag
		else:
			raise Exception("获取版本对应标签异常")

	
	def getCommitBeta(self,alreadyRecord,helloBikeToken,user_agent):
		"""
		在内测发布记录中以git_tag为索引查询过滤出branch,commit信息
		"""
		codeManagerDeployUrl = "https://codemanager-inner.hellobike.cn/deploy/list/query"
		data = {
			"page":
				{
					"size":100,"current":1
				},
			"query":
				{
					"status": None,
					"env":alreadyRecord.env.upper(),
					"startTime":None,
					"endTime":None,
					"appName":alreadyRecord.service_name
				}
		}
		# print(data)
		headers = {'content-type': "application/json;charset=UTF-8",
			'sso-token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(codeManagerDeployUrl,headers=headers,data=data)
		# print(response)

		if response['status']:
			if response['result']['data']['total'] != 0:
				for record in response['result']['data']['records']:
					if record['tag'] == alreadyRecord.git_tag:
						alreadyRecord.commit = record['gitCommit']
						alreadyRecord.branch = record['branchName']
						alreadyRecord.save()
						break
				else:
					raise Exception("没有在内测版本找到与之对应的版本信息")
			else:
				raise Exception("该服务在内测版本对应环境没有发布成功的记录")
		else:
			raise Exception("采集beta发布信息异常")

	def get_zip_url_beta(self,alreadyRecord,helloBikeToken,user_agent):
		"""
			获得内测版本编译后jar包下载地址
		"""
		zip_url = "https://codemanager-inner.hellobike.cn/api/getPackageUrl?appName={appName}&env={env}&tag={tag}".format(
			appName=alreadyRecord.service_name,env=alreadyRecord.env.upper(),
			tag=alreadyRecord.git_tag)

		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.get(zip_url,headers=headers)

		# print(response)

		if response['status']:
			beta_url = response['result'].get('data','')
			if not beta_url:
				raise Exception("beta zip_url 为空")
			alreadyRecord.zip_url = beta_url
			alreadyRecord.save()
		else:
			raise Exception("获取beta编译后class Zip包下载地址异常")



	def get_zip_url(self,alreadyRecord,helloBikeToken,user_agent):
		"""
			从atls获取编译后class zip包下载地址
		"""
		zipUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(
			service_name=alreadyRecord.service_name)
		data = {
			"lang":"java",
			"env":"PRO",
			"expires":3600,
			"name":alreadyRecord.git_tag,
			"action":"tt.code.deploy.tags.download"
			}
		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(zipUrl,headers=headers,data=data)

		if response['status']:

			zip_url = response['result'].get("data",{}).get("url","")

			alreadyRecord.zip_url = zip_url
			alreadyRecord.save()
			return zip_url
		else:
			raise Exception("获取编译后class Zip包下载地址异常")




	def isK8s(self,alreadyRecord,ip,helloBikeToken,user_agent):
		"""
			判断cmdb ip是否能搜索到该IP
		"""
		searchIpUrl = "http://10.111.90.230:20001/api/v1/ip/?search={ip}".format(ip=ip)

		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-Agent': user_agent}

		response = HttpRequest.get(searchIpUrl,headers=headers)
		print(response)
		if self.coverageLog:
			self.logs(operationType="{ip}机器".format(ip=ip),
						message=str(response),
						typeInfo="判断是否是容器",
						remark="")

		if response['status']:
			if response['result']['count'] == 0:
				alreadyRecord.is_container = True
				alreadyRecord.save()
				return True
			else:
				return False
		else:
			raise Exception("判断是否是容器发布异常")

	def downClassZip(self,alreadyRecord):
		"""
		下载atls提供的编译后class zip包
		"jarDir": "/home/maoyongfan10020/jc/{service_name}"
		"/home/maoyongfan10020/jc/{service_name}/{service_name}.zip" 下载的zip包
		"""
		jarDir = JAVA_COV["jarDir"].format(week=alreadyRecord.week_num,service_name=alreadyRecord.service_name)
		os.makedirs(jarDir) if not os.path.exists(jarDir) else True

		zipPath = JAVA_COV["jarDir"].format(week=alreadyRecord.week_num,
				service_name=alreadyRecord.service_name)+"/{service_name}.zip".format(
				service_name=alreadyRecord.service_name)
		self.checkZip(zipPath)
		response = HttpRequest.download(alreadyRecord.zip_url,zipPath)
		return True
		# if not response:
		# 	self.logs(operationType="下载编译后class_zip包",
		# 			message="失败",
		# 			typeInfo="下载atls包",
		# 			remark="")
		# 	return False
		# else:
		# 	self.logs(operationType="下载编译后class_zip包",
		# 			message="成功",
		# 			typeInfo="下载atls包",
		# 			remark="")
		# 	return True

	def checkZip(self,zipPath):
		"""
			删除旧atls下载zip包
		"""
		if os.path.exists(zipPath):
			command = "rm -rf {zipPath}".format(zipPath = zipPath)
			os.popen(command).read()

			self.logs(operationType="删除旧的编译后zip包",
				message=command,
				typeInfo="删除atls旧zip包",
				remark="")


	def getBussiness(self,helloBikeToken,user_agent,user="",isServer=True):
		"""
			获取个业务线拥有的团队
		"""
		result = []
		bussinessTeamDict = {}

		if helloBikeToken == "" and user_agent == "":
			us = UseMysql()
			headerInfos = us.getTokenInfos()
			helloBikeToken = headerInfos[0]
			user_agent = headerInfos[1]
			del us
		
		if isServer:
			getTeamListUrl = "http://10.111.90.230:20001/api/v1/team/org-list/"
		else:
			getTeamListUrl = "https://cmdbservice.hellobike.cn/api/v1/team/org-list/"

		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-Agent': user_agent}

		response = HttpRequest.get(getTeamListUrl,headers=headers)
		print(response)
		if self.coverageLog:
			self.logs(operationType="业务线信息",
						message=str(response),
						typeInfo="cmdb获取业务线信息",
						remark=user)
		# import json
		# print(json.dumps(response))
	
		if response['status']:
			infos = response['result']['data']
			for bussiness in infos:
				temp = {}			
				teamList = []
				temp['label'] = bussiness['label']
				for team in bussiness.get('children',[]):
					teamTemp = {}
					teamTemp['value']=team.get('name')
					teamTemp['team_desc']=team.get('label')
					teamList.append(teamTemp)
					children = team.get('children',[])
					if children:
						for child in children:
							teamTemp = {}
							teamTemp['value'] = child.get('name','')
							teamTemp['team_desc'] = child.get('label','')
							teamList.append(teamTemp)
				temp['value'] = bussiness['label'] #temp['value'] = teamTemp
				if bussiness.get('children'):
					result.append(temp)
					bussinessTeamDict[bussiness['label']] = teamList
			return result,bussinessTeamDict
		else:
			raise Exception("获取业务线信息异常")

	def getBussinessServiceName(self,teamList,helloBikeToken,user_agent,user="",isServer=True):
		"""
			获取某个业务线下所有服务名
		"""
		result = []

		if helloBikeToken == "" and user_agent == "":
			us = UseMysql()
			headerInfos = us.getTokenInfos()
			helloBikeToken = headerInfos[0]
			user_agent = headerInfos[1]
			del us
			
		if isServer:
			getBussinessServiceNameUrl = 'http://10.111.90.230:20001/api/v1/app/?page=1&page_size=5000'
		else:
			getBussinessServiceNameUrl = 'https://cmdbservice.hellobike.cn/api/v1/app/?page=1&page_size=5000'
		for team in teamList:
			getBussinessServiceNameUrl += "&team[]={}".format(team)
		
		print(getBussinessServiceNameUrl)
		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-Agent': user_agent}

		response = HttpRequest.get(getBussinessServiceNameUrl,headers=headers)
		if self.coverageLog:
			self.logs(operationType="服务名信息",
						message=str(response),
						typeInfo="cmdb获取业务线下所有服务名",
						remark=user)
		# print(response)
		if response['status']:
			infos = response['result']['data']
			for team in infos:
				temp = {}
				teamTemp = []
				temp['label'] = team['name']
				temp['value'] = team['name']
				temp['description'] = team['description']
				result.append(temp)
			print(len(result))
			return result
		else:
			raise Exception("获取业务线下服务信息异常")


	def getEcsServerInfos(self,service_name,env,helloBikeToken,
			user_agent,user="",isServer=True):

		if helloBikeToken == "" and user_agent == "":
			us = UseMysql()
			headerInfos = us.getTokenInfos()
			helloBikeToken = headerInfos[0]
			user_agent = headerInfos[1]
			del us

		result = []
		if isServer:
			ttGetEcsIpUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(service_name=service_name)
		else:
			ttGetEcsIpUrl = "https://tt.hellobike.cn/v1/api/{service_name}".format(service_name=service_name)

		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-agent': user_agent}

		data = {
				"page":1,
				"env":env.upper(),
				"action":"tt.application.info.resource",
				"page_size":20,
				"type":"ECS"
				}

		response = HttpRequest.post(ttGetEcsIpUrl,headers=headers,data=data)
		if self.coverageLog:
			self.logs(operationType="ecs服务器信息",
						message=str(response),
						typeInfo="atlas获取ecs服务器信息",
						remark=user)
		# print(response)
		if response['status']:
			infos = response['result']
			if infos['count'] == 0:
				return result

			else:
				for server in infos.get('data',[]):
					temp ={}
					temp['ecs_name'] = server['name']
					temp['team'] = server['team']
					temp['group'] = server['group']
					temp['app_version'] = server['app_version']
					temp['ip_address'] = server.get('ip').get('intranet','0.0.0.0')
					temp['server_status'] = server['status']
					temp['is_container'] = False
					result.append(temp)
				return result

		else:
			raise Exception("获取ecs服务器信息异常")

	def getPodServerInfos(self,service_name,env,helloBikeToken,
			user_agent,user="",isServer=True):

		if helloBikeToken == "" and user_agent == "":
			us = UseMysql()
			headerInfos = us.getTokenInfos()
			helloBikeToken = headerInfos[0]
			user_agent = headerInfos[1]
			del us

		result = []
		if isServer:
			if env.upper() == "FAT":
				groupsUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/6".format(service_name)
				containerUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/6/group/{tag}"
			else:
				groupsUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/2".format(service_name)
				containerUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/2/group/{tag}"
		else:
			if env.upper() == "FAT":
				groupsUrl = "https://gaia.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/6".format(service_name)
				containerUrl = "https://gaia.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/6/group/{tag}"
			else:
				groupsUrl = "https://gaia.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/2".format(service_name)
				containerUrl = "https://gaia.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/2/group/{tag}"

		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-Agent': user_agent}

		grRep = HttpRequest.get(groupsUrl,headers=headers)
		print(grRep)
		
		if self.coverageLog:
			self.logs(operationType="容器group信息",
						message=str(grRep),
						typeInfo="gaia获取容器group信息",
						remark=user)
		if grRep['status']:
			if grRep['result']['data']:
				groupList = grRep['result']['data'].get('groupList',[])
				
				if not groupList:
					return result
				for group in groupList:
					print(group)
					cnRep = HttpRequest.get(containerUrl.format(
						service_name=service_name,
						tag=group),headers=headers)
					if cnRep['status']:
						
						appPodList = cnRep['result']['data'].get('appPodList',[])
						if not appPodList:
							continue
						team = cnRep['result']['data'].get('teamName','')
						for pod in appPodList:
							temp = {}
							temp['running_times'] = pod.get('operationDays','')
							temp['team'] = team
							temp['group'] = group
							temp['app_version'] = pod.get('version','')
							temp['ip_address'] = pod.get('ipAddress','')
							temp['server_status'] = pod.get('status','')
							temp['is_container'] = True
							result.append(temp)

					else:
						raise Exception("获取容器服务器group下详细信息异常")
	
			return result

		else:
			raise Exception("获取容器group服务器信息异常")


	def getServiceIp(self,env,git_tag,service_name):
		"""
		反查出fat,uat,pre指定发布记录对应的IP
		"""
		ipList = []
		# tt-inner
		ttGetEcsIpUrl = "https://tt-inner.hellobike.cn/v1/api/{}".format(service_name)
		if env.upper() == "FAT":
			groupsUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/6".format(service_name)			
		elif env.upper() == "UAT":
			groupsUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/2".format(service_name)
		elif env.upper() == "PRE":
			groupsUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/groups/appname/{}/env/9".format(service_name)

		us = UseMysql()
		headerInfos = us.getTokenInfos()
		headers = {"token": headerInfos[0],"user-agent":headerInfos[1]}
		del us
	
		data = {
				"page":1,
				"env":env.upper(),
				"action":"tt.application.info.resource",
				"page_size":20,
				"type":"ECS"
				}
		ttRep = HttpRequest.post(url=ttGetEcsIpUrl,data=data,headers=headers)	
		# print(ttRep)
		if ttRep["code"] == 200 and ttRep["result"].get('data',[]):
			print("ecs有内容")
			for loop in ttRep["result"].get('data',[]):
				# print(loop["app_version"])
				if loop["app_version"] == git_tag:
					ipList.append(loop.get('ip',{}).get('intranet',''))
			
			print(ipList)
			if ipList:
				return ipList


		grRep = HttpRequest.get(groupsUrl,headers=headers)
		# print(grRep)
		if grRep['code'] == 200:
			dataResult = grRep['result'].get('data')
			groupList = dataResult.get('groupList',[])
		else:
			raise Exception("采集group失败,容器接口有问题")

		if not groupList:
			raise Exception("该服务没有采集到group信息")

		print("容器goupList:",groupList)
		for loop in groupList:
			if env.upper() == "FAT":
				containerUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/6/group/{tag}".format(
				service_name=service_name,tag=loop)
			elif env.upper() == "PRE":
				containerUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/9/group/{tag}".format(
				service_name=service_name,tag=loop)
			else:
				containerUrl = "https://gaia-inner.hellobike.cn/container-business-service/api/v1/apps/pods/appname/{service_name}/env/2/group/{tag}".format(
				service_name=service_name,tag=loop)

			cnRep = HttpRequest.get(containerUrl,headers=headers)

			# print(cnRep)
			if cnRep["code"] == 200:
				# print(cnRep)
				# print(containerUrl)
				appPodList = cnRep["result"].get('data').get('appPodList',[])
				if appPodList:
					for appPod in appPodList:
						if appPod["version"] == git_tag:
							ipList.append(appPod.get('ipAddress'))
				else:
					continue
			else:
				raise Exception("采集容器ip失败,容器接口有问题")
			
		if not ipList:
			raise Exception("该服务没有采集到ip信息")
		
		print(ipList)
		return ipList



if __name__ == '__main__':
	hb = HBRequest()
	# hb.getServiceIp("fat","group_202012021901160310912","AppBikeUserGrowthBaseService")
	# hb.getServiceIp("uat","uat_20201217142813394","AppBikeProSCM")
	#hb.getServiceIp("FAT","fat_20201221114932677","AppHellobikeOpenlockService")
	# alreadyRecord = {"env":"uat","service_name":"AppHellobikeOpenlockService",
	# 		"git_tag":"uat_20201222191917056"}
	# helloBikeToken = "f3d379d9836f7e9fb469d1816d4649b2"
	# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
	# hb.get_zip_url_beta(alreadyRecord,helloBikeToken,user_agent)
	# a =hb.getBussiness("309dd9dbac1b7fd0cefd5e34f40c769b",
	# 	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	# 	isServer=False)
	# print(a)
	# print(a[0])
	# print('gee')
	# print(a[1])
	# for loop in a[1]:
	# 	print(loop)
	# print(hb.getBussinessServiceName(['Tank', 'Tiger', 'Agent', 'Lion', 'Shark', 'Wolf'],"51e4618683215c6d62caa5499845c666",
	# 	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36")
	# )

	print(hb.getEcsServerInfos("AppRcpModelEngineService",
		"fat",
		"e24680385fa5d524db6607ea9cfb57fc",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
		isServer=False))
	# a = hb.getPodServerInfos("AppHellobikeRideApiService",
	# 	"fat",
	# 	"51e4618683215c6d62caa5499845c666",
	# 	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
	# 	isServer=False)
	# print(a)
	# print(len(a))

	#AppHellobikeOpenlockService

	

