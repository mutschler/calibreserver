#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
mimetypes.add_type('application/xhtml+xml','.xhtml')
from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory, make_response, g, flash, Blueprint, Response
from cps import db, config, ub, helper
import os
from sqlalchemy.sql.expression import func
from math import ceil
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _
import requests, zipfile
from werkzeug.security import generate_password_hash, check_password_hash
from babel import Locale as LC

from functools import wraps

feed = Blueprint('feed', __name__, template_folder='templates/feed', url_prefix='/feed')

def _check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = ub.session.query(ub.User).filter(ub.User.nickname == username).first()
    if user and check_password_hash(user.password, password):
            login_user(user, remember = True)
            return True
    else:
        return False   # return username == 'admin' and password == 'secret'

def _authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def http_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _authenticate()
        return f(*args, **kwargs)
    return decorated


@feed.route("/")
@http_auth_required
def feed_index():
    print request.headers
    print request.__dict__
    xml = render_template('index.xml')
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@feed.route("/osd")
@http_auth_required
def feed_osd():
    xml = render_template('osd.xml')
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@feed.route("/search", methods=["GET"])
@http_auth_required
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

@feed.route("/new")
@http_auth_required
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


@feed.route("/discover")
@http_auth_required
def feed_discover():
    off = request.args.get("start_index")
    if off:
        entries = db.session.query(db.Books).order_by(func.random()).offset(off).limit(config.NEWEST_BOOKS)
    else:
        entries = db.session.query(db.Books).order_by(func.random()).limit(config.NEWEST_BOOKS)
        off = 0
    xml = render_template('feed.xml', entries=entries, next_url="/feed/discover?start_index=%d" % (int(config.NEWEST_BOOKS) + int(off)))
    response= make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@feed.route("/hot")
@http_auth_required
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

