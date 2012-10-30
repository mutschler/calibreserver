from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from calibre import config
import os

dbpath = os.path.join(config.DB_ROOT, "metadata.db")
engine = create_engine('sqlite:///{0}'.format(dbpath), echo=True)

Base = declarative_base()

# class User(Base):
# 	__tablename__ = 'users'

# 	id = Column(Integer, primary_key=True)
# 	name = Column(String)
# 	fullname = Column(String)
# 	password = Column(String)

# 	def __init__(self, name, fullname, password):
# 		self.name = name
# 		self.fullname = fullname
# 		self.password = password

# 	def __repr__(self):
# 		return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

books_authors_link = Table('books_authors_link', Base.metadata,
	Column('book', Integer, ForeignKey('books.id'), primary_key=True),
	Column('author', Integer, ForeignKey('authors.id'), primary_key=True)
	)

books_tags_link = Table('books_tags_link', Base.metadata,
	Column('book', Integer, ForeignKey('books.id'), primary_key=True),
	Column('tag', Integer, ForeignKey('tags.id'), primary_key=True)
	)


class Comments(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True)
	text = Column(String)
	book = Column(Integer, ForeignKey('books.id'))

	def __init__(self, text, book):
		self.text = text
		self.book = book

	def __repr__(self):
		return u"<Comments({0})>".format(self.text)
		

class Tags(Base):
	__tablename__ = 'tags'

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return u"<Tags('{0})>".format(self.name)

class Authors(Base):
	__tablename__ = 'authors'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	sort = Column(String)
	link = Column(String)

	#books1 = relationship('Books', secondary=books_authors_link, backref='authors')

	def __init__(self, name, sort, link):
		self.name = name
		self.sort = sort
		self.link = link

	def __repr__(self):
		return u"<Authors('{0},{1}{2}')>".format(self.name, self.sort, self.link)

class Data(Base):
	__tablename__ = 'data'

	id = Column(Integer, primary_key=True)
	book = Column(Integer, ForeignKey('books.id'))
	format = Column(String)
	uncompressed_size = Column(Integer)
	name = Column(String)

	#books1 = relationship('Books', secondary=books_authors_link, backref='authors')

	def __init__(self, book, format, uncompressed_size, name):
		self.book = book
		self.format = format
		self.uncompressed_size = uncompressed_size
		self.name = name

	def __repr__(self):
		return u"<Data('{0},{1}{2}{3}')>".format(self.book, self.format, self.uncompressed_size, self.name)

class Books(Base):
	__tablename__ = 'books'

	id = Column(Integer,primary_key=True)
	title = Column(String)
	sort = Column(String)
	path = Column(String)
	has_cover = Column(Integer)

	authors = relationship('Authors', secondary=books_authors_link, backref='books')
	tags = relationship('Tags', secondary=books_tags_link, backref='books')
	comments = relationship('Comments', backref='books')
	data = relationship('Data', backref='books')

	def __init__(self, title, sort, path, has_cover, authors, tags):
		self.title = title
		self.sort = sort
		self.path = path
		self.has_cover = has_cover
		self.tags = tags


	def __repr__(self):
		return u"<Books('{0},{1}{2}{3}')>".format(self.title, self.sort, self.path, self.has_cover)



Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# ed_user = User('ed', 'Ed Jones', 'edspassword')
# session.add(ed_user)
# our_user = session.query(Books).filter(Books.title.like('%Kind%'))#.first() 
# print dir(our_user)

# for a in our_user:
# 	print u"Titel: {0}".format(a.title)
# 	if a.authors:
# 		print u"Author: {0}".format(a.authors[0].name)
# 		#print a.authors[0].name
# 	# for cimment in a.comments:
# 	# 	print cimment.text
# 	tags = []
# 	for tag in a.tags:
# 		tags.append(tag.name)
# 	if tags:
# 		print u"tags: {0}".format(tags)

# print our_user.title, our_user.authors, our_user.tags
# for a in our_user.authors:
# 	print a.name

# for c in our_user.comments:
# 	print c.text

# for b in our_user.tags:
# 	print b.name

result = (
    session.query(Books)
        .filter(Books.id == 8).first()
)

for a in result.comments:
	print a.text
