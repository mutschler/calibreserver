from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory, make_response
from cps import db, config
import os
from sqlalchemy.sql.expression import func
from math import ceil

app = (Flask(__name__))


#simple pagination for the feed
class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

##pagination links in jinja
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route("/feed")
def feed_index():
    xml = render_template('index.xml')
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route("/feed/osd")
def feed_osd():
    xml = render_template('osd.xml')
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route("/feed/search", methods=["GET"])
def feed_search():
    term = request.args.get("query")
    if term:
        random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
        entries = db.session.query(db.Books).filter(db.or_(db.Books.tags.any(db.Tags.name.like("%"+term+"%")),db.Books.authors.any(db.Authors.name.like("%"+term+"%")),db.Books.title.like("%"+term+"%"))).all()
        xml = render_template('feed.xml', searchterm=term, entries=entries)
    else:
        xml = render_template('feed.xml', searchterm="")
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route("/feed/new")
def feed_new():
    off = request.args.get("start_index")
    if off:
        entries = db.session.query(db.Books).order_by(db.Books.last_modified.desc()).offset(off).limit(config.NEWEST_BOOKS)
    else:
        entries = db.session.query(db.Books).order_by(db.Books.last_modified.desc()).limit(config.NEWEST_BOOKS)
        off = 0
    xml = render_template('feed.xml', entries=entries, next_url="/feed/new?start_index=%d" % (int(config.NEWEST_BOOKS) + int(off)))
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route("/feed/hot")
def feed_hot():
    off = request.args.get("start_index")
    if off:
        entries = db.session.query(db.Books).filter(db.Books.ratings.any(db.Ratings.rating > 9)).offset(off).limit(config.NEWEST_BOOKS)
    else:
        entries = db.session.query(db.Books).filter(db.Books.ratings.any(db.Ratings.rating > 9)).limit(config.NEWEST_BOOKS)
        off = 0

    xml = render_template('feed.xml', entries=entries, next_url="/feed/hot?start_index=%d" % (int(config.NEWEST_BOOKS) + int(off)))
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route("/")
def index():
    random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
    entries = db.session.query(db.Books).order_by(db.Books.last_modified.desc()).limit(config.NEWEST_BOOKS)
    print request.user_agent.__dict__
    print request.user_agent
    #{'platform': 'linux', 'version': '528.5', 'string': 'Mozilla/5.0 (Linux; U; de-DE) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)', 'language': 'de-DE', 'browser': 'safari'}
    #Mozilla/5.0 (Linux; U; de-DE) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)
    return render_template('index.html', random=random, entries=entries, title="Latest Books")

@app.route("/hot")
def hot_books():
    random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
    entries = db.session.query(db.Books).filter(db.Books.ratings.any(db.Ratings.rating > 9)).order_by(db.Books.last_modified.desc()).limit(config.NEWEST_BOOKS)
    return render_template('index.html', random=random, entries=entries, title="Hot Books")

@app.route("/stats")
def stats():
    counter = len(db.session.query(db.Books).all())
    return render_template('stats.html', counter=counter, title="Statistics")

@app.route("/discover")
def discover():
    entries = db.session.query(db.Books).order_by(func.random()).limit(config.NEWEST_BOOKS)
    return render_template('discover.html', entries=entries, title="%s Random Books" % config.NEWEST_BOOKS)

@app.route("/book/<int:id>")
def show_book(id):
    entries = db.session.query(db.Books).filter(db.Books.id == id).first()
    return render_template('detail.html', entry=entries,  title=entries.title)

@app.route("/category/<name>")
def category(name):
    random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
    if name != "all":
        entries = db.session.query(db.Books).filter(db.Books.tags.any(db.Tags.name.like("%" +name + "%" ))).order_by(db.Books.last_modified.desc()).all()
    else:
        entries = db.session.query(db.Books).all()
    return render_template('index.html', random=random, entries=entries, title="Category: %s" % name)

@app.route("/series/<name>")
def series(name):
    random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
    entries = db.session.query(db.Books).filter(db.Books.series.any(db.Series.name.like("%" +name + "%" ))).order_by(db.Books.series_index).all()
    return render_template('index.html', random=random, entries=entries, title="Series: %s" % name)

