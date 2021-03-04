#!usr/bin/python

# Copyright 2021 Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.

import os
import shutil
from kafka_wizard import Wizard

def test_wizard():
	FINAL_LOCATION = './packages'

	# check if exists folder
	os.mkdir(FINAL_LOCATION)
	if os.path.exists(FINAL_LOCATION) and os.path.isdir(FINAL_LOCATION):
		shutil.rmtree(FINAL_LOCATION)

	# generate
	Wizard.generate('test.xml', 
		broker='localhost:9092', 
		author='GandalFran', 
		email='franpintosantos@usal.es', 
		final_location=FINAL_LOCATION
	)
	
	# delete
	shutil.rmtree(FINAL_LOCATION)


def test_command_cli():
	FINAL_LOCATION = './packages_cli'

	# check if exists folder
	os.mkdir(FINAL_LOCATION)
	if os.path.exists(FINAL_LOCATION) and os.path.isdir(FINAL_LOCATION):
		shutil.rmtree(FINAL_LOCATION)

	# generate
	os.system(f'kafkawizard -i test.xml -o {FINAL_LOCATION} -a GandalFran -m franpintosantos@usal.es -b localhost:9092')

	# delete
	shutil.rmtree(FINAL_LOCATION)
