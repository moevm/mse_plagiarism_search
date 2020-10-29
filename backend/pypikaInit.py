from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions

class DBObjects:
	def __init__(self):
		self.tables = {}
		self.tables["Entry"] = Table("Entry")
		self.tables["File"] = Table("File")
		self.tables["CodeFragment"] = Table("CodeFragment")
		self.func = {}
		self.func["metaphone"] = CustomFunction('metaphone', ['text', 'len'])
		self.func["levenshtein"] = CustomFunction('levenshtein', ['source', 'target'])

db = DBObjects()