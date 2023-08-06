"""settings
"""
import json
import yaml

__author__ = "help@castellanidavide.it"
__version__ = "01.03 2021-03-07"

class settings:
	def __init__ (self, file, format="yaml", json_indent=4):
		"""Where it all begins
		"""
		assert(format in ["json", "yml", "yaml"])

		# Setup variabiles
		self.file = file
		self.format = format
		self.json_indent = json_indent

	def read(self):
		"""Return the settings into dict type
		"""
		input = open(self.file, "r+").read()

		if self.format == "json":
			return json.loads(input)
		elif self.format in ["yml", "yaml"]:
			return yaml.safe_load(input)

	def write(self, dictionary):
		"""Save file giving a dictionary as input
		"""
		assert(isinstance(dictionary, dict))

		output = ""
		if self.format == "json":
			output = json.dumps(dictionary, indent=self.json_indent)
		elif self.format in ["yml", "yaml"]:
			output = yaml.dump(dictionary)

		open(self.file, "w+").write(output)

if __name__ == "__main__":
	# Test yaml/ yml
	settings("settings.yaml", format="yaml").write({"test": {1: "something", "two": ["something", "else"]}})

	# Test json
	settings("settings.json", format="json").write({"test": {1: "something", "two": ["something", "else"]}})
