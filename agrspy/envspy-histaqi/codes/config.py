import os
import socket
from pathlib import Path


class Config(object):
	"""
	Basic configuration, like socket default timeout, headers
	"""

	def __init__(self):
		super(Config, self).__init__()
		self.socket_timeout = 20
		# set socket layer timeout as 20s
		socket.setdefaulttimeout(self.socket_timeout)
		# self.headers = {'User-Agent': 'Mozilla/5.0'}
		self.url = "http://www.tianqihoubao.com/aqi/"
		self.headers = {'user-agent': 'my-app/0.0.1'}
		self.folder_json = self.makedirs('json')
		self.folder_csv = self.makedirs('csv')
		self.log_path = self.makedirs('logging')
		self.timeout = 500
		self.max_retries = 30

	def makedirs(self, path):
		path = Path.cwd().parent.joinpath(path)
		if not path.exists():
			os.makedirs(path)
		return path
