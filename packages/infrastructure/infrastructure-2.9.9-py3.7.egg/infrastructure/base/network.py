# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-19 14:12:44
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-06-19 14:14:41

import IPy

def is_ip(address):
	"""
		判断字符串是否是IP地址
	"""
	try:
		IPy.IP(address)
		return True
	except Exception as e:
		return False