from calibre import db
from calibre.logger import logger
from calibre import config
import os

myDB = db.DBConnection()

#get all books sort by title asc
response = myDB.select("SELECT * from books ORDER BY sort ASC")



for result in response:
	book = {}
	#print "{0}\n".format(result)
	book["title"] = result["title"]
	book["id"] = result["id"]
	series_id = myDB.select("SELECT series from books_series_link WHERE book = {0}".format(book["id"]))
	book["series_index"] = result["series_index"]
	book["has_cover"] = result["has_cover"]
	book["author_sort"] = result["author_sort"]
	# bookauthor_id = myDB.select("SELECT * from books_authors_link WHERE book = {0}".format(book["id"]))
	# print bookauthor_id
	bookrating = myDB.select("SELECT rating from books_ratings_link WHERE book = {0}".format(book["id"]))
	book["rating"] = bookrating[0]["rating"]

	bookformat = myDB.select("SELECT * from data WHERE book = {0}".format(book["id"]))
	formate = {}
	for format in bookformat:
		formate[format["format"]] = format["name"]
		#formate["{0}".format(format["format"])] = format["name"]
	book["format"] = formate
	#print bookrating, bookformat
	if series_id:
		book["series_id"] = series_id[0]["series"]
		series = myDB.select("SELECT * from series WHERE id = {0}".format(book["series_id"]))
		book["series"] = series[0]["name"]
	else:
		book["series"] = None
 		#print series
	#print book
	print u"Title: {0}".format(book["title"])
	if book["series"]:
		print u"Buch {0} von {1}".format(book["series_index"], book["series"])
	print "Formate: "
	for format in book["format"]:
		#print book["format"][format]
		print " - " + book["format"][format] + "."+ format.lower()

	print book