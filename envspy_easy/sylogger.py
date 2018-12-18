# -*-coding:utf-8-*-

import logging


def logger(logFilename, msg_type = 'debug', msg = 'no_msg_given'):
	''''' Output log to file and console '''
	# Define a Handler and set a format which output to file
	logging.basicConfig(
		level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
		format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
		datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
		filename=logFilename,  # log文件名
		filemode='w')  # 写入模式“w”或“a”
	# Define a Handler and set a format which output to console
	console = logging.StreamHandler()  # 定义console handler
	console.setLevel(logging.INFO)  # 定义该handler级别
	formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
	console.setFormatter(formatter)
	# Create an instance
	logging.getLogger().addHandler(console)  # 实例化添加handler

	# Print information              # 输出日志级别
	if msg_type == 'debug':
		logging.debug(msg)
	elif msg_type == 'info':
		logging.info(msg)
	elif msg_type == 'warning':
		logging.warning(msg)
	elif msg_type == 'error':
		logging.error(msg)
	elif msg_type == 'critical':
		logging.critical(msg)


# if __name__ == "__main__":
# 	logger('logging.log', msg_type='error', msg='this is')
# 	logger('logging.log', msg_type='info', msg='a')
# 	logger('logging.log', msg_type='warning', msg='test')