@app.route("/admin/")
def admin():
    return "Admin ONLY!"

def title_sort(title):
    return title

@app.route("/search", methods=["GET"])
def search():
    term = request.args.get("query")
    if term:
        random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
        entries = db.session.query(db.Books).filter(db.or_(db.Books.tags.any(db.Tags.name.like("%"+term+"%")),db.Books.series.any(db.Series.name.like("%"+term+"%")),db.Books.authors.any(db.Authors.name.like("%"+term+"%")),db.Books.title.like("%"+term+"%"))).all()
        return render_template('search.html', searchterm=term, entries=entries)
    else:
        return render_template('search.html', searchterm="")

@app.route("/author/<name>")
def author(name):
    random = db.session.query(db.Books).order_by(func.random()).limit(config.RANDOM_BOOKS)
    entries = db.session.query(db.Books).filter(db.Books.authors.any(db.Authors.name.like("%" +  name + "%"))).all()
    return render_template('index.html', random=random, entries=entries, title="Author: %s" % name)

@app.route("/cover/<path:cover_path>")
def get_cover(cover_path):
    return send_from_directory(os.path.join(config.DB_ROOT, cover_path), "cover.jpg")

@app.route("/download/<int:book_id>/<format>")
def get_download_link(book_id, format):
    book = db.session.query(db.Books).filter(db.Books.id == book_id).first()
    data = db.session.query(db.Data).filter(db.Data.book == book.id).filter(db.Data.format == format.upper()).first()
    response = make_response(send_from_directory(os.path.join(config.DB_ROOT, book.path), data.name + "." +format))
    response.headers["Content-Disposition"] = "attachment; filename=%s.%s" % (data.name, format)
    return response

@app.route("/admin/book/<int:book_id>", methods=['GET', 'POST'])
def edit_book(book_id):
    ## create the function for sorting...
    db.session.connection().connection.connection.create_function("title_sort",1,db.title_sort)
    book = db.session.query(db.Books).filter(db.Books.id == book_id).first()
    if request.method == 'POST':
        to_save = request.form.to_dict()
        print to_save
        #print title_sort(to_save["book_title"])
        book.title = to_save["book_title"]
        book.authors[0].name = to_save["author_name"]

        if book.series_index != to_save["series_index"]:
            book.series_index = to_save["series_index"]
        if len(book.comments):
            book.comments[0].text = to_save["description"]
        else:
            book.comments.append(db.Comments(text=to_save["description"], book=book.id))

        for tag in to_save["tags"].split(","):
            if tag.strip():
                print tag
                is_tag = db.session.query(db.Tags).filter(db.Tags.name.like('%' + tag.strip() + '%')).first()
                if is_tag:
                    book.tags.append(is_tag)
                else:
                    new_tag = db.Tags(name=tag.strip())
                    book.tags.append(new_tag)
        if to_save["series"].strip():
            is_series = db.session.query(db.Series).filter(db.Series.name.like('%' + to_save["series"].strip() + '%')).first()
            if is_series:
                book.series.append(is_series)
            else:
                new_series = db.Series(name=to_save["series"].strip(), sort=to_save["series"].strip())
                book.series.append(new_series)
        if to_save["rating"].strip():
            is_rating = db.session.query(db.Ratings).filter(db.Ratings.rating == int(to_save["rating"].strip())).first()
            if is_rating:
                book.ratings[0] = is_rating
            else:
                new_rating = db.Ratings(rating=int(to_save["rating"].strip()))
                book.ratings[0] = new_rating
        db.session.commit()
        if to_save["detail_view"]:
            return redirect(url_for('show_book', id=book.id))
        else:
            return render_template('edit_book.html', book=book)
    else:
        return render_template('edit_book.html', book=book)

# @app.route('/admin/delete/<int:book_id>')
# def delete_book(book_id):
#     to_delete = db.session.query(db.Books).filter(db.Books.id == book_id).first()
#     print to_delete
#     db.session.delete(to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))
