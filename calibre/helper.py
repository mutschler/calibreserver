from calibre import db
from calibre import config

import os

def searchAuthor(authorname):
	result = (
    db.session.query(db.Books)
        .filter(db.Books.authors.any(db.Authors.name.like(u'%{0}%'.format(authorname))))
        .all()
	)
	return result

def searchTitle(titlename):
	result = (
    db.session.query(db.Books)
        .filter(db.Books.title.like(u'%{0}%'.format(titlename)))
        .all()
	)
	return result

def searchDescription(searchfor):
	result = (
    db.session.query(db.Books)
        .filter(db.Books.comments.any(db.Comments.text.like(u'%{0}%'.format(searchfor))))
        .all()
	)
	return result

def searchTag(tagname):
	result = (
    db.session.query(db.Books)
        .filter(db.Books.tags.any(db.Tags.name.like(u'%{0}%'.format(tagname))))
        .all()
	)
	return result

def searchSeries(seriesname):
	result = (
    db.session.query(db.Books)
        .filter(db.Books.series.any(db.Series.name.like(u'%{0}%'.format(seriesname))))
        .all()
	)
	return result

def authorsList():
	result = (
    db.session.query(db.Authors)
        .order_by(db.Authors.sort)
        .all()
	)
	return result

def ratingsList(rating):
	rating = rating*2
	result = (
    db.session.query(db.Books)
        .filter(db.Books.ratings.any(db.Ratings.rating == rating))
        .all()
	)
	return result

def bookDetails(bookid):
	result = (
	    db.session.query(db.Books)
	        .filter(db.Books.id == bookid).first()
	)
	return result

def booksList(limit):
	result = (
    db.session.query(db.Books)
        .order_by(db.Books.sort)
        .limit(limit)
	)
	return result

def newestBooks(limit):
	result = (
    db.session.query(db.Books)
        .order_by(db.Books.last_modified)
        .limit(limit)
	)
	return result

def doSearch(searchfor, searchtype):
	if (searchtype == "authors"):
		result = searchAuthor(searchfor)
	if (searchtype == "description"):
		result = searchDescription(searchfor)
	if (searchtype == "title"):
		result = searchTitle(searchfor)

	return result