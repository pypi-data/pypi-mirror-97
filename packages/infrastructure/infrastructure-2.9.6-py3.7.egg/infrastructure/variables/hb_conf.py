# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-29 19:01:35
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-01-14 20:24:44
from infrastructure.base.dealTime import getWeek

JAVA_COV = {
	"refreshUrl": "http://uat-admin.hellobike.com:40001/systemUser/getLoginUserInfo",
	"jacocoDir": "/home/mario/jc/lib",
	"repoDir": '/home/mario/jc/repo',
	"serviceRepoDir": '/home/mario/jc/repo/{service_name}',
	"jarDir": "/home/mario/jc/{week}/{service_name}",
	"destfile": "/home/mario/jc/{week}/{service_name}/destfile/{recordID}",
	"destfileBack": '/home/mario/jc/back/{service_name}/jacoco-it-back.exec',
	"jacocoIt" : "/home/mario/jc/{week}/{service_name}/destfile/{recordID}/{index}.exec",
	"mergeFile": "/home/mario/jc/{week}/{service_name}/mergeFile/{recordID}",
	"mdestfile": "/home/mario/jc/{week}/{service_name}/mdestfile/{recordID}",
	"reportDir": "/home/mario/jc/{week}/{service_name}/report/{recordID}",
	"mergeReportDir": "/home/mario/jc/{week}/{service_name}/mergeReport/{recordID}",
	"copySourceDir": "/home/mario/jc/{week}/{service_name}/source",	
	"restJacoco": "cd {jacocoDir}&&java -jar jacococli.jar dump --address {ip} --port {port} --reset --retry 3 --destfile ",
	"dumpJacoco": "cd {jacocoDir};java -jar jacococli.jar dump --address {ip} --port {port} --retry 3 --destfile "
}