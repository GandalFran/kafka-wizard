#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.


import uuid
import json
import xml.etree.ElementTree as ET
from os import path

class DrawioParser:

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

		# build components
		components = {}
		for e in data:
			if e['name'] is not None:
				# build default consumer id for each components
				consumer_id = str(uuid.uuid4())

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

		# fix consumer id for the ones ho share it 
		shared_consumer_id = str(uuid.uuid4())
		for c in load_balanced_components:
			# assign to element
			c['consumer_id'] = shared_consumer_id

		# get components
		components = list(components.values())

		return components

	def parse(self, path, **kwargs):
		file_content = self._read_file_content(path=path)
		json_content = list(self._map_to_json(data=file_content))
		component_list = self._build_component_list(data=json_content)
		return component_list