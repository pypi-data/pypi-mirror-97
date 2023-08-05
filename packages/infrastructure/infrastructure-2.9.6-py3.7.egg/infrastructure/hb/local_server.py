# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-29 11:41:39
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-01-18 15:01:02

import os
import time
import socket
from infrastructure.variables.hb_conf import JAVA_COV
from infrastructure.parse.htmlParse import HtmlParse
from infrastructure.base.dealTime import getWeek
from infrastructure.base.con_mysql import UseMysql
from infrastructure.gitAbout.git_operator import GitOperator
class LocalServer(object):
	def __init__(self,alreadyRecord,JavaCoverageReportUrl="",
		JavaCoverageIncrementRes="",
		coverageLog="",
		javaCoverageNolib="",javaCoverageLibOneNotSN="",isMerge=False):
		"""
			操作本地服务器
		"""
		self.alreadyRecord = alreadyRecord
		self.isMerge = isMerge
		self.JavaCoverageReportUrl = JavaCoverageReportUrl
		self.JavaCoverageIncrementRes = JavaCoverageIncrementRes
		self.coverageLog = coverageLog
		self.jarDir = JAVA_COV["jarDir"].format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name)
		self.copySourceDir = JAVA_COV["copySourceDir"].format(week=self.alreadyRecord.week_num,
				service_name=self.alreadyRecord.service_name)
		self.reportDir = JAVA_COV["reportDir"].format(week=self.alreadyRecord.week_num,
			service_name=self.alreadyRecord.service_name,
			recordID=self.alreadyRecord.id)
		self.serviceRepoDir = JAVA_COV["serviceRepoDir"].format(service_name=self.alreadyRecord.service_name)
		self.jacocoDir = JAVA_COV["jacocoDir"]
		self.jacocoIt = JAVA_COV["jacocoIt"]
		self.mergeFile = JAVA_COV["mergeFile"].format(week=self.alreadyRecord.week_num,
			service_name=self.alreadyRecord.service_name,recordID=self.alreadyRecord.id)
		self.destfile = JAVA_COV["destfile"].format(week=self.alreadyRecord.week_num,
				service_name=self.alreadyRecord.service_name,recordID=self.alreadyRecord.id)
		self.mdestfile = JAVA_COV["mdestfile"].format(week=self.alreadyRecord.week_num,
				service_name=self.alreadyRecord.service_name,recordID=self.alreadyRecord.id)
		self.mergeReportDir = JAVA_COV["mergeReportDir"].format(week=self.alreadyRecord.week_num,
			service_name=self.alreadyRecord.service_name,
			recordID=self.alreadyRecord.id)
		self.javaCoverageNolib = javaCoverageNolib
		self.javaCoverageLibOneNotSN = javaCoverageLibOneNotSN



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

	def cpFile(self):
		os.makedirs(self.mergeFile) if not os.path.exists(self.mergeFile) else os.popen("rm -rf {}/*".format(self.mergeFile)).read()
		os.makedirs(self.mdestfile) if not os.path.exists(self.mdestfile) else os.popen("rm -rf {}/*".format(self.mdestfile)).read()

		for jcIndex in eval(self.alreadyRecord.sn_id):
			us = UseMysql()
			week = us.getWeekNum(jcIndex)
			del us
			command = "cp {jacocoIt} {mergeFile}/{index}.exec".format(jacocoIt=self.jacocoIt.format(
				week=week,service_name=self.alreadyRecord.service_name,recordID=jcIndex,index=jcIndex),mergeFile=self.mergeFile,
				index=jcIndex)
			self.logs(operationType="复制Java覆盖率记录",
					message=command,
					typeInfo="合并覆盖率命令",
					remark="{recordId}次合并覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			with os.popen(command) as temp:
				result =temp.read()

	def mergeRecordFile(self):
		self.cpFile()

		command = "cd {jacocoDir};java -jar jacococli.jar merge {mergeFile}/*.exec --destfile {mdestfile}/all.exec".format(jacocoDir=self.jacocoDir,
			mergeFile=self.mergeFile,mdestfile = self.mdestfile)

		self.logs(operationType="合并Java覆盖率操作",
					message=command,
					typeInfo="合并覆盖率命令",
					remark="{recordId}次合并覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

		with os.popen(command) as temp:
			result =temp.read()


	def filter_local_jar(self,jar_list,command):
		"""
		过滤本服务器上的jar包名,为特殊化处理打成一个jar包的服务
		"""

		download_jar = []
		jar_name_list = eval(self.alreadyRecord.jar_name)
		for jar_name in jar_name_list:
			filter_jar_command = command.format(
				service_name=self.alreadyRecord.service_name,jarNameDir=jar_list[0].split(".j")[0],jarName=jar_name)	

			with os.popen(filter_jar_command) as temp:
				result =temp.read()

			if self.coverageLog:
				self.logs(operationType="在服务本地过滤",
					message=filter_jar_command+"\n"+result,
					typeInfo="特殊化过滤jar包",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			for loop in result.split('\n'):
				if not loop:
					continue
				if 'iface' in loop.lower():
					continue

				download_jar.append(loop.strip())


		if download_jar:
			self.alreadyRecord.download_jar = str(download_jar)
			self.alreadyRecord.save()
			return True
		else:
			self.alreadyRecord.status = 6
			self.alreadyRecord.mark = "在本地特殊化处理匹配jar包失败"
			self.alreadyRecord.save()
			return False

	def filter_local_jar_container(self):
		"""
			^过滤以jarName开头的jar包
		"""
		download_jar = []

		if self.javaCoverageNolib and self.javaCoverageNolib.objects.filter(service_name=self.alreadyRecord.service_name):
			# 解压jar包后发现没有lib目录
			command = "cd "	+ self.jarDir + "/{service_name};ls | grep ^{jarName}"
		else:
			command = "cd " + self.jarDir + "/{service_name}/lib;ls | grep ^{jarName}"
		jar_name_list = eval(self.alreadyRecord.jar_name)
		for jar_name in jar_name_list:
			filter_jar_command = command.format(
				service_name=self.alreadyRecord.service_name,jarName=jar_name)	

			with os.popen(filter_jar_command) as temp:
				result =temp.read()

			if self.coverageLog:
				self.logs(operationType="容器解压后zip包本地过滤jar",
					message=filter_jar_command+"\n"+result,
					typeInfo="容器化过滤jar包",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			for loop in result.split('\n'):
				if not loop:
					continue
				if 'iface' in loop.lower():
					continue

				download_jar.append(loop.strip())

				if self.javaCoverageNolib and self.javaCoverageNolib.objects.filter(service_name=self.alreadyRecord.service_name):
					mv_command = "mv " + self.jarDir + '/{service_name}/{jarName} '.format(
						service_name=self.alreadyRecord.service_name,
						jarName=loop.strip()) + self.jarDir
				else:
					mv_command = "mv " + self.jarDir + '/{service_name}/lib/{jarName} '.format(
						service_name=self.alreadyRecord.service_name,
						jarName=loop.strip()) + self.jarDir
				os.popen(mv_command).read()		
		if download_jar:
			self.alreadyRecord.download_jar = str(download_jar)
			self.alreadyRecord.save()
			return True
		else:
			self.alreadyRecord.status = 6
			self.alreadyRecord.mark = "在本地过滤容器jar包失败"
			self.alreadyRecord.save()
			return False
	def checkZip(self,zipPath):
		if os.path.exists(zipPath):
			command = "rm -rf {zipPath}".format(zipPath = zipPath)
			os.popen(command).read()
			if self.coverageLog:
				self.logs(operationType="删除旧的zip包",
					message=command,
					typeInfo="覆盖率解压zip包过程",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

	def unzipJar_container(self):
		#"jarDir": "/home/maoyongfan10020/jc/{service_name}"
		containerFile = self.jarDir+"/{service_name}".format(service_name = self.alreadyRecord.service_name)

		deleteAllCommand = "rm -rf " + containerFile + "/*"
		os.popen(deleteAllCommand).read()

		# 注意解压的目录
		unzip_command = "cd " + self.jarDir + (";unzip -o {jarToZip} -d "+ self.jarDir).format(
				jarToZip=self.alreadyRecord.service_name +'.zip')

		if self.coverageLog:
			self.logs(
					operationType="解压atlas下载zip包命令",
					message=unzip_command,		
					typeInfo="覆盖率解压atlas下载包",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
						service_name=self.alreadyRecord.service_name)
				)		
		os.popen(unzip_command).read()

	def special(self):
		"""
		把/home/maoyongfan10020/jc/{service_name}/{service_name}/lib/* 移动到 /home/maoyongfan10020/jc/{service_name}
		"""
		mv_command = "mv " + self.jarDir + '/' + self.alreadyRecord.service_name + '/lib/* ' + self.jarDir
		os.popen(mv_command).read()
		return [self.alreadyRecord.service_name+".jar"]

	def upzipJar(self,jar_list="",jarDir="",javaCoverageLibOne="",special_deal=False):
		"""
			解压下载下来的jar包(jar包已重命名)
			args:
				jar_list  为了处理特殊的服务，该服务把所有jar包融成一个jar包 该参数为了第一次解压融合jar包
				jarDir special_deal 为特殊化处理第二次解压本地融合的jar包
			1.判断/home/maoyongfan10020/jc/{service_name}/all 是否存在 不存在创建
		"""
		classFile = self.jarDir+"/all"
		os.makedirs(classFile) if not os.path.exists(classFile) else True
		if not special_deal:
			deleteAllCommand = "rm -rf " + self.jarDir + "/all/*"
			os.popen(deleteAllCommand).read()

		if not jarDir:
			jarDir = self.jarDir

		if jar_list:
			download_jar = jar_list
		else:
			download_jar = eval(self.alreadyRecord.download_jar)



		
		for jar in download_jar:
			self.checkZip(self.jarDir+'/'+jar.split('.j')[0]+'.zip')
			command = "cd " + jarDir + ";mv {download_jar} {jarToZip}".format(
				download_jar=jar,
				jarToZip=jar.split('.j')[0]+'.zip')
			os.popen(command).read()

			if self.coverageLog:
				self.logs(operationType="把jar包转为zip包命令",
					message=command,
					typeInfo="覆盖率解压zip包过程",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))

			unzip_command = "cd " + jarDir + (";unzip -o {jarToZip} -d "+self.jarDir + "/all/{jarNameDir}").format(
				jarToZip=jar.split('.j')[0]+'.zip',
				jarNameDir=jar.split('.j')[0])

			if self.coverageLog:
				self.logs(
						operationType="解压zip包命令",
						message=unzip_command,		
						typeInfo="覆盖率解压zip包过程",
						remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name)
					)		
			os.popen(unzip_command).read()

		if javaCoverageLibOne and javaCoverageLibOne.objects.filter(service_name=self.alreadyRecord.service_name) and not special_deal:

			command = "cd {jarDir}/".format(jarDir=self.jarDir)+"all/{jarNameDir}/BOOT-INF/lib;ls | grep {jarName}"
			self.filter_local_jar(jar_list,command)
			self.upzipJar(jarDir="{jarDir}/".format(jarDir=self.jarDir)+"all/{jarNameDir}/BOOT-INF/lib".format(
				service_name=self.alreadyRecord.service_name,
				jarNameDir=jar_list[0].split(".j")[0]),special_deal=True)

			# 删除掉融合目录(包含了不需要的class)
			os.popen("rm -rf {jarDir}/all/{service_name}".format(
										jarDir=self.jarDir,service_name=self.alreadyRecord.service_name
										)).read()

	def copyCode(self):
		os.popen("rm -rf " + self.copySourceDir).read() if os.path.exists(self.copySourceDir) else True
		for path in eval(self.alreadyRecord.jar_dir):
			os.popen("cp -r " + path + "/src/main/java/. " + self.copySourceDir).read() if os.path.exists(path + "/src/main/java") else True

	def mergeContinue(self):

		if not os.path.exists(self.jacocoIt.format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name,
					recordID=self.alreadyRecord.id,index=self.alreadyRecord.id)):

			command = "cd {jacocoDir};java -jar jacococli.jar merge {destfile}/*.exec --destfile {destfile}/{index}.exec".format(jacocoDir=self.jacocoDir,
				destfile = self.destfile,index=self.alreadyRecord.id)

			self.logs(operationType="合并Java覆盖率操作",
						message=command,
						typeInfo="合并持续统计覆盖率命令",
						remark="{recordId}次合并覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
								service_name=self.alreadyRecord.service_name))

			with os.popen(command) as temp:
				result =temp.read()

	def operateExec(self):
		if len(os.listdir(self.destfile)) > 1:
			self.mergeContinue()
		else:
			if not os.path.exists(self.jacocoIt.format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name,
					recordID=self.alreadyRecord.id,index=self.alreadyRecord.id)):
				os.rename(self.jacocoIt.format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name,
						recordID=self.alreadyRecord.id,index=0),self.jacocoIt.format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name,
						recordID=self.alreadyRecord.id,index=self.alreadyRecord.id))

	def jacocoReport(self):
		if self.isMerge:
			reportDir = self.mergeReportDir
			jacocoDumpFile = "{mdestfile}/all.exec".format(mdestfile=self.mdestfile)
		else:
			reportDir = self.reportDir
			self.operateExec()
			jacocoDumpFile =  self.jacocoIt.format(week=self.alreadyRecord.week_num,service_name=self.alreadyRecord.service_name,
					recordID=self.alreadyRecord.id,index=self.alreadyRecord.id)

		try:
			os.makedirs(reportDir) if not os.path.exists(reportDir) else True
		except:
			if self.coverageLog:
				self.logs(
						operationType="reportDir目录下recordID目录出现异常",
						message=reportDir,		
						typeInfo="生成报告目录",
						remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name)
					)


		f = open(reportDir+"/jacoco.xml","w")
		f.close()

		self.copyCode()


		libOneNotSN = self.javaCoverageLibOneNotSN.objects.filter(service_name=self.alreadyRecord.service_name)

		if libOneNotSN:
			"""	使用该种模式，计算覆盖率不全，会遗弃掉解压后lib下的部分jar包，这部分jar包就不会算覆盖率了
				/workspace/carkey/AppHelloSaturnService/latest/lib 目录下仅有一个jar包，且这个jar包名不为服务名
				AppHelloSaturnService 这个服务git过滤出两个需要记录覆盖率的jar包,而lib 目录下仅有一个jar包，且这个jar包名不为服务名
				解压这个jar包后,有个需要计算覆盖率的jar包就在解压后的目录里,其他jar包在解压后的目录
				/home/maoyongfan10020/jc/AppHelloSaturnService/all/saturn-service/BOOT-INF/lib中，需要二次解压
			"""

			classfile = self.jarDir + "/all/{jar_name}/BOOT-INF/classes".format(jar_name = libOneNotSN[0].jar_name)
		elif self.javaCoverageNolib.objects.filter(service_name=self.alreadyRecord.service_name):
			classfile = self.jarDir + "/all/{name}/BOOT-INF/classes".format(name=eval(self.alreadyRecord.download_jar)[0].split('.j')[0])
		else:
			classfile = self.jarDir + "/all"
		sourcefiles = self.copySourceDir

		report_command = ("cd {jacocoDir};java -jar jacococli.jar report " +\
				jacocoDumpFile + " --classfiles {classfile} --sourcefiles {sourcefiles} --html {reportDir} --xml {xml}").format(
				jacocoDir = self.jacocoDir,
				service_name=self.alreadyRecord.service_name,
				classfile=classfile,
				sourcefiles = sourcefiles,
				reportDir=reportDir,
				xml=reportDir+"/jacoco.xml"
				)

		if self.coverageLog:
			self.logs(operationType="覆盖率执行参数",
				message=report_command,
				typeInfo="覆盖率报告",
				remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
						service_name=self.alreadyRecord.service_name))

		with os.popen(report_command) as temp:
				temp.read()

		return True
		# else:
		# 	return False



	def jacocoIncrementReport(self,master_week_num=None):
		gitOp = GitOperator()
		if self.isMerge:
			reportDir = self.mergeReportDir

		else:
			reportDir = self.reportDir

		if self.isMerge:
			commit = gitOp.get_master_last_week_commit(self.alreadyRecord.service_name,master_week_num=master_week_num)
		else:
			commit = gitOp.get_master_last_week_commit(self.alreadyRecord.service_name)
		del gitOp

		print("incrementR_cm:",commit)
		if commit:
			compare = commit
		else:
			compare = "origin/master"
		command = "source /home/mario/virtualEnv/rfServerEnv/bin/activate;cd {serviceCodeDir};diff-cover {xml} --compare-branch={compare} --src-roots {sourcefiles} --html-report {incrementReport}".format(
			serviceCodeDir = self.serviceRepoDir,	
			xml=reportDir+"/jacoco.xml",
			compare=compare,
			sourcefiles=self.serviceRepoDir + '/*/src/main/java',			
			incrementReport=reportDir+"/incrementReport.html"
			)

		with os.popen(command) as gen_irmReport:
			out = gen_irmReport.read()

		if self.coverageLog:
			self.logs(operationType="覆盖率执行参数",
				message=command + "\n" + out,
				typeInfo="覆盖率增量报告",
				remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
						service_name=self.alreadyRecord.service_name))

		if not out:
			return False
		if "No lines" in out:
			if self.coverageLog:
				self.logs(operationType="无新增覆盖率",
					message="",
					typeInfo="覆盖率增量报告",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))
			return "无新增覆盖率"
		for loop in out.split('\n'):
			if 'Total' in loop:
				totalList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				total = totalList[1]

			if 'Missing' in loop:
				missList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				miss = missList[1]

			if 'Coverage' in loop:
				coverageList = [ i for i in loop.split(' ') if (len(i)!=0) ]
				coverage = coverageList[1]

		self.alreadyRecord.incrementCoverage = coverage
		self.alreadyRecord.increment_coverage_lines = str(int(total)-int(miss))
		self.alreadyRecord.increment_lines = total
		self.alreadyRecord.save()

		with open(reportDir+"/incrementReport.html","r") as temp:
			content = temp.read()

		self.JavaCoverageIncrementRes.objects.create(coverageRecord=self.alreadyRecord,incrementRes=content)

		return True

	def parseReport(self):
		if self.isMerge:
			reportDir = self.mergeReportDir
			reportName = "mergeReport"
		else:
			reportDir = self.reportDir
			reportName = "report"

		index_path = reportDir+"/index.html"
		if os.path.exists(index_path):
			with open(index_path) as report:
				content = report.read()
			hp = HtmlParse(content)
			tdContent = hp.getNode('table').tfoot.tr.contents
			no_coverage_lines = self.__delayStringLine((tdContent[7].contents)[0])
			total_lines = self.__delayStringLine((tdContent[8].contents)[0])

			total_coverage_lines = total_lines - no_coverage_lines
			totalCoverage = '{:.2f}%'.format(total_coverage_lines/total_lines*100)
			print (total_coverage_lines,total_lines)
			# return str(total_lines),str(total_coverage_lines),totalCoverage

			self.alreadyRecord.total_lines = str(total_lines)
			self.alreadyRecord.total_coverage_lines = str(total_coverage_lines)
			self.alreadyRecord.totalCoverage = totalCoverage
			#http://10.111.10.223:8001/report/AppHellobikeRideApiService/129/index.html
			hostname = socket.gethostname()
			env = socket.gethostbyname(hostname)
			# if "uat" in hostname:
			# 	env = "uat"
			# elif "fat" in hostname:
			# 	env = "fat"
			# else:
			# 	env = "uat"  {}-rfautotest.hellobike.cn
			report_html_url = ['http://{}:8001/report/{}/{}/{}/{}/index.html'.format(
					env,getWeek(onlyWeek=True),self.alreadyRecord.service_name,reportName,self.alreadyRecord.id),
				'https://{}-rfautotest.hellobike.cn/report/{}/{}/{}/incrementReport.html'.format(
				env,self.alreadyRecord.service_name,reportName,self.alreadyRecord.id)]
			for url in report_html_url:
				self.JavaCoverageReportUrl.objects.create(coverageRecord=self.alreadyRecord,reportUrl=url)

			self.alreadyRecord.status = 1
			self.alreadyRecord.save()
			return self.alreadyRecord
		else:
			if self.coverageLog:
				self.logs(operationType="无总量报告生成",
					message="",
					typeInfo="解析覆盖率总量报告",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))
		return False

	def deleteImportantRes(self):
		'''
		删除重要的信息
		'''
		week_num = self.alreadyRecord.week_num
		# 删除代码仓库

		if (week_num%2) !=0 : #基数星期删除
			os.popen("rm -rf {serviceRepoDir}".format(
				serviceRepoDir=self.serviceRepoDir)).read()

			if self.coverageLog:
				self.logs(operationType="删除代码仓库",
					message="rm -rf {serviceRepoDir}".format(
				serviceRepoDir=self.serviceRepoDir),
					typeInfo="安全策略",
					remark="{recordId}次覆盖率统计{service_name}".format(recordId=self.alreadyRecord.id,
							service_name=self.alreadyRecord.service_name))


		# # 删除生成报告路径
		# with os.popen("rm -rf {reportDir}".format(
		# 	reportDir=self.reportDir)) as temp:
		# 	temp.read()

		# # 删除合并报告路径
		# with os.popen("rm -rf {mergeReportDir}".format(
		# 	mergeReportDir=self.mergeReportDir)) as temp:
		# 	temp.read()

		# 删除一个星期前的记录
		# week_num = getWeek(onlyWeek=True)
		with os.popen("rm -rf /home/mario/jc/{week}".format(week=week_num-2)) as temp:
			temp.read()


		# # 删除"/home/mario/jc/{week}/".format(week=getWeek(onlyWeek=True))+"{service_name}"/* 目录
		# # 防止/home/mario/jc/{week}/".format(week=getWeek(onlyWeek=True))+"{service_name}"/service_name jar包被移走了，下一次没有jar包
		# with os.popen("rm -rf {jarDir}/*".format(
		# 	jarDir=self.jarDir)) as temp:
		# 	temp.read()

		# 删除jc/服务名目录下所有.zip
		with os.popen("rm -rf {jarDir}".format(
			jarDir=(self.jarDir+'/*.zip'))) as temp:
			temp.read()

		# 删除jc/服务名/source目录
		with os.popen("rm -rf {source}".format(
			source=(self.jarDir+'/source/*'))) as temp:
			temp.read()

		# 删除jc/服务名/all目录
		with os.popen("rm -rf {all}".format(
			all=(self.jarDir+'/all/*'))) as temp:
			temp.read()

		# 删除jc/week/servie_name/service_name 目录
		with os.popen("rm -rf {service_name}".format(
			service_name=(self.jarDir+"/"+self.alreadyRecord.service_name))) as temp:
			temp.read()

		






	def __delayStringLine(self,line):
		'''
			line '13,401'
		'''
		if ',' in line:
			temp = line.split(',')
			return int(temp[0]+temp[1])
		else:
			return int(line)	

