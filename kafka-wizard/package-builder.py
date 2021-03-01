#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.

import json
from os import path
from cookiecutter.main import cookiecutter

class PackageGenerator:

	def __init__(self, broker='localhost:9092', author='default', email='default@example.com', num_tries=10, delivery_timeout=3000, **kwargs):
		self.broker = broker
		self.author = author
		self.email = email
		self.num_tries = num_tries
		self.delivery_timeout = delivery_timeout

	def _prepare_cookie_cutter_config(self, package_info):
		return {
			"author": self.author,
			"email": self.email,
			"name": package_info['name'],
			"kafka": {
				"num_tries": self.num_tries,
				"input_topics": package_info['input_topics'],
				"output_topics": package_info['output_topics'],
				"group_id": package_info['consumer_id'],
				"broker": self.broker,
				"delivery_timeout": self.delivery_timeout
			},
			"flow": {
				"producer": 'yes' if package_info['output_topics'] else 'no',
				"consumer": 'yes' if package_info['input_topics'] else 'no'
			}
		}

	def _prepare_pm2(self, package_info):
		return {
			"name": package_info['name'],
			"cwd": f"./{package_info['name']}",
			"interpreter": "/bin/bash",
			"script": f"launch.sh",
			"out_file": f"/var/log/{package_info['name']}.log",
			"error_file": f"/var/log/{package_info['name']}.err"
		}

	def _build_cookie_cutter(self, cookie_cutter_info, final_location=None):
		# get template dir
		template_dir = path.join(path.dirname(os.path.abspath(__file__)), 'kafka-service-template')

		# write config
		with open(path.join(template_dir, 'cookiecutter.json'), 'w+') as f:
			json.dump(cookie_cutter_info, f, indent=4)
			
		# run cookie cutter
		cookiecutter(template_dir, no_input=True, output_dir=final_location)

	def _write_pm2(self, pm2_config, final_location=None):
		with open(path.join(final_location, 'pm2.json'), 'w+') as f:
			json.dump(pm2_config, f, indent=4)

	def build(self, package_info, final_location=None):
		# build cookie cutter and package
		cookie_cutter_info = self._prepare_cookie_cutter_config(package_info)
		self._build_cookie_cutter(cookie_cutter_info, final_location=final_location)

		# build pm2 package info
		pm2_info = self._prepare_pm2(package_info)
		pm2_info = { 'apps': pm2_info }
		self._write_pm2(pm2_info, final_location=final_location)


	def build_multiple(self, packages_info, final_location=None, **kwargs):

		all_pm2_info = []
		for p in packages_info:
			# build cookie cutter and package
			cookie_cutter_info = self._prepare_cookie_cutter_config(p)
			self._build_cookie_cutter(cookie_cutter_info, final_location=final_location)

			# build pm2 package info
			pm2_info = self._prepare_pm2(p)
			all_pm2_info.append(pm2_info)
		
		# join pm2 config
		pm2_info = { 'apps': all_pm2_info }
		self._write_pm2(pm2_info, final_location=final_location)

