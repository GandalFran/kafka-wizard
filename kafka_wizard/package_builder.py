#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.

import json
import yaml
from os import path, unlink
from cookiecutter.main import cookiecutter

class PackageBuilder:

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
			"kafka.num_tries": self.num_tries,
			"kafka.input_topics": package_info['input_topics'],
			"kafka.output_topics": package_info['output_topics'],
			"kafka.group_id": package_info['consumer_id'],
			"kafka.broker": self.broker,
			"kafka.delivery_timeout": self.delivery_timeout,
			"flow.producer": 'yes' if package_info['output_topics'] else 'no',
			"flow.consumer":'yes' if package_info['input_topics'] else 'no'
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

		# write config
		config_file = './config.yml'
		with open(config_file, 'w+') as f:
			yaml.dump({'default_context':cookie_cutter_info}, f)

		# run cookie cutter
		cookie_repo = 'https://github.com/GandalFran/kafka-cookie.git'
		cookiecutter(cookie_repo, config_file=config_file, no_input=True, output_dir=final_location)

		# remove config file
		unlink(config_file)

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

