from calibre import db
from calibre.logger import logger
from calibre import config
from calibre import encodingKludge as ek
import os


class Book(object):

	def _init_(self, id):
		self.id = id


	def _getBookSeries(self, book_id):
		myDB = db.DBConnection()
		bookids = myDB.select(u"SELECT * from books_series_link WHERE book = '{0}'".format(book_id))
		#return bookids
		series = {}
		for bookid in bookids:
			series["id"] = bookid["series"]
			series_result = myDB.select(u"SELECT * from series WHERE id = '{0}'".format(bookid["series"]))
			series["series_name"] = series_result[0]["name"]
		if series:
			return series["series_name"]
		else:
			return None
		
	def _getBookInfoFromId(self, book_id):
		myDB = db.DBConnection()
		bookids = myDB.select(u"SELECT * from books WHERE id = '{0}'".format(book_id))
		print bookids
		if bookids:
			return bookids[0]


	def _getBookRating(self, book_id):
		myDB = db.DBConnection()
		ratingid = myDB.select(u"SELECT * from books_ratings_link WHERE book = '{0}'".format(book_id))
		if ratingid:
			rating = myDB.select(u"SELECT * from ratings WHERE id = '{0}'".format(ratingid[0]["rating"]))
			return int(rating[0]["rating"]) / 2
		else:
			return None

	def _getPublisher(self, book_id):
		myDB = db.DBConnection()
		publisher = myDB.select(u"SELECT * from books_publishers_link WHERE book = '{0}'".format(book_id))
		if publisher:
			publisher = myDB.select(u"SELECT * from publishers WHERE id = '{0}'".format(publisher[0]["publisher"]))
			return publisher[0]["name"]
		else:
			return None

	def _getSummary(self, book_id):
		myDB = db.DBConnection()
		description = myDB.select(u"SELECT * from comments WHERE book = '{0}'".format(book_id))
		if description:
			return description[0]["text"]

	def _getFormat(self, book_id):
		myDB = db.DBConnection()
		bookformat = myDB.select(u"SELECT * from data WHERE book = '{0}'".format(book_id))
		formate = {}
		for format in bookformat:
			formate[format["format"]] = format["name"] + "." + format["format"].lower()
		return formate

	def _getAuthor(self, book_id):
		myDB = db.DBConnection()
		authorid = myDB.select(u"SELECT * from books_authors_link WHERE book = '{0}'".format(book_id))
		if authorid:
			author = myDB.select(u"SELECT * from authors WHERE id = '{0}'".format(authorid[0]["author"]))
			return author[0]["name"]

	
	def _getTags(self, book_id):
		myDB = db.DBConnection()
		tagids = myDB.select(u"SELECT * from books_tags_link WHERE book = '{0}'".format(book_id))
		taglist = []
		if tagids:
			for tag in tagids:
				mytags = myDB.select(u"SELECT * from tags WHERE id = '{0}'".format(tag["tag"]))
				taglist.append(mytags[0]["name"])
		return taglist

	def _generateBook(self, book_id):
		'''Generate the book objekt that has to be the same everytime... store all infos in the dict...'''
		
		bookinfos = self._getBookInfoFromId(book_id)
		bookinfos["rating"] = self._getBookRating(book_id)
		bookinfos["publisher"] = self._getPublisher(book_id)
		bookinfos["description"] = self._getSummary(book_id)
		bookinfos["format"] = self._getFormat(book_id)
		bookinfos["author"] = self._getAuthor(book_id)
		bookinfos["series_name"] = self._getBookSeries(book_id)
		bookinfos["tags"] = self._getTags(book_id)
		return bookinfos
		
	def listAllBooksASC(self):
		myDB = db.DBConnection()
		books = myDB.select(u"SELECT * from books ORDER BY sort ASC")
		newbooks = []		
		for book in books:
		 	book = self._generateBook(book["id"])
		 	newbooks.append(book)
		#newbooks = self._generateBook(54)
		return newbooks

	def listBooks(self):
		myDB = db.DBConnection()
		books = myDB.select(u"SELECT * from books ORDER BY last_modified ASC LIMIT 10")
		newbooks = []		
		for book in books:
		 	book = self._generateBook(book["id"])
		 	newbooks.append(book)
		#newbooks = self._generateBook(54)
		return newbooks

	def listByAuthor(self, name):
		myDB = db.DBConnection()
		authors = myDB.select(u"SELECT * from authors WHERE name = '{0}'".format(name))
		books = myDB.select(u"SELECT * from books_authors_link WHERE author = '{0}'".format(authors[0]["id"]))
		newbooks = []
		for book in books:
			book = self._generateBook(book["book"])
			newbooks.append(book)
		return newbooks

	def listAuthors(self):
		myDB = db.DBConnection()
		authors = myDB.select(u"SELECT * from authors ORDER BY sort ASC")
		return authors
		
	def listBySeries(self, name):
		myDB = db.DBConnection()
		series = myDB.select(u"SELECT * from series WHERE name = '{0}'".format(name))
		books = myDB.select(u"SELECT * from books_series_link WHERE series = '{0}'".format(series[0]["id"]))
		newbooks = []
		for book in books:
			book = self._generateBook(book["book"])
			newbooks.append(book)
		return newbooks

	def listSeries(self):
		myDB = db.DBConnection()
		series = myDB.select(u"SELECT * from series")
		# newbooks = []
		# for serie in series:

		# 	books = myDB.select("SELECT * from books_series_link WHERE series = '{0}'".format(serie["id"]))
		
		# 	for book in books:
		# 		book = self._generateBook(book["book"])
		# 		newbooks.append(book)
		# return newbooks
		return series

	def listByTags(self, name):
		myDB = db.DBConnection()
		tags = myDB.select(u"SELECT * from tags WHERE name LIKE '%{0}%'".format(name))
		books = myDB.select(u"SELECT * from books_tags_link WHERE tag = '{0}'".format(tags[0]["id"]))
		newbooks = []
		for book in books:
			book = self._generateBook(book["book"])
			newbooks.append(book)
		return newbooks

	def listTags(self):
		myDB = db.DBConnection()
		tags = myDB.select(u"SELECT * from tags")
		return tags

	def searchTitle(self, searchstring):
		response = myDB.select(u"SELECT * from books WHERE title LIKE '%{0}%' ORDER BY sort ASC".format(searchstring))
		book = self._generateBook(response, "name")
		return book

	def searchAuthor(self, searchstring):
		myDB = db.DBConnection()
		books = myDB.select(u"SELECT * from books WHERE author_sort LIKE '%{0}%' ORDER BY author_sort ASC".format(searchstring))
		print books
		newbooks = []
		for book in books:
			book = self._generateBook(book["id"])
			newbooks.append(book)
		return newbooks

	def searchContent(self, searchstring):
		myDB = db.DBConnection()
		booksids = myDB.select(u"SELECT * from comments WHERE text LIKE '%{0}%'".format(searchstring))
		print booksids
		newbooks = []
		for book in booksids:
			book = self._generateBook(book["book"])
			newbooks.append(book)
		return newbooks

	def searchRating(self, searchstring):
		response = myDB.select(u"SELECT * from books_ratings_link WHERE rating = '{0}'".format(searchstring))
		return response

	def searchSeries(self, searchstring):
		myDB = db.DBConnection()
		response = myDB.select(u"SELECT * from series WHERE name LIKE '%{0}%' ORDER BY sort ASC".format(searchstring))
		print response
		book = self._generateBook(response)
		return book
		

	def getDetails(self, id):
		pass

	def allBooks(self):
		myDB = db.DBConnection()


