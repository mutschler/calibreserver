import os
import sys
import logging

from lib import pyservice
from lib.bottle import route, run, template, static_file, error, post, request, TEMPLATE_PATH
from calibre import helper
from calibre import config




# monkey patching for BaseHTTPRequestHandler.log_message
def log_message(obj, format, *args):
    logging.info("%s %s" % (obj.address_string(), format%args))

@route('/authors')
def index():
	content = helper.authorsList()
	return template('authors_list', content=content)

@route('/authors/<name>')
def index(name):
	content = helper.searchAuthor(name.decode('utf-8'))
	#print type("{0}".format(name).decode('utf-8'))
	return template('books', content=content)

@route('/tag/<name>')
def index(name):
	content = helper.searchTag(name.decode('utf-8'))
	return template('books', content=content)

@route('/series')
@route('/series/<name>')
def index(name=""):
	content = helper.searchSeries(name.decode('utf-8'))
	return template('books', content=content)

@route('/details/<bookid:int>')
def limit(bookid=0):
	content = helper.bookDetails(bookid)
	return template('details', content=content)

@route('/books')
@route('/books/<limit:int>')
def limit(limit=300):
	content = helper.booksList(limit)
	return template('books', content=content)


@route('/rating/<count:int>')
def limit(count=5):
	content = helper.ratingsList(count)
	return template('books', content=content)

@route('/')
@route('/books/new')
@route('/books/new/<limit:int>')
def newest(limit=20):
	content = helper.newestBooks(limit)
	return template('books', content=content)


@route('/download/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config.DB_ROOT, download=True, mimetype='application/epub+zip')


@post('/search') # or @route('/login', method='POST')
def login_submit():
    searchfor = request.forms.get('searchfor')
    searchtype = request.forms.get('searchtype')
    content = helper.doSearch(searchfor, searchtype)
    return template('books', content=content)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config.TEMPLATEDIR)

@route('/favicon.ico')
def server_static():
    return static_file('favicon.ico', root=config.TEMPLATEDIR)

@error(404)
def error404(error):
    return 'Nothing here, sorry'

class CalibreServerProcess(pyservice.Process):

    pidfile = os.path.join(os.getcwd(), 'calibreserver.pid')
    logfile = os.path.join(os.getcwd(), 'calibreserver.log')

    def __init__(self):
        super(CalibreServerProcess, self).__init__()
        
        from BaseHTTPServer import BaseHTTPRequestHandler
        BaseHTTPRequestHandler.log_message = log_message
            
    def run(self):
        logging.info('CalibreServer starting up')
        TEMPLATE_PATH.append(config.TEMPLATEDIR)
        run(host='0.0.0.0', port=config.PORT)

if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] in 'start stop restart status'.split():
        pyservice.service('calibreserver.CalibreServerProcess', sys.argv[1])
    else:
        print 'usage: calibreserver <start,stop,restart,status>'