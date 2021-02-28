import uuid
import json
import xml.etree.ElementTree as ET
from os import path

class Parser:

	def _read_file_content(self, path):
		with open(path, 'r') as f:
			file_content =  f.read()
		return file_content

	def _map_to_json(self, data):
		xml_tree = ET.fromstring(data)
		elements = xml_tree.findall('.//mxCell')
		for e in elements:
			yield {
				'id': e.get('id'),
				'name': e.get('value'),
				'source': e.get('source'),
				'target': e.get('target'),
				'style': 'normal' if e.get('style') is None or 'dashed' not in e.get('style') else 'special'
			}

	def _build_component_list(self, data):

		# build default consumer id for all components
		consumer_id = str(uuid.uuid4())

		# build components
		components = {}
		for e in data:
			if e['name'] is not None:
				c = {
					'name': e['name'],
					'input_topics': [],
					'output_topics': [],
					'consumer_id': consumer_id
				}
				components[e['id']] = c

		# build connections
		load_balanced_components = []
		for e in data:

			# retrieve style
			style = e['style']

			# retrieve source and destination components
			source = e['source']
			target = e['target']
			
			# build topic id
			topic_id = str(uuid.uuid4())

			if source is not None:
				components[source]['output_topics'].append(topic_id)

			if target is not None:
				components[target]['input_topics'].append(topic_id)

			# save to fix consumer id if dashed
			if style == 'special':
				load_balanced_components.append(components[target])

		# fix consumer id
		for c in load_balanced_components:
			# generate new consumer id
			consumer_id = str(uuid.uuid4())
			# assign to element
			c['consumer_id'] = consumer_id

		# get components
		components = list(components.values())

		return components

	def parse(self, path):
		file_content = self._read_file_content(path=path)
		json_content = list(self._map_to_json(data=file_content))
		component_list = self._build_component_list(data=json_content)
		return component_list


from cookiecutter.main import cookiecutter

class PackageBuilder:

	def __init__(self, broker='localhost:9092', author='default', email='default@example.com', num_tries=10, delivery_timeout=3000):
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
		# write config
		with open(path.join('kafka-service-template', 'cookiecutter.json'), 'w+') as f:
			json.dump(cookie_cutter_info, f, indent=4)
		# run cookie cutter
		cookiecutter('kafka-service-template', no_input=True, output_dir=final_location)

	def _write_pm2(self, pm2_config, final_location=None):
		with open(path.join(final_location,'pm2.json'), 'w+') as f:
			json.dump(pm2_config, f, indent=4)

	def build(self, package_info, final_location=None):
		# build cookie cutter and package
		cookie_cutter_info = self._prepare_cookie_cutter_config(package_info)
		self._build_cookie_cutter(cookie_cutter_info, final_location=final_location)

		# build pm2 package info
		pm2_info = self._prepare_pm2(package_info)
		pm2_info = { 'apps': pm2_info }
		self._write_pm2(pm2_info, final_location=final_location)


	def build_multiple(self, packages_info, final_location=None):

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


if __name__ == '__main__':
	parser = Parser()
	components = parser.parse('test.xml')

	package_builder = PackageBuilder(broker='localhost:9092', author='GandalFran', email='franpintosantos@usal.es')
	package_builder.build_multiple(components, final_location='./packages')