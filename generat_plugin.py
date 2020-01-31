# -*- coding: utf-8 -*-
# @Author: p1g3
# @Date:   2020-01-30 16:07:00
# @Last Modified by:   p1g3
# @Last Modified time: 2020-01-31 02:23:24

import argparse
import sys


def parse_args():
	parser = argparse.ArgumentParser(epilog='\tUsage:\npython ' + sys.argv[0] + " -d www.baidu.com --keyword baidu")
	parser.add_argument("-u", "--url", help="Rss Url.",required=True)
	parser.add_argument("-pn", "--plugin_name", help="Plugin name.",required=True)
	parser.add_argument("--type", help="Plugin type.",required=True)
	return parser.parse_args()

def generat_plugin(plugin_name,url,plugin_type):
	atom_type = """
import asyncio
import feedparser
import ssl
import pymongo
from loguru import logger
import datetime
from dateutil import parser


class %s:
	def __init__(self,loop,collection,lock):
		ssl._create_default_https_context = ssl._create_unverified_context
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
		self.loop = loop
		self.rss = '%s'
		self.collection = collection
		self.type = '%s'
		self.lock = lock
	async def return_result(self):
		logger.info("{} is running.",self.__class__.__name__)
		future = self.loop.run_in_executor(None,feedparser.parse,self.rss)
		try:
			parse_result = await asyncio.wait_for(future, 30, loop=self.loop)
		except:
			logger.warning("{} parse time out".format(self.rss))
			return
		if parse_result.has_key('entries'):
			entries = parse_result['entries'] 
			format_time = datetime.date.today()
			for entrie in entries:
				logger.debug('[Debug]{} {}'.format(entrie['title'],entrie['link'])) # remove here
				article_time = parser.parse(entrie['updated'])
				logger.debug('[Debug]{} - {}'.format(format_time,article_time)) # remove here
				if (article_time.year == format_time.year) and (article_time.month == format_time.month) and (article_time.day == format_time.day):
					add_dict = {'type':self.type,'title':entrie['title'],'link':entrie['link'],'is_send':0}
					try:
						await self.lock
						if self.collection.count_documents({'link':entrie['link']}) < 1:
							self.collection.insert_one(add_dict)
							logger.info('[%s] {} {}'.format(entrie['title'],entrie['link']))
					finally:
						self.lock.release()
		else:
			logger.error('[Error Parse] {}',self.rss)

if __name__ == '__main__':
	client = pymongo.MongoClient(host='localhost', port=27017)
	db = client.info_collect
	collection = db['infos']

	lock = asyncio.Lock()
	loop = asyncio.get_event_loop()

	class_name = %s(loop,collection,lock)
	loop.run_until_complete(class_name.return_result())
	"""%(plugin_name,url,plugin_type,plugin_type.capitalize(),plugin_name)

	with open(plugin_name+'.py','a+') as f:
		f.write(atom_type)

def main():
	args = parse_args()
	rss_url = args.url
	plugin_name = args.plugin_name
	plugin_type = args.type
	generat_plugin(plugin_name,rss_url,plugin_type)


if __name__ == '__main__':
	main()