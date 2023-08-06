# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2021-01-28 19:30:33
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-02-05 20:05:43

import smtplib
import json
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from infrastructure.base.con_mysql import UseMysql
from infrastructure.base.dealTime import getWeek

class SendEmail(object):
	def __init__(self):
		self.smtp = smtplib.SMTP_SSL('smtp.163.com',465)
		self.smtp.set_debuglevel(1)
		self.smtp.ehlo("smtp.163.com")
		self.smtp.login("maoyongfan@163.com","Myf68827106")

	def sendMergeReport(self,week_num=None):
		table=""
		toEmailList = []
		ccEmailList = []

		if week_num:
			week_num = week_num
		else:
			week_num = getWeek(onlyWeek=True)

		useMysql = UseMysql()
		toEmailTuple = useMysql.getJavaCoverageToEmail()
		ccEmailTuple = useMysql.getJavaCoverageCcEmail()

		for loop in toEmailTuple:
			toEmailList.append(loop[0])

		toEmail = ",".join(toEmailList)

		for loop in ccEmailTuple:
			ccEmailList.append(loop[0])

		ccEmail = ",".join(ccEmailList)

		toAdds = toEmailList + ccEmailList + ["shaohui10290@hellobike.com"]


		for business,team,service_name,service_desc,branch,totalCoverage,incrementCoverage,total_lines,total_coverage_lines,increment_lines,increment_coverage_lines in useMysql.getWeekReportResult(week_num=week_num):
			temp = """
				<tr>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>			
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
				<th scope="row" class="spec">
					<font>{}</font>
				</th>
			</tr>""".format(business,team,service_name,service_desc,branch,
				totalCoverage,incrementCoverage,total_lines,
				total_coverage_lines,increment_lines,increment_coverage_lines)

			table += "<tr>"+temp+"</tr>"



		#<th class="nobg">app名称</th>
		tbody = """
			<table id="mytable" cellspacing="0" summary="The technical specifications of the Apple PowerMac G5 series" class="table table-bordered">
			<thead>
			<tr>
				<th >业务线</td>
				<th>团队</td>
				<th>服务名</th>
				<th>服务描述</th>
				<th>分支</th>
				<th>总覆盖率</th>
				<th>增量覆盖率</th>
				<th>总代码行</th>
				<th>总覆盖行</th>
				<th>增量代码行</th>
				<th>增量代码覆盖行</th>
			</tr>
			</thead>
			<tbody>"""+table+"""
			</tbody>
			</table>
		"""

		html = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN""http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<title>Java覆盖率报告</title>
			<script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>

			<!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
			<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

			<!-- 可选的 Bootstrap 主题文件（一般不用引入） -->
			<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

			<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
			<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>


			</head>
			<style type="text/css">
				/* CSS Document color: #4f6b72;*/

				body {
				font: normal 11px auto "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
				color: #4f6b72;
				background: #E6EAE9;
				}

				#mytable {
				width: 1200px;
				padding: 0;
				margin: 0;
				}

				caption {
				padding: 0 0 5px 0;
				width: 700px;  
				font: italic 11px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
				text-align: right;
				}

				th {
				font: bold 25px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif; <!--标签字体大小-->
				color: #4f6b72; <!--#4f6b72  为字体颜色-->
				border-right: 1px solid #C1DAD7;
				border-bottom: 1px solid #C1DAD7;
				border-top: 1px solid #C1DAD7;
				letter-spacing: 2px;
				text-transform: uppercase;
				text-align: center; <!--中间位置-->
				padding: 6px 6px 6px 12px;
				background: #CAE8EA url(images/bg_header.jpg) no-repeat;
				}

				th.nobg {
				border-top: 0;
				border-left: 0;
				border-right: 1px solid #C1DAD7;
				background: none;
				}

				td {
				border-right: 1px solid #C1DAD7;
				border-bottom: 1px solid #C1DAD7;
				background: #fff;
				font-size:25px;
				padding: 6px 6px 6px 12px;
				color: #4f6b72; <!--#4f6b72-->
				}


				td.alt {
				background: #F5FAFA;
				color: #797268;
				}

				th.spec {
				border-left: 1px solid #C1DAD7;
				border-top: 0;
				background: #fff url(images/bullet1.gif) no-repeat;
				font: bold 15px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
				}

				th.specalt {
				border-left: 1px solid #C1DAD7;
				border-top: 0;
				background: #f5fafa url(images/bullet2.gif) no-repeat;
				font: bold 10px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
				color: #797268;
				}
				/*---------for IE 5.x bug*/
				html>body td{ font-size:11px;}

				.p1 {
					float:left;
					height:50px;
					font:40px/44px "微软雅黑";
					color:#666;
					border-left:#f1f1f1 1px solid;
					padding:0 10px;
					margin:25px 0 0 5px;
				}   

			</style>
			<body>
			<div class="container-fluid">
				<h1 style="text-align:center">Java覆盖率 第%d周报告</h1>
			"""%(week_num)+tbody+"""
				<br/>
				<p class="text-left"><img  style="height:50px" href="https://www.helloglobal.com/" src="https://www.helloglobal.com/online-public/header__logo--colored.png" alt="Hellobike" border="0"/>
				</p>
				<br/>
				<p class="text-left"><font size="3">（此邮件由两轮测试工具后台生成，报告问题联系：<a size="3" href="mailto:maoyongfan10020@hellobike.com?subject=[问题反馈]&cc=zhouzhifang509@hellobike.com;yanlei@hellobike.com">开发组</a></font><font size="3">）</font></p>
				</div>
				</body>
				</html>
			"""

		msg = MIMEMultipart("related")
		msg["Subject"] = "Java覆盖率 第{week_num}周报告".format(week_num=week_num)
		msg["From"] = "maoyongfan@163.com"

		msg["To"] = toEmail

		msg["Cc"] = ccEmail

		msg["Bcc"] = "shaohui10290@hellobike.com"

		msgAlternative = MIMEMultipart('alternative')
		msg.attach(msgAlternative)

		msgText = MIMEText(html,"html","utf-8")
		msgAlternative.attach(msgText)

		self.smtp.sendmail("maoyongfan@163.com",toAdds,msg.as_string())

		self.smtp.quit()

if __name__ == '__main__':
	se=SendEmail()
	se.sendMergeReport(week_num=5)




