
import asyncio
import feedparser
import ssl
import pymongo
from loguru import logger
import datetime
from dateutil import parser


class thief_news_plugin:
	def __init__(self,loop,collection,lock):
		ssl._create_default_https_context = ssl._create_unverified_context
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
		self.loop = loop
		self.rss = 'https://sec.thief.one/atom.xml'
		self.collection = collection
		self.type = 'news'
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
				article_time = parser.parse(entrie['updated'])
				if (article_time.year == format_time.year) and (article_time.month == format_time.month) and (article_time.day == format_time.day):
					add_dict = {'type':self.type,'title':entrie['title'],'link':entrie['link'],'is_send':0}
					try:
						await self.lock
						if self.collection.count_documents({'link':entrie['link']}) < 1:
							self.collection.insert_one(add_dict)
							logger.info('[News] {} {}'.format(entrie['title'],entrie['link']))
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

	class_name = thief_news_plugin(loop,collection,lock)
	loop.run_until_complete(class_name.return_result())
	