import sqlite3

def dictFactory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

class db:
	def __init__(self, database):
		self.connection = sqlite3.connect(database, check_same_thread=False)
		self.connection.row_factory = dictFactory

	def execute(self, query, params = ()):
		try:
			cursor = self.connection.cursor()
			cursor.execute(query, params)
			self.connection.commit()
			return cursor.lastrowid
		finally:
			if cursor:
				cursor.close()

	def executeSQLFile(self, sqlFile):
		try:
			with open(sqlFile) as f:
				query = f.read()
			cursor = self.connection.cursor()
			cursor.executescript(query)
			self.connection.commit()
		finally:
			if cursor:
				cursor.close()

	def fetch(self, query, params = (), all = False):
		try:
			cursor = self.connection.cursor()
			cursor.execute(query, params)
			if all == True:
				return cursor.fetchall()
			else:
				return cursor.fetchone()
		finally:
			if cursor:
				cursor.close()

	def fetchAll(self, query, params = ()):
		return self.fetch(query, params, True)
