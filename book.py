from calibre import db
from calibre.logger import logger
from calibre import config
from calibre import books
import os

book = books.Book()
book.searchName("Auge")

bookers = book.searchSeries("Robert")
for book in bookers:
	print book