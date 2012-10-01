from calibre import db
from calibre.logger import logger
from calibre import config

import os




def getBookByRating(rating):
	myDB = db.DBConnection()
	
	response = myDB.select("SELECT * from books_ratings_link WHERE rating = {0}".format(rating))
	logger.debug(u"response: ".format(response))
	
	#get infos for every book in response
	books = []
	for result in response:
		rating = result["rating"]
		book_id = result["book"]
		#get book name and infos...
		book = myDB.select("SELECT * from books WHERE id = {0}".format(book_id))
		logger.debug(u"book dict: {}".format(book))
		logger.info(u"Rating: {0:02} Title: {1}".format(rating, book[0]["title"]))
		path = os.path.join(config.DB_ROOT, book[0]["path"])
		data = myDB.select("SELECT * from data WHERE book = {0}".format(book_id))
		logger.debug(u"data dict: {}".format(data))
		for result in data:
			logger.info(u"ebook: " + os.path.join(path, result["name"]) + ".{0}".format(result["format"]))
		if book[0]["has_cover"]:
			logger.info(u"Cover: " + os.path.join(path, "cover.jpg"))

			#return os.path.join(path, "cover.jpg"
			books.append(os.path.join(path, "cover.jpg"))
	return books