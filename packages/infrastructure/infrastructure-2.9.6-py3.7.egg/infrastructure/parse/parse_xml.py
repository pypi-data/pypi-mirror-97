# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-27 14:21:02
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-29 17:19:20

from xml.dom.minidom import parse

class ParseXml(object):
	def __init__(self,file_path):
		dom = parse(file_path)
		self.root = dom.documentElement

	def get_designation_node(self,tagName,match):
		"""
			得到指定的tag对应节点内容
			match 为父节点tagName
		"""
		domList = self.root.getElementsByTagName(tagName)
		if not domList:
			return False
		for dom in domList:
			if dom.parentNode.tagName == match:
				content = dom.childNodes[0].data
				if "parent" not in content:
					return content

		return False

if __name__ == '__main__':
	px = ParseXml("/Users/yongfanmao/哈啰mycode/jc/AppHelloAnunnakiDSPService/service/pom.xml")

	print(px.get_designation_node("artifactId","project"))




