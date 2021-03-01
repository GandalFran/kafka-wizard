#!usr/bin/python

# Copyright 2021Francisco Pinto-Santos @ GandalFran in GitHub
# See LICENSE for details.


from . import DrawioParser, PackageBuilder

class Wizard:

	@classmethod
	def generate(cls, diagram_file, final_location, **kwargs):
		parser = DrawioParser()
		components = parser.parse(diagram_file, **kwargs)
		package_builder = PackageBuilder(**kwargs)
		package_builder.build_multiple(components, final_location=final_location, **kwargs)