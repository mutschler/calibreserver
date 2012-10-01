# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import os
import sqlite3
import threading
import time
from calibre.logger import logger
from calibre.exceptions import ex

db_lock = threading.Lock()

def checkDB():
	if not os.path.exists('metadata.db'):
		conn = sqlite3.connect('metadata.db')
		curs = conn.cursor()
		curs.execute("""CREATE TABLE scrobble (id NUMERIC, thepath TEXT, name TEXT, process NUMERIC, lastviewed TEXT, imdb_id TEXT, tvdb_id NUMERIC, duration NUMERIC, viewed NUMERIC, type TEXT, directory TEXT, year NUMERIC, season NUMERIC, episode NUMERIC, scrobbled NUMERIC);""")
		curs.execute("""CREATE TABLE synoindex (version NUMERIC, lastrun NUMERIC);""")
		conn.commit()

# http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

# myDB = db.DBConnection()
# myDB.action("INSERT INTO history (action, date, showid, season, episode, quality, resource, provider) VALUES (?,?,?,?,?,?,?,?)",
#				 [action, logDate, showid, season, episode, quality, resource, provider])
class DBConnection:
	def __init__(self, filename="metadata.db", suffix=None, row_type="dict"):

		self.filename = filename
		self.connection = sqlite3.connect(filename)
		if row_type == "dict":
			self.connection.row_factory = self._dict_factory
		else:
			self.connection.row_factory = sqlite3.Row

	def action(self, query, args=None):
		with db_lock:
	
			if query == None:
				return
	
			sqlResult = None
			attempt = 0
	
			while attempt < 5:
				try:
					if args == None:
						logger.debug(u"{0}: {1}".format(self.filename, query))
						#print query
						sqlResult = self.connection.execute(query)
					else:
						logger.debug(u"{0}: {1} with args {2}".format(self.filename, query, args))
						#print query, args
						sqlResult = self.connection.execute(query, args)
					self.connection.commit()
					# get out of the connection attempt loop since we were successful
					break
				except sqlite3.OperationalError, e:
					if "unable to open database file" in e.message or "database is locked" in e.message:
						logger.warning(u"DB error: ".format(ex(e)))
						#print "error(e)"
						attempt += 1
						time.sleep(1)
					else:
						logger.error(u"DB error: ".format(ex(e)))
						#print "error(e)"
						raise
				except sqlite3.DatabaseError, e:
					logger.error(u"Fatal error executing query: ".format(ex(e)))
					#print "error(e)"
					raise
	
			return sqlResult
	
	def _dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
	
	
	def select(self, query, args=None):
		sqlResults = self.action(query, args).fetchall()
		if sqlResults == None:
			return []
		return sqlResults


	#update oder insert in tabel
	#myDB.upsert("watch",{'abitrate': '44800','acodec':'ac3'},{'id': '2'})

	def upsert(self, tableName, valueDict, keyDict):

		changesBefore = self.connection.total_changes

		genParams = lambda myDict : [x + " = ?" for x in myDict.keys()]

		query = "UPDATE "+tableName+" SET " + ", ".join(genParams(valueDict)) + " WHERE " + " AND ".join(genParams(keyDict))

		self.action(query, valueDict.values() + keyDict.values())

		if self.connection.total_changes == changesBefore:
			query = "INSERT INTO "+tableName+" (" + ", ".join(valueDict.keys() + keyDict.keys()) + ")" + \
					 " VALUES (" + ", ".join(["?"] * len(valueDict.keys() + keyDict.keys())) + ")"
			self.action(query, valueDict.values() + keyDict.values())
