# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-02 15:17:55
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-06-02 16:31:10
from bs4 import BeautifulSoup

class HtmlParse(object):
	def __init__(self,content):
		self.soup = BeautifulSoup(content,'html.parser')

	def getNode(self,node):
		return self.soup.findAll(node)[0]