# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-19 14:29:57
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-07-01 13:53:34

import paramiko
import threading
import time
from sshtunnel import SSHTunnelForwarder
from io import StringIO

class ConnectServerDM(object):
	"""
		通过跳板机连接远程server(支持办公环境已经服务器环境)
	"""
	def __init__(self,serverIP,SSHPort="",ssh_pkey="/home/maoyongfan10020/.ssh/id_rsa",isServerEnv=True):
		"""
			isServerEnv 是从服务器还是办公环境访问跳板机
		"""
		if isServerEnv:
			dumpIp = "10.111.80.92"
		else:
			dumpIp = "47.96.131.92"
			ssh_pkey = "/Users/yongfanmao/.ssh/id_rsa"

		self.SSHPort = ""

		self.localPort = 10023
		if SSHPort:
			self.SSHPort = SSHPort
			sshPort = SSHPort.objects.filter(status = 1).order_by("-port")
			if sshPort:
				self.localPort = sshPort[0].port + 1


		try:
			self.server = SSHTunnelForwarder(
				ssh_address_or_host=(dumpIp,22),
				ssh_username="maoyongfan10020",
				ssh_pkey=ssh_pkey,
				local_bind_address=('0.0.0.0', self.localPort),
				remote_bind_address=(serverIP,22)
				)
			self.server.start()

			dump_key = """-----BEGIN RSA PRIVATE KEY-----
			MIIEoQIBAAKCAQEAxzNks235S92VsiPABEZKbrpMDommaEmfJvY1LxFhK6jBapHD
			qQ7mWWYq5evyzI1z21aXKeE/KbFufVzi2HQN5OTiKNaMMb822JdPzeBtvdH4Ehrq
			iO9QVjHTDI5pZ2hlwha9Il7Dn2l3h2zeeDya5qkZM4vwiAGw+tEE4Uefjr6ZyGLV
			RO6pr1YsIq2OFofi3ATF+yY5KvWUkqFGepRNfkkYikPI6noVsvkj0eEb1H1jtODN
			J/y4hZNGhubHF6LeKJ43EI8P5uBF+gPwYPaZjy3xaEX2mYEDPqNDmR5cgtSPi9xN
			ZmBSxm07vdDYe1xu6E0wS6OE5iD9Y73pjiPDcwIBIwKCAQAWxAuCOHRDL0RO34Oo
			t5N6Xm8XmrPuqVQEc+jSLd84MIsiH0mPqe5wnfZGKZgXYJ+GyBFGnWZN6GRmGT5/
			IzTJs8ITS7hAMxw2AqoI5nLxH0+NCmPyZH41vI0mAaWlawRQsiQ+cTrtpadCrVtA
			8PvClvuQ3MsIOrUj+qF41PxK08CqeaOmvNeOWj1zwbZdMiox1Qtbs1YxfTOgfNxW
			9k3sv3MkKIbJMD6KUi5F/R6k5ZGLFnSBEO+uraZ+wiILdg+Z07sRX3R4CzO9sBGe
			+TxjQCTJADmmzHupMBy/bjmeSAYT1/XgQ8Wm1ciNrmbXLvy0176ZntdbnFL1hl0b
			ZwSLAoGBAOpiO9+s9N9w22BeQM+BgR1MjZiZ4jQO4ZEiy09nUPLIVWxNa6HIZzgX
			4yDU5L8TZODFkoF571BRWbRR0N4BVo+anwTP4yP3N/PAI9Jl2TOlhbF/EPQwdrGs
			NY+YjPp19qGduh4qhivyTRwhS39KhKmI2qblOUs/c1X3+JcNqLjhAoGBANmSfp2l
			BWwg5TIPjcLlj9Rbbwn+4tLrDH+zkW8aWDDeaHzAdYvBrLpgxu4YlZCeP8luSdBE
			uTb7yiFf8z8yA0YMAo1oqLDVRk1+G4PMGJWFNv4Kcwn1jReKCLh1jOnj57jAgIfR
			iSVgUYTEz1VV/KIxEsWmPF1FFdGHbaPQtaLTAoGBALTPcARSOT6nhKltR/CIeYuh
			dIup6QOWc36XLx//PnIlg7nylNvjvVcoXsGOSg++gQUqstjpCRIS3szuqHC/NCWj
			Kjbpg1ZCXlzzTtWBxNAR+WurKlX5gCKpayWhkVN/kl9rC+tiogSk+af8bXDTFeHe
			mgu4JOJG4/HcjJHItVtrAoGAb+TwqNiGch+L0JpI5+PGT/SCP6en2i+9SP1Deveb
			EdF3kJ1+R9/ybnrp9srQk4SV1U6pnk86rpAez1Xq0AsXoF3yrx/hugdIuiOZHzXD
			gBif8F0lOFJl0ZdyMvqgPcWqXwPqVHpjyhRHLlaWg6iQje1aHIFg34KdgbNc9SmB
			+/cCgYAbXQ7mueqqcSZX4thebrRhotKDSGRzMAnftrHxAiyDhOSvUUAHOtgtxg/G
			+twSL4MudIHjn98RhjAWfjp6/j4eTyZ11ghbKBw1y2bd5o1E4U8xG7zXBSMlSKjI
			DCHa39uecvq9DbI85MbWUfmSG+aqug31JmFldR9+UUrGwHnK+Q==
			-----END RSA PRIVATE KEY-----"""

			private_key = paramiko.RSAKey(file_obj=StringIO(dump_key))

			transport = paramiko.Transport((self.server.local_bind_host, self.server.local_bind_port))
			transport.connect(username='maoyongfan10020',pkey=private_key)
			self.__transport = transport
			self.ssh = paramiko.SSHClient()

			sshPortOb = SSHPort.objects.filter(port = self.localPort)
			if sshPortOb:
				sshPortOb[0].status = 1
				sshPortOb[0].save()
			else:
				sshOj = SSHPort(port=self.localPort,status=1)
				sshOj.save()

		except Exception as e:
			self.exception_close()
			raise e
		# self.client = paramiko.SSHClient()
		# self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# self.client.connect(self.server.local_bind_host, self.server.local_bind_port, username='maoyongfan10020', pkey=private_key)
		# self.shell = self.client.invoke_shell()

	def upload(self,local_path,target_path):
		"""
			连接上传
		"""
		sftp = paramiko.SFTPClient.from_transport(self.__transport)
		# 将location.py 上传至服务器 /tmp/test.py
		sftp.put(local_path, target_path)
		# print(os.stat(local_path).st_mode)
		# 增加权限
		# sftp.chmod(target_path, os.stat(local_path).st_mode)
		# sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀

	def download(self,remote_path,local_path):
		sftp = paramiko.SFTPClient.from_transport(self.__transport)
		sftp.get(remote_path,local_path)

	def exec_command(self,command,func="",remoteServer="",
		service_name="",status="",coverageLog=""):
		"""
			command 可为string 也是以为List
		"""
		
		self.ssh._transport = self.__transport
		result=""

		if not isinstance(command,list):
			# 执行命令
			stdin, stdout, stderr = self.ssh.exec_command(command)
			# 获取命令结果
			result = stdout.readlines()
		else:
			channel = self.ssh.invoke_shell()
			for commandls in command:			
				channel.sendall(commandls)
				time.sleep(1)
			time.sleep(3)
			if func:
				while func(remoteServer,service_name,status,coverageLog=coverageLog):
					result=channel.recv(2048).decode('utf-8')
					break
			else:
				result=channel.recv(2048).decode('utf-8')
			channel.close()
		return result


	def close(self):
		self.__transport.close()
		self.ssh.close()
		self.server.close()
		if self.SSHPort:
			sshPortOb = self.SSHPort.objects.filter(port = self.localPort)
			if sshPortOb:
				sshPortOb[0].status=0
				sshPortOb[0].save()


	def exception_close(self):
		self.server.close()

	def __del__(self):
		self.close()
