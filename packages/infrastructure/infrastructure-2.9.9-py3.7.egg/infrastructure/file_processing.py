# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2021-03-04 19:24:17
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-03-04 19:33:29
import os

class FileProcessing(object):
	def __init__(self):
		pass

	def file_name(self,file_dir):   
		for root, dirs, files in os.walk(file_dir):  
			print(root) #当前目录路径  
			print(dirs) #当前路径下所有子目录  
			print(files) #当前路径下所有非目录子文件


if __name__ == '__main__':
	f = FileProcessing()
	f.file_name("/Users/yongfanmao/哈啰mycode/AppHellobikeRfAutoTest")
