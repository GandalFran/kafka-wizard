#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.

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