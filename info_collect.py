import os
import asyncio
import importlib
import pymongo
from loguru import logger





def main():
	plugin_dir = "plugins"
	models = os.listdir(plugin_dir)
	model_types = ['web','pwn','re','coding','news','generic']
	for model_type in model_types:
		logger.info('Collect {}_type infos now.',model_type)
		tasks = []
		for model in models:
			if model.endswith('{}_plugin.py'.format(model_type)):
				model_name = model[:-3] # replace .py
				model = importlib.import_module('plugins.{}'.format(model_name))
				model_class = getattr(model,model_name)(loop,collection,lock)
				tasks.append(asyncio.ensure_future(model_class.return_result())) # add task
		if tasks != []:
			loop.run_until_complete(asyncio.wait(tasks)) # run tasks,all will run len(model_types) times.

if __name__ == '__main__':
	client = pymongo.MongoClient(host='localhost', port=27017)
	db = client.info_collect
	collection = db['infos']
	lock = asyncio.Lock()
	loop = asyncio.get_event_loop()
	main()
